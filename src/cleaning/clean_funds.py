import pandas as pd
import numpy as np

# Load Data

file_path = r"data/raw/groww_fund_dashboard_data.xlsx"

df = pd.read_excel(file_path)

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

# Standardize columns

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Remove duplicates

before = len(df)

df = df.drop_duplicates()

after = len(df)

print("\nDuplicates removed:", before - after)

# Missing values

print("\nMissing values:")
print(df.isnull().sum())

# Fix invalid launch dates

if 'launch_date' in df.columns:

    # Convert launch_date to proper datetime
    df['launch_date'] = pd.to_datetime(
        df['launch_date'],
        errors='coerce'
    )

    # Detect dates before 1950
    invalid_launch_date = (
        df['launch_date'].dt.year < 1950
    )

    print(
        "\nInvalid launch dates:",
        invalid_launch_date.sum()
    )

    # Treat invalid dates as missing
    df.loc[
        invalid_launch_date,
        'launch_date'
    ] = pd.NaT

    # Recalculate launch year
    df['launch_year'] = df['launch_date'].dt.year

# Negative values

if 'nav' in df.columns:

    print(
        "\nNegative NAV:",
        len(df[df['nav'] < 0])
    )

if 'aum_cr' in df.columns:

    print(
        "\nNegative AUM:",
        len(df[df['aum_cr'] < 0])
    )

# Fund Age

CURRENT_YEAR = 2026

if 'launch_year' in df.columns:

    df['fund_age'] = (
        CURRENT_YEAR
        - df['launch_year']
    )

    # Unknown launch date = unknown fund age
    df.loc[
        df['launch_year'].isna(),
        'fund_age'
    ] = np.nan

# AUM Rank

if 'aum_cr' in df.columns:

    df['aum_rank'] = (
        df['aum_cr']
        .rank(
            ascending=False,
            method='dense'
        )
    )

# NAV Percentile

if 'nav' in df.columns:

    df['nav_percentile'] = (
        df['nav']
        .rank(pct=True) * 100
    )

# Save

output = "data/processed/funds_clean.csv"

df.to_csv(
    output,
    index=False
)

print("\nSaved:")
print(output)
