import requests
import time

def call_pricing_api(filter_params: dict) -> dict:
    """
    Makes the API call with filter_params, returns parsed pricing data.
    """
    url = "https://prices.azure.com/api/retail/prices"
    response_time_ms = None

    try:
        start_time = time.time()
        response = requests.get(url, params=filter_params)
        response.raise_for_status()
        end_time = time.time()
        response_time_ms = round((end_time - start_time) * 1000, 2)  # in ms

        data = response.json().get("Items", [])
        return data, response_time_ms
    except Exception as e:
        return [], response_time_ms
