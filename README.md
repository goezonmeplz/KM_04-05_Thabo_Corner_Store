# Thabo's Corner Store — Sales Insights System (Starter Code)

## Folder structure

```
starter_code/
├── README.md              <- This file
├── requirements.txt       <- Python packages you need
├── main.py                <- entry point; runs the entire pipeline.
├── data_cleaning.py       <- Task 2: load & clean the raw CSVs
├── database.py            <- Task 3: build the SQLite database + SQL queries
├── analysis.py            <- Task 4: functions/loops/conditionals for insights
├── visualize.py           <- Task 5: charts with matplotlib
└── security.py            <- Task 6: simple login / password hashing
```

## Setting up the project

1. Make sure Python 3.10+ is installed: `python3 --version`
2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the `data/` folder (provided separately) so it sits **next to**
   `starter_code/`, like this:
   ```
   project/
   ├── data/
   │   ├── products.csv
   │   └── sales.csv
   └── starter_code/
       └── ... (these files)
   ```

## Running the proejct

Once Python is set up and all dependencies are installed:

```bash
python main.py
```
### Findings

## data_cleaning.py
# Missing unit_price
A sale record without a price severely limits any calculation that is to be performed based on selling prices in the data set(totals, fees, profit / loss...) thus, remove all records with a missing unit_price.

# Missing product_name
Drop rows with missing a missing product_name, this is not usable data.

# Inconsistent category capitalization
Capitalize every row's category starting letter.

# Inconsistent Date Formats
Standardize them to a single format (YYYY-MM-DD)

#Duplicate rows
Drop them.

# Data cleaning summary
products: 16 raw rows -> 12 clean rows (4 removed)
sales: 71 raw rows -> 43 clean rows (28 removed)

## security.py

#Refleciton

1. Confidentiality - The login gate helps keep sales reports from being viewed by unauthorized users. It checks a password before granting access, and storing a hash instead of the plain-text password avoids keeping the original password directly in the code. This is a basic protection, not a guarantee against every kind of access.

2. Integrity - The login gate does not prevent data from being changed or corrupted. In database.py, primary keys help ensure each record has a unique identifier, while suitable data types help prevent invalid values.

3. Availability - If the laptop is lost, damaged, stolen, or its files are accidentally deleted, the project and its reports may become unavailable. Regular backups stored somewhere separate from the laptop, such as an external drive or a cloud backup can reduce that risk.
