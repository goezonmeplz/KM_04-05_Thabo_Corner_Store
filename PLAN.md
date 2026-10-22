# Plan Before Coding

## Project goal

Build a small sales-insights system for Thabo’s Corner Store. It will clean the supplied product and sales data, store the cleaned records in a relational SQLite database, analyse sales with Python, create charts, and protect reports with a password check.

## Computational thinking

1) Decomposition - I will divide the work into data cleaning, database design and SQL queries, sales analysis, visualisation, security, and documentation. I will first inspect the starter code and CSV files so I understand the expected inputs and outputs before implementing each part.

2) Patterns - The raw files may contain missing fields, duplicate rows, inconsistent category capitalisation and date formats, and sales that refer to unknown product IDs. I will check which issues actually occur in the files, then apply consistent rules and record those decisions in the README.

3) Abstraction - I will focus the analysis on information useful to the shop, such as revenue by product or category and sales over time. I will treat customer type as optional context and avoid adding complexity that is not needed for the project.

4) Algorithms - I will inspect the data, clean and validate products and sales, resolve dates using one documented interpretation, save the cleaned data, create and populate the SQLite tables with primary and foreign keys, run and record at least five SQL queries, implement Python analysis, generate and describe two charts, add a SHA-256 password-hashing gate, and finish the README and end-to-end test.

## Module order

I will work through the modules in dependency order : data_cleaning.py, database.py, analysis.py, visualize.py, and security.py, then connect and test them through main.py. I will create the GitHub repository before programming and commit meaningful progress throughout, aiming for at least eight clear commits. I also will check that the project runs successfully, the required files are included, and the repository matches the submission ZIP.
