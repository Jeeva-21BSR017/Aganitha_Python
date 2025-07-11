import pandas as pd

def save_to_excel(papers: list, filename: str = "results.xlsx"):
    if not papers:
        print("No papers to save.")
        return

    df = pd.DataFrame(papers)
    df.to_excel(filename, index=False)
    print(f"✅ Excel file saved as: {filename}")
