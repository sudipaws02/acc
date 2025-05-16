import pandas as pd
from api_caller import call_pricing_api

def enrich_data(df: pd.DataFrame, field_keys: list) -> (pd.DataFrame, pd.DataFrame):
    enriched_rows = []
    ambiguous_rows = []

    for idx, row in df.iterrows():
        request_id = f"REQ{idx + 1}"
        filters = {key: row.get(key) for key in field_keys if key in row}
        filter_tuple = tuple(filters.items())

        api_results, response_time_ms = call_pricing_api(filters)
        api_response_count = len(api_results)

        if api_response_count == 0:
            enriched_row = row.copy()
            enriched_row["RequestID"] = request_id
            enriched_row["unitPrice"] = 0
            enriched_row["unitOfMeasure"] = None
            enriched_row["retailPrice"] = 0
            enriched_row["ApiResponseCount"] = 0
            enriched_row["ApiResponseTimeMs"] = response_time_ms
            enriched_rows.append(enriched_row)

        elif api_response_count == 1:
            enriched_row = row.copy()
            enriched_row["RequestID"] = request_id
            enriched_row["unitPrice"] = api_results[0].get("unitPrice")
            enriched_row["unitOfMeasure"] = api_results[0].get("unitOfMeasure")
            enriched_row["retailPrice"] = api_results[0].get("retailPrice")
            enriched_row["ApiResponseCount"] = 1
            enriched_row["ApiResponseTimeMs"] = response_time_ms
            enriched_rows.append(enriched_row)

        else:
            # Multiple results: append first, track rest
            for i, res in enumerate(api_results):
                enriched_row = row.copy()
                enriched_row["RequestID"] = f"{request_id}-A{i+1}" if i > 0 else request_id
                enriched_row["unitPrice"] = res.get("unitPrice")
                enriched_row["unitOfMeasure"] = res.get("unitOfMeasure")
                enriched_row["retailPrice"] = res.get("retailPrice")
                enriched_row["ApiResponseCount"] = api_response_count
                enriched_row["ApiResponseTimeMs"] = response_time_ms

                if i == 0:
                    enriched_rows.append(enriched_row)
                else:
                    ambiguous_rows.append(enriched_row)

    enriched_df = pd.DataFrame(enriched_rows)
    ambiguous_df = pd.DataFrame(ambiguous_rows)
    return enriched_df, ambiguous_df
