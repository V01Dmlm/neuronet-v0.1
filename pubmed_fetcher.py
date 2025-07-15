from Bio import Entrez

Entrez.email = "bodeegamer47@gmail.com"  # Change this to yours

def fetch_top_abstract(query):
    try:
        search_handle = Entrez.esearch(db="pubmed", term=query, retmax=1)
        search_results = Entrez.read(search_handle)
        search_handle.close()

        if not search_results["IdList"]:
            return None

        pmid = search_results["IdList"][0]

        fetch_handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
        abstract = fetch_handle.read()
        fetch_handle.close()

        return abstract.strip()
    except Exception as e:
        print(f"[PubMed Error] {e}")
        return None
