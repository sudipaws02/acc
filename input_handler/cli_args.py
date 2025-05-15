import argparse

def parse_cli_args():
    parser = argparse.ArgumentParser(description="Azure Pricing Tool")

    parser.add_argument(
        "--billing-type",
        choices=["EA"],  # only EA supported for now
        required=True,
        help="Billing type: EA (Enterprise Agreement)"
    )
    parser.add_argument(
        "--input-file",
        required=True,
        help="Path to input CSV file"
    )
    parser.add_argument(
        "--filter-strategy",
        choices=["recommended", "custom"],
        required=True,
        help="Filter strategy to use for API calls"
    )
    parser.add_argument(
        "--custom-fields",
        nargs="*",
        help="List of custom filter fields (if filter-strategy is custom)"
    )
    parser.add_argument(
        "--logs",
        choices=["enabled", "disabled"],
        default="disabled",
        help="Enable or disable logging"
    )

    args = parser.parse_args()

    # Basic validation
    if args.filter_strategy == "custom" and not args.custom_fields:
        parser.error("--custom-fields is required when --filter-strategy is custom")

    return args
