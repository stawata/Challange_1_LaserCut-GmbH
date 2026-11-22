from pathlib import Path

import pandas as pd


ORDER_COLUMNS = ["customer_name", "customer_branch", "file_name", "order_quantity"]
CUSTOMER_NAME_CORRECTIONS = {
    "AutoPart AG": "AutoParts AG",
    "Metalform SA": "MetalForm SA",
}


def main():
    project_dir = Path(__file__).resolve().parent
    input_path = project_dir / "customers_sales.csv"
    output_path = project_dir / "customers_sales_cleaned.csv"

    sales = pd.read_csv(input_path, dtype=str, keep_default_na=False)
    missing_columns = [column for column in ORDER_COLUMNS if column not in sales]
    if missing_columns:
        raise ValueError(f"Missing columns in {input_path.name}: {', '.join(missing_columns)}")

    sales["customer_name"] = (
        sales["customer_name"].str.strip().replace(CUSTOMER_NAME_CORRECTIONS)
    )

    # Flag every row in a matching group because the CSV has no order IDs or dates.
    sales["possible_duplicate"] = sales.duplicated(subset=ORDER_COLUMNS, keep=False)

    sales.to_csv(output_path, index=False)
    print(f"Saved {len(sales)} rows to {output_path.name}.")
    print(f"Rows flagged as possible duplicates: {sales['possible_duplicate'].sum()}")


if __name__ == "__main__":
    main()