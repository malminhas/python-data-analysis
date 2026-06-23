"""
Global Car Sales: Electric vs Non-Electric (2010-2025)
=======================================================

A CRAFT-structured analysis of new car sales by type (electric vs
non-electric), built from data published by Our World in Data
(source: International Energy Agency, Global EV Outlook 2025).

CRAFT = Collect -> Refine -> Analyse -> Fact-check -> Transform

Each stage below is written as a small set of functions so that the
whole pipeline can later be lifted, section by section, into separate
cells of a Jupyter notebook. Run this file directly to execute the
full pipeline end to end:

    python car_sales_craft.py

Expected input: car-sales.zip (or an already-extracted car-sales.csv)
in the same folder as this script.

Output: two PNG charts saved alongside this script.
"""

import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent
ZIP_PATH = DATA_DIR / "car-sales.zip"
CSV_NAME = "car-sales.csv"

# These rows represent regional/world aggregates rather than individual
# countries, and need to be treated separately in places.
AGGREGATE_ENTITIES = ["World", "Europe", "European Union (27)", "Rest of World"]


# =============================================================================
# 1. COLLECT
#    Bring the raw data together in one place.
# =============================================================================

def collect_data(zip_path: Path = ZIP_PATH, csv_name: str = CSV_NAME) -> pd.DataFrame:
    """Load car-sales.csv into a DataFrame, extracting it from the zip if needed."""
    csv_path = zip_path.parent / csv_name

    if not csv_path.exists():
        with zipfile.ZipFile(zip_path) as zf:
            zf.extract(csv_name, path=zip_path.parent)

    df = pd.read_csv(csv_path)

    print("COLLECT")
    print(f"  Loaded {len(df)} rows, {df.shape[1]} columns from {csv_name}")
    print(f"  Entities: {df['Entity'].nunique()}")
    print(f"  Year range: {df['Year'].min()}-{df['Year'].max()}")
    print(f"  Columns: {list(df.columns)}")
    print()

    return df


# =============================================================================
# 2. REFINE
#    Clean, standardise, and de-duplicate.
# =============================================================================

def refine_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardise the raw car sales data.

    Steps:
      - Rename columns to snake_case.
      - Flag rows that are regional/world aggregates rather than countries.
      - Fill missing country codes for aggregate regions.
      - Drop rows with negative car counts (data errors).
      - Drop rows with missing sales figures.
      - Add derived columns: total_cars and ev_share_pct.
      - Remove duplicate rows.
    """
    df = df.copy()

    df = df.rename(columns={
        "Electric cars": "electric_cars",
        "Non-electric cars": "non_electric_cars",
    })

    # Mark aggregate regions (World, Europe, etc.) vs individual countries
    df["is_aggregate"] = df["Entity"].isin(AGGREGATE_ENTITIES)

    # Aggregate regions have no ISO country code in the source data
    df["Code"] = df["Code"].fillna("AGG")

    # A handful of "Rest of World" rows have negative electric car counts
    # and missing non-electric figures - these look like data errors, so
    # drop them rather than guess at a value.
    n_before = len(df)
    invalid_mask = df["electric_cars"] < 0
    df = df[~invalid_mask]
    n_dropped_negative = n_before - len(df)

    # Drop any remaining rows with a missing sales figure
    n_before = len(df)
    df = df.dropna(subset=["non_electric_cars"])
    n_dropped_missing = n_before - len(df)

    # Tidy up types now that bad rows are gone
    df["electric_cars"] = df["electric_cars"].astype(int)
    df["non_electric_cars"] = df["non_electric_cars"].astype(int)
    df["Year"] = df["Year"].astype(int)

    # Derived columns used throughout the analysis
    df["total_cars"] = df["electric_cars"] + df["non_electric_cars"]
    df["ev_share_pct"] = (df["electric_cars"] / df["total_cars"] * 100).round(2)

    # De-duplicate (belt and braces - none expected in this dataset)
    n_before = len(df)
    df = df.drop_duplicates()
    n_dropped_dupes = n_before - len(df)

    df = df.reset_index(drop=True)

    print("REFINE")
    print(f"  Dropped {n_dropped_negative} row(s) with negative car counts")
    print(f"  Dropped {n_dropped_missing} row(s) with missing sales figures")
    print(f"  Dropped {n_dropped_dupes} duplicate row(s)")
    print(f"  {len(df)} rows remain after cleaning")
    print(f"  New columns added: total_cars, ev_share_pct, is_aggregate")
    print()

    return df


# =============================================================================
# 3. ANALYSE
#    Ask questions of the data.
# =============================================================================

def analyse_data(df: pd.DataFrame) -> dict:
    """Compute summary statistics and answer some headline questions.

    Returns a dictionary of results that downstream steps (fact-check,
    transform) can reuse.
    """
    world = df[df["Entity"] == "World"].sort_values("Year")
    latest_year = int(world["Year"].max())
    base_year = 2015

    world_latest = world.loc[world["Year"] == latest_year].iloc[0]
    world_base = world.loc[world["Year"] == base_year].iloc[0]

    ev_growth_multiple = world_latest["electric_cars"] / world_base["electric_cars"]

    # Top countries (excluding aggregates) by EV sales in the latest year
    countries_latest = df[(~df["is_aggregate"]) & (df["Year"] == latest_year)]
    top_countries = (
        countries_latest.sort_values("electric_cars", ascending=False)
        .head(5)[["Entity", "electric_cars", "ev_share_pct"]]
    )

    results = {
        "world_trend": world[["Year", "electric_cars", "non_electric_cars", "total_cars", "ev_share_pct"]],
        "latest_year": latest_year,
        "base_year": base_year,
        "world_latest_ev_share": world_latest["ev_share_pct"],
        "ev_growth_multiple": ev_growth_multiple,
        "top_countries_latest": top_countries,
    }

    print("ANALYSE")
    print(f"  In {latest_year}, electric cars made up {results['world_latest_ev_share']:.1f}% "
          f"of new car sales worldwide.")
    print(f"  World EV sales grew {ev_growth_multiple:.1f}x between {base_year} and {latest_year} "
          f"({int(world_base['electric_cars']):,} -> {int(world_latest['electric_cars']):,}).")
    print(f"  Top 5 countries by EV sales in {latest_year}:")
    print(top_countries.to_string(index=False))
    print()

    return results


# =============================================================================
# 4. FACT-CHECK
#    Verify figures against the source data before trusting them.
# =============================================================================

def fact_check(df: pd.DataFrame, results: dict, tolerance_pct: float = 5.0) -> bool:
    """Sanity-check the headline "World" figures against the underlying rows.

    The "World" row is itself a reported aggregate, not something we
    calculated - so we check it independently by summing electric car
    sales across every individual country plus the "Rest of World"
    catch-all, and comparing that total to the reported "World" figure.

    A small gap is expected (rounding, reporting lags, coverage
    differences), so we treat the check as passing if the two figures
    are within `tolerance_pct` percent of each other.
    """
    latest_year = results["latest_year"]
    year_data = df[df["Year"] == latest_year]

    reported_world = year_data.loc[df["Entity"] == "World", "electric_cars"].iloc[0]

    # Sum of every row that is NOT the World/Europe/EU aggregates
    # (countries + "Rest of World") should approximate the World total.
    bottom_up_total = year_data.loc[
        ~year_data["Entity"].isin(["World", "Europe", "European Union (27)"]),
        "electric_cars",
    ].sum()

    diff = abs(bottom_up_total - reported_world)
    pct_diff = diff / reported_world * 100
    passed = pct_diff <= tolerance_pct

    print("FACT-CHECK")
    print(f"  Year checked: {latest_year}")
    print(f"  Reported 'World' electric car sales:        {reported_world:>12,}")
    print(f"  Sum of countries + 'Rest of World':         {bottom_up_total:>12,}")
    print(f"  Difference:                                 {diff:>12,} ({pct_diff:.1f}%)")
    if passed:
        print(f"  PASS - within {tolerance_pct:.0f}% tolerance. The reported World total "
              f"is consistent with the underlying country-level data.")
    else:
        print(f"  FAIL - difference exceeds {tolerance_pct:.0f}% tolerance. "
              f"Investigate before using the 'World' figure in any report.")
    print()

    return passed


# =============================================================================
# 5. TRANSFORM
#    Convert results into the format needed: here, charts for a report.
# =============================================================================

def transform_to_charts(results: dict, output_dir: Path = DATA_DIR) -> list[Path]:
    """Create and save matplotlib charts summarising the analysis.

    Produces:
      1. world_ev_trend.png  - electric vs non-electric sales over time
      2. world_ev_share.png  - electric share of total sales over time
    """
    world_trend = results["world_trend"]
    saved_paths = []

    # --- Chart 1: Electric vs non-electric sales over time -----------------
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(world_trend["Year"], world_trend["electric_cars"], marker="o", label="Electric cars")
    ax.plot(world_trend["Year"], world_trend["non_electric_cars"], marker="o", label="Non-electric cars")
    ax.set_title("Global New Car Sales by Type, 2010-2025")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cars sold")
    ax.ticklabel_format(style="plain", axis="y")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()

    path1 = output_dir / "world_ev_trend.png"
    fig.savefig(path1, dpi=150)
    plt.close(fig)
    saved_paths.append(path1)

    # --- Chart 2: EV share of total sales over time -------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(world_trend["Year"], world_trend["ev_share_pct"], marker="o", color="green")
    ax.set_title("Electric Cars as a Share of New Car Sales (World)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Electric car share (%)")
    ax.grid(alpha=0.3)
    fig.tight_layout()

    path2 = output_dir / "world_ev_share.png"
    fig.savefig(path2, dpi=150)
    plt.close(fig)
    saved_paths.append(path2)

    print("TRANSFORM")
    for p in saved_paths:
        print(f"  Saved {p.name}")
    print()

    return saved_paths


# =============================================================================
# Run the full CRAFT pipeline
# =============================================================================

def main():
    raw = collect_data()
    clean = refine_data(raw)
    results = analyse_data(clean)
    fact_check(clean, results)
    transform_to_charts(results)


if __name__ == "__main__":
    main()
