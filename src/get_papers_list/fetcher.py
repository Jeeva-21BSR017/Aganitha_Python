import requests
import xml.etree.ElementTree as ET
import re
from typing import List, Dict

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def fetch_pubmed_ids(query: str, retmax: int = 10) -> List[str]:
    params = {"db": "pubmed", "term": query, "retmax": str(retmax)}
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    return [id_elem.text for id_elem in root.findall(".//IdList/Id")]


def fetch_papers(ids: List[str]) -> List[Dict[str, str]]:
    if not ids:
        return []

    params = {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    root = ET.fromstring(response.text)

    papers = []
    for article in root.findall(".//PubmedArticle"):
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "No title"

        pub_date_elem = article.find(".//PubDate")
        year = pub_date_elem.findtext("Year") if pub_date_elem is not None else "Unknown"

        authors = []
        affiliations = []
        industry_authors = []
        emails_found = []

        for author in article.findall(".//Author"):
            last = author.findtext("LastName") or ""
            first = author.findtext("ForeName") or ""
            full_name = f"{first} {last}".strip()

            aff_elem = author.find(".//AffiliationInfo/Affiliation")
            aff_text = aff_elem.text if aff_elem is not None and aff_elem.text else ""

            # ✅ Improved email extraction (multiple emails from each affiliation)
            emails_in_aff = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", aff_text)
            emails_found.extend(emails_in_aff)

            aff_text_lower = aff_text.lower()
            if aff_text:
                affiliations.append(aff_text)
                # ✅ Heuristic: detect industry authors
                if not any(keyword in aff_text_lower for keyword in ["university", "institute", "college", "hospital"]):
                    industry_authors.append(full_name)

            if full_name:
                authors.append(full_name)

        if industry_authors:
            papers.append({
                "Title": title,
                "Publication Year": year,
                "Non-Academic Authors": ", ".join(industry_authors),
                "All Authors": ", ".join(authors),
                "Affiliations": "; ".join(affiliations),
                "Corresponding Email": emails_found[0] if emails_found else "Not found"
            })

    return papers
