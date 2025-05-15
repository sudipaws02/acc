import pandas as pd
from datetime import datetime
import os

def read_input_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def generate_output_filename(prefix="ea_output", output_dir="output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(output_dir, f"{prefix}_{timestamp}.csv")
