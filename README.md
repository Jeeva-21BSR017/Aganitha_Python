A command-line tool to fetch PubMed research papers with **industry (non-academic)** authors and export the results as a CSV file.

This tool uses NCBI's PubMed E-Utilities to:
- Search papers by keyword
- Fetch paper titles, authors, and affiliations
- Identify non-academic authors from companies (e.g., biotech/pharma)
- Extract email addresses (if available)
- Save results to CSV for analysis


## Features

- CLI-powered: Run from terminal with simple commands
- Filters only papers with **industry authors**
- Extracts author affiliations + email address (from XML)
- Exports clean CSV output
- Built with Poetry for reproducibility

## Code Organization:
    └── jeeva-21bsr017-aganitha_python/
       ├── covid_results.csv
       ├── industry_only.csv
       ├── industry_with_email.csv
       ├── papers.csv
       ├── pyproject.toml
       ├── .gitignore.txt
       └── src/
         └── get_papers_list/
           ├── cli.py
           └── fetcher.py

## How to Install and Run

- Python 3.9 or higher
- [Poetry](https://python-poetry.org/docs/)

### 🧩 Install dependencies:

```bash
poetry install
```

#To Run the CLI tool:
 - poetry run get-papers-list "covid vaccine" -f output.csv

## SCREENSHOTS

This screenshot shows Poetry successfully installing all dependencies and running the CLI tool:

![image](https://github.com/user-attachments/assets/95c9a27c-23be-4b5d-bb46-f14b58e3ef16)



The tool successfully fetched and filtered papers using the `"immunotherapy cancer"` and `"covid vaccine"` queries.  
You can see it:

- Saving the filtered results to `papers.csv`
- Printing the full paper metadata (title, year, authors, affiliations)

![image](https://github.com/user-attachments/assets/21fb6c36-382a-4dee-8913-6b81043e092b)


### 🧾 Sample CSV Output

This is how the exported data looks in `papers.csv` opened in Excel:
![image](https://github.com/user-attachments/assets/c12a281a-ea2d-4bc1-b448-2ccd6e61328f)

