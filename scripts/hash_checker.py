import hashlib
from pathlib import Path


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


if __name__ == "__main__":
    path = input("Enter file path: ").strip()

    file = Path(path)

    if not file.exists():
        print("Error: File not found.")
    elif not file.is_file():
        print("Error: Path is not a file.")
    else:
        file_hash = calculate_hash(file)

        print("\n=== SOCShield Hash Checker ===")
        print(f"File: {file}")
        print(f"SHA-256: {file_hash}")
        print("\nHash calculation complete.")