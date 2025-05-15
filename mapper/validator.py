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

    missing_mandatory = mandatory - cols_set
    if missing_mandatory:
        msg = f"[ERROR] Validation Failed: Missing mandatory filters: {missing_mandatory}"
        print(msg)
        raise ValueError(msg)
    else:
        print(f"[INFO] Mandatory Filters Present: {mandatory}")

    if strategy == "recommended":
        missing_recommended = recommended - cols_set
        if missing_recommended:
            msg = f"[ERROR] Validation Failed: Missing recommended filters: {missing_recommended}"
            print(msg)
            raise ValueError(msg)
        else:
            print(f"[INFO] Recommended Filters Present: {recommended}")
    elif strategy == "custom":
        if not custom_fields:
            msg = "[ERROR] Validation Failed: Custom fields must be provided for custom strategy"
            print(msg)
            raise ValueError(msg)
        custom_set = set(custom_fields)
        missing_custom = custom_set - cols_set
        if missing_custom:
            msg = f"[ERROR] Validation Failed: Missing custom filter fields in input columns: {missing_custom}"
            print(msg)
            raise ValueError(msg)
        else:
            print(f"[INFO] Custom Filters Present: {custom_set}")
    else:
        msg = f"[ERROR] Validation Failed: Unknown filter strategy '{strategy}'"
        print(msg)
        raise ValueError(msg)

    print("[SUCCESS] Validation Passed: All required filters are present.")
    return True