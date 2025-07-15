import json
import time
from Bio import Entrez
from tqdm import tqdm
import re

# 📬 Required by NCBI Entrez API
Entrez.email = "bodeegamer47@gmail.com"
Entrez.tool = "neuronet-med-scraper"


def fetch_pubmed_ids(query, max_results):
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        return record.get("IdList", [])
    except Exception as e:
        print(f"❌ Failed to fetch PubMed IDs: {e}")
        return []


def fetch_abstract(pmid):
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
        abstract = handle.read().strip()
        handle.close()
        return abstract if is_valid_abstract(abstract) else None
    except Exception as e:
        print(f"❌ Error fetching {pmid}: {e}")
        return None


def is_valid_abstract(abstract):
    # Basic filtering
    if not abstract or len(abstract.split()) < 25:
        return False
    if "No abstract available" in abstract:
        return False
    return True


def clean_abstract(abstract):
    abstract = re.sub(r'\s+', ' ', abstract)
    abstract = abstract.replace("\n", " ").strip()
    return abstract


def generate_prompt_completion_pair(abstract, prompt_template="{abstract}"):
    prompt = prompt_template.replace("{abstract}", abstract.strip())
    return {
        "prompt": prompt,
        "completion": " "
    }


def generate_dataset(query="Cancer", max_results=100, output_file="neuronet_data.jsonl", prompt_template="{abstract}"):
    print(f"\n🔍 Searching PubMed for:\n   📌 Query: {query}\n   📈 Max Results: {max_results}")
    ids = fetch_pubmed_ids(query, max_results)
    print(f"🔗 Found {len(ids)} article IDs.")

    entries_saved = 0
    failed_count = 0

    with open(output_file, "w", encoding="utf-8") as f_out:
        for pmid in tqdm(ids, desc="📥 Downloading & processing abstracts"):
            abstract = fetch_abstract(pmid)
            if not abstract:
                failed_count += 1
                continue

            cleaned = clean_abstract(abstract)
            entry = generate_prompt_completion_pair(cleaned, prompt_template)
            f_out.write(json.dumps(entry, ensure_ascii=False) + "\n")
            entries_saved += 1
            time.sleep(0.34)  # Respect NCBI's rate limits

    print(f"\n✅ Done.\n   🧾 Entries saved: {entries_saved}\n   ❌ Failed/Skipped: {failed_count}")
    print(f"📁 Output file: {output_file}")


# ✅ CLI usage (safe for GUI importing)
if __name__ == "__main__":
    generate_dataset()
