
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import csv

def mock_fetch_pubmed_ids(query, retmax=10):
    return ["123456", "234567"]

def mock_fetch_papers(ids):
    return [
        {
            "Title": "COVID-19 Vaccine Study",
            "Publication Year": "2023",
            "Non-Academic Authors": "John Doe",
            "All Authors": "John Doe, Jane Smith",
            "Affiliations": "Pfizer Inc., New York",
            "Corresponding Email": "john.doe@pfizer.com"
        },
        {
            "Title": "Cancer Immunotherapy Breakthrough",
            "Publication Year": "2022",
            "Non-Academic Authors": "Alice Lee",
            "All Authors": "Alice Lee, Bob White",
            "Affiliations": "Moderna Biotech, Boston",
            "Corresponding Email": "alice.lee@moderna.com"
        }
    ]

root = Tk()
root.title("PubMed Industry Paper Fetcher")
root.geometry("900x500")

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Search Query:").grid(row=0, column=0, padx=5)
query_var = StringVar()
query_entry = Entry(frame, textvariable=query_var, width=50)
query_entry.grid(row=0, column=1, padx=5)

def fetch_and_display():
    query = query_var.get().strip()
    if not query:
        messagebox.showerror("Error", "Please enter a search query.")
        return

    ids = mock_fetch_pubmed_ids(query)
    results = mock_fetch_papers(ids)

    for row in tree.get_children():
        tree.delete(row)

    for paper in results:
        tree.insert("", END, values=(
            paper["Title"],
            paper["Publication Year"],
            paper["Non-Academic Authors"],
            paper["Corresponding Email"]
        ))

    global current_results
    current_results = results

Button(frame, text="Fetch Papers", command=fetch_and_display).grid(row=0, column=2, padx=5)

columns = ("Title", "Year", "Industry Authors", "Email")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)
tree.pack(pady=20, fill=BOTH, expand=True)

def save_to_csv():
    if not current_results:
        messagebox.showwarning("No data", "No results to save.")
        return

    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return

    with open(filepath, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=current_results[0].keys())
        writer.writeheader()
        writer.writerows(current_results)

    messagebox.showinfo("Saved", f"Results saved to {filepath}")

Button(root, text="Save Results as CSV", command=save_to_csv).pack(pady=10)

current_results = []
root.mainloop()
