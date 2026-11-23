from pathlib import Path

import pandas as pd

sales = pd.read_csv(
    "customers_sales_cleaned.csv",
    dtype=str,
    keep_default_na=False,
)

required_columns = [
    "customer_name",
    "customer_branch",
    "file_name",
    "order_quantity",
    "possible_duplicate",
]

missing_columns = set(required_columns) - set(sales.columns)
if missing_columns:
    raise ValueError(f"Missing columns: {sorted(missing_columns)}")

# Check empty cells, including values containing only whitespace.
blank_cells = sales[required_columns].apply(
    lambda column: column.str.strip().eq("")
)

print("Sales rows:", len(sales))
print("\nBlank cells per column:")
print(blank_cells.sum())

# Report surrounding whitespace for review.
whitespace_cells = sales[required_columns].apply(
    lambda column: column.ne(column.str.strip())
)

print("\nCells with surrounding whitespace:")
print(whitespace_cells.sum())

# Check quantities without changing the original values yet.
quantity = pd.to_numeric(sales["order_quantity"], errors="coerce")
valid_quantity = (
    quantity.notna()
    & quantity.gt(0)
    & quantity.mod(1).eq(0)
)

print("\nRows with invalid quantities:")
print(sales.loc[~valid_quantity].to_string(index=False))

print("\nCustomer and branch combinations:")
print(
    sales.groupby(
        ["customer_name", "customer_branch"],
        dropna=False,
    ).size().rename("sales_rows").to_string()
)

repeated_files = sales["file_name"].duplicated(keep=False)

print("\nRows sharing a DXF filename:")
print(
    sales.loc[repeated_files]
    .sort_values("file_name")
    .to_string(index=False)
)

print("\nIdentical sales rows:")
print(
    sales.loc[sales.duplicated(keep=False)]
    .to_string(index=False)
)

# Inventory the drawings directly inside the DXF folder.
dxf_folder = Path("10991360")
drawings = pd.DataFrame(
    [
        {
            "file_name": path.name,
            "dxf_path": path.as_posix(),
        }
        for path in sorted(dxf_folder.iterdir())
        if path.is_file() and path.suffix.lower() == ".dxf"
    ],
    columns=["file_name", "dxf_path"],
)

missing_drawings = sorted(
    set(sales["file_name"]) - set(drawings["file_name"])
)
unused_drawings = sorted(
    set(drawings["file_name"]) - set(sales["file_name"])
)

print("\nDXF files:", len(drawings))
print("Distinct filenames in sales:", sales["file_name"].nunique())
print("Sales filenames without a drawing:", missing_drawings)
print("Drawings without a sales record:", unused_drawings)

if blank_cells.any().any():
    raise ValueError("Review the blank fields before exporting.")

if not valid_quantity.all():
    raise ValueError("Review the invalid quantities before exporting.")

if missing_drawings:
    raise ValueError("Review the unmatched sales filenames before exporting.")

# Multiple sales rows may reference the same drawing.
linked = sales.merge(
    drawings,
    on="file_name",
    how="left",
    validate="many_to_one",
)

linked["order_quantity"] = quantity.astype("int64")
linked.to_csv("sales_with_dxf.csv", index=False)

print(f"\nSaved sales_with_dxf.csv with {len(linked)} rows.")