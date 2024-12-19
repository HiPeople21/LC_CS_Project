# Splits bigger CSV dataset into smaller, more manageable files
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent

FILENAME = "Traffic_Flow_Data_Jan_to_June_2022_SDCC.csv"

with open(f"{BASE}/{FILENAME}", "r") as f:
    rows = f.readlines()
    
columns = rows[0]

zones = defaultdict(list)

for row in rows[1:]:
    zones[row.split(",")[0]].append(row)
    
folder_path = Path(f"{BASE}/zones_csvs")

if not folder_path.is_dir():
    folder_path.mkdir(parents=True, exist_ok=True)
s = 0
for zone, data in zones.items():
    with open(f"{folder_path}/{zone}.csv", "w") as f:
        text = columns + "".join(data)
        
        f.write(text)
    