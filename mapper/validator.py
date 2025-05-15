import yaml

def load_filter_config(yaml_path: str) -> dict:
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)

def validate_fields(columns: list, strategy: str, custom_fields: list = None, filter_config: dict = None) -> bool:
    if filter_config is None:
        raise ValueError("[ERROR] Filter config is required for validation")

    mandatory = set(filter_config.get("mandatory_filters", []))
    recommended = set(filter_config.get("recommended_filters", []))
    cols_set = set(columns)

    # Step 1: Mandatory check (common for all)
    missing_mandatory = mandatory - cols_set
    if missing_mandatory:
        raise ValueError(f"Missing mandatory filters: {missing_mandatory}")
    print(f"[INFO] Mandatory Filters Present: {mandatory}")

    # Step 2: Strategy-specific check
    if strategy == "recommended":
        missing_recommended = recommended - cols_set
        if missing_recommended:
            raise ValueError(f"Missing recommended filters: {missing_recommended}")
        print(f"[INFO] Recommended Filters Present: {recommended}")
    elif strategy == "custom":
        if not custom_fields:
            raise ValueError("Custom fields must be provided for custom strategy")
        custom_set = set(custom_fields)
        missing_custom = custom_set - cols_set
        if missing_custom:
            raise ValueError(f"Missing custom filter fields in input columns: {missing_custom}")
        print(f"[INFO] Custom Filters Present: {custom_set}")
    else:
        raise ValueError(f"Unknown filter strategy '{strategy}'")

    print("[SUCCESS] Validation Passed: Required fields are present.")
    return True