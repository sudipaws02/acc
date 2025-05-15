import yaml

def load_filter_config(yaml_path: str) -> dict:
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)

def validate_fields(columns: list, strategy: str, custom_fields: list = None, filter_config: dict = None) -> bool:
    """
    Validates the presence of required fields in raw input (unmapped) columns.
    """
    if filter_config is None:
        raise ValueError("[ERROR] Filter config is required for validation")

    mandatory = set(filter_config.get("mandatory_filters", []))
    recommended = set(filter_config.get("recommended_filters", []))

    cols_set = set(columns)
    missing_mandatory = mandatory - cols_set

    if missing_mandatory:
        raise ValueError(f"[ERROR] Validation Failed:\n  Missing Mandatory Filters: {missing_mandatory}")
    else:
        print(f"[INFO] Mandatory Filters Present: {mandatory}")

    if strategy == "recommended":
        missing_recommended = recommended - cols_set
        if missing_recommended:
            raise ValueError(f"[ERROR] Validation Failed:\n  Missing Recommended Filters: {missing_recommended}")
        else:
            print(f"[INFO] Recommended Filters Present: {recommended}")

    elif strategy == "custom":
        if not custom_fields:
            raise ValueError("[ERROR] Custom fields must be provided when using 'custom' strategy.")

        custom_set = set(custom_fields)
        missing_custom = custom_set - cols_set
        if missing_custom:
            raise ValueError(f"[ERROR] Validation Failed:\n  Missing Custom Fields: {missing_custom}")
        else:
            print(f"[INFO] Custom Filters Present: {custom_set}")

    else:
        raise ValueError(f"[ERROR] Unknown filter strategy: '{strategy}'")

    print("[SUCCESS] Validation Passed: Required fields are present.")
    return True
