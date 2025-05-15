import yaml
import pandas as pd

def load_column_map(yaml_path: str) -> dict:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("column_mapping", {})

def map_columns(df: pd.DataFrame, column_map: dict) -> pd.DataFrame:
    """
    Renames columns in the input DataFrame using the provided column mapping.
    Input CSV columns → Standard Azure fields (from mapping file)
    """
    inverted_map = {v: k for k, v in column_map.items()}  # input_name -> standard_field
    rename_dict = {col: inverted_map[col] for col in df.columns if col in inverted_map}
    return df.rename(columns=rename_dict)
