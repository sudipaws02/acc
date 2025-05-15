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
    memory_snapshots = []

    try:
        print("[TASK] Parsing CLI arguments...")
        args = parse_cli_args()
        memory_snapshots.append(tracemalloc.get_traced_memory()[1])

        print("[TASK] Reading input CSV...")
        df = read_input_csv(args.input_file)
        memory_snapshots.append(tracemalloc.get_traced_memory()[1])

        print("[TASK] Loading column mappings...")
        column_map = load_column_map(args.column_map)
        memory_snapshots.append(tracemalloc.get_traced_memory()[1])

        print("[TASK] Mapping columns to standard Azure fields...")
        mapped_df = map_columns(df, column_map)
        memory_snapshots.append(tracemalloc.get_traced_memory()[1])

        print("[TASK] Loading filter configuration...")
        filter_config_path = f"config/{args.billing_type.lower()}_filters.yaml"
        filter_config = load_filter_config(filter_config_path)
        memory_snapshots.append(tracemalloc.get_traced_memory()[1])

        print("[TASK] Validating input fields based on strategy...")
        mapped_columns = mapped_df.columns.tolist()
        validate_fields(
            columns=mapped_columns,
            strategy=args.filter_strategy,
            custom_fields=args.custom_fields,
            filter_config=filter_config
        )
        memory_snapshots.append(tracemalloc.get_traced_memory()[1])

        print("[TASK] Generating output filename...")
        output_file = generate_output_filename(billing_type=args.billing_type)
        memory_snapshots.append(tracemalloc.get_traced_memory()[1])

        print("[TASK] Writing mapped data to output file...")
        mapped_df.to_csv(output_file, index=False)
        print(f"[SUCCESS] Output written to: {output_file}")
        memory_snapshots.append(tracemalloc.get_traced_memory()[1])

    except ValueError as ve:
        print(str(ve))
        sys.exit(1)

    except Exception as e:
        print(f"[FATAL] Unexpected error: {e}")
        sys.exit(1)

    finally:
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        average_memory = sum(memory_snapshots) / len(memory_snapshots) if memory_snapshots else 0

        print("\n[METRICS] Execution Time      :", f"{end_time - start_time:.2f} seconds")
        print("[METRICS] Peak Memory Usage   :", f"{peak / 1024 / 1024:.2f} MB")
        print("[METRICS] Average Memory Usage:", f"{average_memory / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
