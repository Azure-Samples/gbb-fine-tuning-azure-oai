# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from promptflow.core import tool
from promptflow.connections import AzureOpenAIConnection
import yfinance as yf
import pandas as pd
import json 
from openai import AzureOpenAI
from function_definitions import full_function_definitions, short_function_definitions

def get_current_stock_price(symbol: str) -> str:
    ticker = yf.Ticker(symbol).info
    info = {}
    if "currentPrice" in ticker:
        market_price = ticker["currentPrice"]
        info = {"symbol": symbol, "current_price": market_price}
    else:
        print(f"{symbol} is not valid.")
    return json.dumps(info)


def get_last_nday_stock_price(symbol: str, period: str) -> str:
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    df = pd.DataFrame(data)
    return df.to_json(orient="records")


@tool
def function_calling_tool(user_messages: list, aoai_conn: AzureOpenAIConnection, tool_description:str, deployment_name:str) -> str:

    client = AzureOpenAI(
        azure_endpoint=aoai_conn.api_base,
        api_key=aoai_conn.api_key,
        api_version=aoai_conn.api_version
    )

    if tool_description == "full":
        functions = full_function_definitions
    else:
        functions = short_function_definitions


    messages = [
                {"role": "system", "content": "You are an assistant that provides functions related to stock prices."},
        ]

    messages.append({"role": "user", "content": user_messages[1]["content"]})

    completion = client.chat.completions.create(
                model=deployment_name,
                messages=messages,
                temperature=0.0, 
                functions=functions,
                function_call="auto",
            )

    response_message = completion.choices[0].message

    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens

    # Check if the model wants to call a function
    function_calls_dict = {}
    function_calls = response_message.function_call
    if function_calls:
        function_calls_dict = {"name": function_calls.name, "arguments": function_calls.arguments}
        function_name = response_message.function_call.name
        available_functions = {
            "get_current_stock_price": get_current_stock_price,
            "get_last_nday_stock_price": get_last_nday_stock_price,
        }
        function_to_call = available_functions[function_name]

        function_args = json.loads(response_message.function_call.arguments)
        function_response = function_to_call(**function_args)

        # Append function response to user messages
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response
            }   
        )

        # Get the last message from the model
        second_response = client.chat.completions.create(
            model=deployment_name, 
            messages=messages
        )

        prompt_tokens += second_response.usage.prompt_tokens
        completion_tokens += second_response.usage.completion_tokens

    return {
        "answer": second_response.choices[0].message.content, 
        "prompt_tokens": prompt_tokens, 
        "completion_tokens": completion_tokens,
        "function_calls": function_calls_dict
        }
