import fastf1
import pandas as pd
from pathlib import Path

# Setup cache
cache_dir = Path("cache")
cache_dir.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(cache_dir))

YEAR = 2024
GRAND_PRIX = "Silverstone"

print(f"Loading {YEAR} {GRAND_PRIX} Race...")

# More robust session loading
event = fastf1.get_event_schedule(YEAR).query(f"EventName == '{GRAND_PRIX}'")
if event.empty:
    # Fallback: try British GP name
    event = fastf1.get_event_schedule(YEAR).query("EventName.str.contains('British', case=False)")

session = fastf1.get_session(YEAR, GRAND_PRIX, 'R')
session.load()  # quiet=True reduces spam

results = session.results

# Build DataFrame with better formatting
df = pd.DataFrame({
    "driver_code": results["Abbreviation"],
    "driver_name": results["FullName"],
    "team": results["TeamName"],
    "grid_position": results["GridPosition"].astype("Int64"),      # nullable integer
    "finish_position": results["Position"].astype("Int64"),
    "race_time_status": results["Time"].astype(str)
})

# Clean race_time_status
df["race_time_status"] = results["Time"].astype(str)
mask = results["Time"].isna()
df.loc[mask, "race_time_status"] = results.loc[mask, "Status"]


# Optional: Better time formatting
def format_time(td):
    if pd.isna(td):
        return results["Status"].iloc[0] if not results["Status"].empty else "Unknown"
    # Convert to nice string like "1:22:27.059" or gap
    return str(td).split()[-1]  # removes '0 days '

# Apply if desired
# df["race_time_status"] = results["Time"].apply(format_time).fillna(results["Status"])

print(df)

# Export
df.to_csv("silverstone_2024_basic_results.csv", index=False)
df.to_json("silverstone_2024_basic_results.json", orient="records", indent=4)

print("\n✅ Files exported successfully!")
print(f"Total drivers: {len(df)}")
