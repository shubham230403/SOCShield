import re
from pathlib import Path


IP_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

DOMAIN_PATTERN = (
    r"\b(?:[a-zA-Z0-9-]+\.)+"
    r"[a-zA-Z]{2,}\b"
)

URL_PATTERN = r"https?://[^\s]+"

HASH_PATTERN = r"\b[a-fA-F0-9]{32,64}\b"


def extract_iocs(file_path):
    text = Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    ips = sorted(set(re.findall(IP_PATTERN, text)))
    domains = sorted(set(re.findall(DOMAIN_PATTERN, text)))
    urls = sorted(set(re.findall(URL_PATTERN, text)))
    hashes = sorted(set(re.findall(HASH_PATTERN, text)))

    print("\n=== SOCShield IOC Extractor ===")

    print("\n[IP Addresses]")
    for ip in ips:
        print(ip)

    print("\n[Domains]")
    for domain in domains:
        print(domain)

    print("\n[URLs]")
    for url in urls:
        print(url)

    print("\n[Hashes]")
    for file_hash in hashes:
        print(file_hash)

    print("\nIOC extraction complete.")


if __name__ == "__main__":
    path = input("Enter log/text file path: ").strip()

    file = Path(path)

    if not file.exists():
        print("Error: File not found.")
    elif not file.is_file():
        print("Error: Path is not a file.")
    else:
        extract_iocs(file)
        