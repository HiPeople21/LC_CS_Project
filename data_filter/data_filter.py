# Splits bigger CSV dataset into smaller, more manageable files
import csv

from pathlib import Path

from utils import BASE, generate_holiday_dates, parse_date, MISSING_DATA, MONTHS, YEARS
        
        

def filter_data() -> None:
    """
    Reads CSV files from "./data" and writes new files into "./output_data" with only the data required
    """
    for year in YEARS:
        folder_path = Path(f"{BASE}/output_data/{year}")
        # Creates folder is it doesn't exist
        if not folder_path.is_dir():
            folder_path.mkdir(parents=True, exist_ok=True)
        
        # Generates holiday dates for the year
        dates = generate_holiday_dates(year)
        months = {date.month for date in dates}
        
        # Converts dates into tuples for easier searching
        dates = [[date.year, date.month, date.day] for date in dates]
        
        files = [f"SCATS{MONTHS[month]}{year}.csv" for month in months]
        for file in files:
            path = BASE / f"data/{year}" / file
            if not path.is_file() and path not in MISSING_DATA:
                print(f"'{path}' does not exist")
                continue
            elif path in MISSING_DATA:
                continue
            
            # Reads data
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                headers = next(reader)
                output_file = BASE / f"output_data/{year}" / file
                
                # Writes data
                with open(output_file, "w", encoding="utf-8", newline='') as output_f:
                    writer = csv.writer(output_f)
                    writer.writerow(headers[1:] + ["Year", "Month", "Day", "Hour", "Minute", "Second"])
                    length = 0
                    for row in reader:
                        date = parse_date(row[0], year)
                        if date[:3] in dates:
                            # Removes the unneeded date column and replaces it with the separated fields
                            writer.writerow(row[1:] + date)
                            length += 1
                print(output_file, length)
            
            
def calculate_and_show_percentage() -> None:
    """
    Calculates and shows what percentage of rows were kept
    """
    for year in YEARS:
        # Generates holiday dates for the year
        dates = generate_holiday_dates(year)
        months = {date.month for date in dates}
        
        files = [f"SCATS{MONTHS[month]}{year}.csv" for month in months]
        for file in files:
            path = BASE / f"data/{year}" / file
            if not path.is_file() and path not in MISSING_DATA:
                print(f"'{path}' does not exist")
                continue
            elif path in MISSING_DATA:
                continue
            # Reads from file
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                headers = next(reader)
                total_rows = sum(1 for _ in reader)
                output_file = BASE / f"output_data/{year}" / file
                # Reads from corresponding file
                with open(output_file, "r", encoding="utf-8") as output_f:
                    reader2 = csv.reader(output_f)
                    headers = next(reader2)
                    kept_rows = sum(1 for _ in reader2)
                print(file, total_rows, kept_rows, kept_rows / total_rows)
        

if __name__ == '__main__':
    filter_data()
    calculate_and_show_percentage()
        
    with open(BASE / "info.txt", "r") as f:
        t = 0
        k = 0
        for i in f:
            name, total, kept = i.strip().split(" ")
            total = int(total)
            kept = int(kept)
            t += total
            k += kept
            print(name, total, kept, kept / total)
        print(t, k, k / t)