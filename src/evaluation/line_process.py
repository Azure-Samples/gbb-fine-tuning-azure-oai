from promptflow.core import tool
import json


@tool
def line_process(groundtruth: list, prediction: dict):
    """
    This tool processes the prediction of a single line and returns the processed result.

    :param groundtruth: the groundtruth of a single line.
    :param prediction: the prediction of a single line.
    """

    # Add your line processing logic here
    groundtruth = groundtruth[2]["function_call"]
    name_match = groundtruth['name'] == prediction['name']
    arguments_match = json.loads(groundtruth['arguments']) == json.loads(prediction['arguments'])
    
    if name_match and arguments_match:
        result = 1
    else:
        result = 0

    return result 
