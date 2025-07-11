import argparse
import csv
from get_papers_list.fetcher import fetch_pubmed_ids, fetch_papers

def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with industry authors."
    )
    parser.add_argument("query", help="Search term for PubMed.")
    parser.add_argument("-f", "--file", dest="filename", help="Output CSV file.")
    parser.add_argument("--excel", action="store_true", help="Export results to Excel")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug logging.")
    args = parser.parse_args()

    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    ids = fetch_pubmed_ids(args.query)
    papers = fetch_papers(ids)

    if not papers:
        print("No papers found.")
        return

    if args.filename:
        # Save to CSV
        with open(args.filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=papers[0].keys())
            writer.writeheader()
            writer.writerows(papers)
        print(f"Saved {len(papers)} papers to {args.filename}")
    else:
        # Just print to terminal
        for paper in papers:
            print("== Paper ==")
            for key, value in paper.items():
                print(f"{key}: {value}")
            print()
    if args.excel:
        from get_papers_list.excel_exporter import save_to_excel
        save_to_excel(papers, "results.xlsx")
