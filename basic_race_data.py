import fastf1
import pandas as pd

# Enable FastF1 cache (creates a cache folder locally)
fastf1.Cache.enable_cache("cache")

YEAR = 2024
GRAND_PRIX = "Silverstone"   # British GP

print(f"Loading {YEAR} {GRAND_PRIX} Race...")

session = fastf1.get_session(YEAR, GRAND_PRIX, "R")
session.load()

results = session.results

df = pd.DataFrame({
    "driver_code": results["Abbreviation"],
    "driver_name": results["FullName"],
    "team": results["TeamName"],
    "grid_position": results["GridPosition"],
    "finish_position": results["Position"],
    "race_time_status": results["Time"].astype(str)
})

# Replace NaT with Status (DNF, DSQ, etc.)
df.loc[df["race_time_status"] == "NaT", "race_time_status"] = results["Status"]

print(df)

df.to_csv("silverstone_2024_basic_results.csv", index=False)
df.to_json(
    "silverstone_2024_basic_results.json",
    orient="records",
    indent=4
)

print("\nFiles exported successfully!")
