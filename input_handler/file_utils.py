import pandas as pd
from datetime import datetime
import os

def read_input_csv(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    return pd.read_csv(file_path)


def generate_output_filename(billing_type: str, output_dir="output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    prefix = f"{billing_type.lower()}_output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(output_dir, f"{prefix}_{timestamp}.csv")
