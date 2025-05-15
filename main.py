import sys
import time
import tracemalloc

from input_handler.cli_args import parse_cli_args
from input_handler.file_utils import read_input_csv, generate_output_filename
from mapper.column_mapper import load_column_map, map_columns
from mapper.validator import load_filter_config, validate_fields

def main():
    start_time = time.perf_counter()
    tracemalloc.start()

    args = parse_cli_args()

    if args.billing_type != "EA":
        print(f"Billing type '{args.billing_type}' is not supported yet.")
        sys.exit(1)

    try:
        df = read_input_csv(args.input_file)
    except Exception as e:
        print(f"Failed to read input file: {e}")
        sys.exit(1)

    column_map = load_column_map("config/column_map.yaml")
    df_mapped = map_columns(df, column_map)
    filter_config = load_filter_config("config/ea_filters.yaml")

    try:
        validate_fields(
            columns=df_mapped.columns.tolist(),
            strategy=args.filter_strategy,
            custom_fields=args.custom_fields,
            filter_config=filter_config
        )
    except ValueError as e:
        print(f"Validation failed: {e}")
        sys.exit(1)

    output_file = generate_output_filename()
    df_mapped.to_csv(output_file, index=False)
    print(f"Mapped CSV saved as: {output_file}")

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.perf_counter()

    print(f"Execution time: {end_time - start_time:.4f} seconds")
    print(f"Current memory usage: {current / 1024:.2f} KB")
    print(f"Peak memory usage: {peak / 1024:.2f} KB")

if __name__ == "__main__":
    main()
