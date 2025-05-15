import argparse

def parse_cli_args():
    parser = argparse.ArgumentParser(description="Azure Pricing Tool")

    parser.add_argument(
        "--billing-type",
        choices=["EA"],
        required=True,
        help="Billing type: EA (Enterprise Agreement)"
    )
    parser.add_argument(
        "--input-file",
        required=True,
        help="Path to the input CSV file"
    )
    parser.add_argument(
        "--filter-strategy",
        choices=["recommended", "custom"],
        required=True,
        help="Strategy to apply for Azure Retail Prices API filters"
    )
    parser.add_argument(
        "--custom-fields",
        nargs="*",
        help="Custom filter fields to use if strategy is 'custom'"
    )
    parser.add_argument(
        "--column-map",
        required=True,
        help="Path to column_map.yaml configuration file"
    )
    parser.add_argument(
        "--logs",
        choices=["enabled", "disabled"],
        default="disabled",
        help="Enable or disable stdout logging"
    )

    args = parser.parse_args()

    if args.filter_strategy == "custom" and not args.custom_fields:
        parser.error("--custom-fields is required when --filter-strategy is 'custom'")

    return args
