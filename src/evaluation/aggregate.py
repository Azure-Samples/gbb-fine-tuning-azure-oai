from typing import List

from promptflow.core import tool


@tool
def aggregate(processed_results: List[str]):
    """
    This tool aggregates the processed result of all lines to the variant level and log metric for each variant.

    :param processed_results: List of the output of line_process node.
    """

    # Add your aggregation logic here
    # aggregated_results should be a dictionary with the metric name as the key and the metric value as the value.
    results_num = sum(processed_results) / len(processed_results)
    print(results_num)
    print(processed_results)

    # Log metric for each variant
    from promptflow.core import log_metric
    log_metric(key="results_num", value=results_num)

    return results_num
