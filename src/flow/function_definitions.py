full_function_definitions = [
    {
        "name": "get_current_stock_price",
        "description": """ 
                This function is designed to fetch the current market price of a specified stock symbol. It leverages the yfinance library to retrieve real-time stock data. The function takes a single parameter, symbol, which represents the stock ticker symbol (e.g., 'AAPL' for Apple Inc.). Upon successful retrieval, it returns a JSON string that includes the stock symbol and its current price. If the provided symbol is invalid or if there is an issue with the data retrieval, the function will print an error message and return an empty JSON object.
            
                Examples:
                ---------
                Example: Fetching the Current Price of Apple Inc. (AAPL)
                >>> symbol = 'AAPL'
                >>> current_price = get_current_stock_price(symbol)
                >>> print(current_price)
                {
                "symbol": "AAPL",
                "price": 150.00
                }
            """,
        "parameters": {
            "type": "object",
            "properties": {"symbol": {"type": "string", "description": "The stock symbol is a unique series of letters assigned to a security or stock for trading purposes. It is used to uniquely identify publicly traded shares of a particular stock on a particular stock market. For example, 'AAPL' is the stock symbol for Apple Inc. The symbol parameter should be a valid string representing a publicly traded company's stock symbol."}},
            "required": ["symbol"],
        },
    },
    {
        "name": "get_last_nday_stock_price",
        "description": "This function is intended to retrieve historical stock prices for a given stock symbol over a specified period. It uses the yfinance library to access historical market data. The function accepts two parameters: symbol and period. The symbol parameter is a string representing the stock ticker symbol, while the period parameter is a string that specifies the duration for which historical data is required (e.g., '1d' for one day, '1mo' for one month, '1y' for one year, etc.). The function returns the historical stock prices as a JSON string in a records format. This data can be used for analysis, charting, or other financial computations.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "The stock symbol is a unique series of letters assigned to a security or stock for trading purposes. It is used to uniquely identify publicly traded shares of a particular stock on a particular stock market. For example, 'AAPL' is the stock symbol for Apple Inc. The symbol parameter should be a valid string representing a publicly traded company's stock symbol."},
                "period": {"type": "string", "description": "Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max"},
            },
            "required": ["symbol", "period"],
        },
    },
]

short_function_definitions = [
    {
        "name": "get_current_stock_price", 
        "parameters": {"type": "object", "properties": {}, "required": ["symbol"]}
    },
    {
        "name": "get_last_nday_stock_price",
        "parameters": {"type": "object", "properties": {}, "required": ["symbol", "period"]},
    },
]

