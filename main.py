import time
import tracemalloc
import pandas as pd

from config.cli_args import parse_cli_args
from config.file_utils import read_input_csv, generate_output_filename
from mapper.column_mapper import load_column_map, map_columns
from mapper.validator import load_filter_config, validate_fields
from enricher.enrich_data import enrich_data


def main():
    # Start timers and memory tracking
    tracemalloc.start()
    start_time = time.time()

    print("[TASK] Parsing CLI arguments")
    args = parse_cli_args()

    print("[TASK] Reading input CSV")
    df = read_input_csv(args.input_file)

    print("[TASK] Loading column map and mapping columns")
    column_map = load_column_map(args.column_map)
    df_mapped = map_columns(df, column_map)

    print("[TASK] Validating mapped fields")
    filter_config = load_filter_config(args.filter_config)
    mapped_columns = df_mapped.columns.tolist()

    validate_fields(
        columns=mapped_columns,
        strategy=args.filter_strategy,
        custom_fields=args.custom_fields,
        filter_config=filter_config
    )

    # Determine which fields to use for API filtering
    if args.filter_strategy == "recommended":
        field_keys = filter_config["recommended_filters"]
    else:
        field_keys = args.custom_fields

    print("[TASK] Enriching data via Azure Retail Prices API")
    enriched_df, ambiguous_df = enrich_data(df_mapped, field_keys)

    print("[TASK] Writing enriched output")
    output_file = generate_output_filename(billing_type=args.billing_type)
    enriched_df.to_csv(output_file, index=False)

    if not ambiguous_df.empty:
        ambiguous_output_file = output_file.replace(".csv", "_ambiguous.csv")
        ambiguous_df.to_csv(ambiguous_output_file, index=False)
        print(f"[INFO] Ambiguous records written to: {ambiguous_output_file}")

    # Time and memory stats
    end_time = time.time()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"[SUMMARY] Total Time Taken: {round(end_time - start_time, 2)} seconds")
    print(f"[SUMMARY] Peak Memory Usage: {round(peak_memory / (1024 * 1024), 2)} MB")
    print(f"[SUMMARY] Total Records Processed: {len(df_mapped)}")
    print(f"[SUMMARY] Enriched Records: {len(enriched_df)}")
    print(f"[SUMMARY] Ambiguous Records: {len(ambiguous_df)}")


if __name__ == "__main__":
    main()
