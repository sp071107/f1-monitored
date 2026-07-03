import fastf1
from fastf1.core import Session
import pandas as pd
from pathlib import Path
def get_race_info(YEAR, GRAND_PRIX):
    # Setup cache
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_dir))
    #
    print(f"Loading {YEAR} {GRAND_PRIX} Race...")
    # More robust session loading
    session: Session = fastf1.get_session(YEAR, GRAND_PRIX, 'R')
    session.load()  
    results = session.results
#Data frame=]
    df = pd.DataFrame({
        "driver_code": results["Abbreviation"],
        "driver_name": results["FullName"],
        "team": results["TeamName"],
        "grid_position": results["GridPosition"].astype("Int64"),      # nullable integer
        "finish_position": results["Position"].astype("Int64"),
        "race_time_status": results["Time"].astype(str)
    })
# Clean race_time_status
    mask = results["Time"].isna()
    df.loc[mask, "race_time_status"] = results.loc[mask, "Status"]
    #print(df)
    # you can print to check the value^^
    GRAND_PRIX = GRAND_PRIX.lower().replace(" ", "_")
# Export
    df.to_csv(f"{GRAND_PRIX}_{YEAR}_basic_results.csv", index=False)
    df.to_json(f"{GRAND_PRIX}_{YEAR}_basic_results.json", orient="records", indent=4)

    print("\n✅ Files exported successfully!")
    print(f"Total drivers: {len(df)}")
    return df
#def format_time(td):
    #if pd.isna(td):
        #return results["Status"].iloc[0] if not results["Status"].empty else "Unknown"
    # Convert to nice string like "1:22:27.059" or gap
    #return str(td).split()[-1]  # removes '0 days '
# df["race_time_status"] = results["Time"].apply(format_time).fillna(results["Status"])
if __name__=='__main__':
    get_race_info(2024,'Silverstone')

