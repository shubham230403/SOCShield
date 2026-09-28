import re
from collections import Counter

FAILED_LOGIN_THRESHOLD = 5


def analyze_log(file_path):
    failed_logins = []
    source_ips = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            if "Failed password" in line or "authentication failure" in line:
                failed_logins.append(line.strip())

                ip_matches = re.findall(
                    r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                    line
                )

                source_ips.extend(ip_matches)

    ip_counts = Counter(source_ips)

    print("\n=== SOCShield Log Analysis ===")
    print(f"Failed authentication events: {len(failed_logins)}")

    if ip_counts:
        print("\nSource IP frequency:")

        for ip, count in ip_counts.most_common():
            print(f"{ip}: {count} attempts")

        print("\n=== Detection Results ===")

        suspicious_found = False

        for ip, count in ip_counts.items():
            if count >= FAILED_LOGIN_THRESHOLD:
                print(
                    f"[ALERT] Suspicious IP: {ip} "
                    f"({count} failed attempts)"
                )
                suspicious_found = True

        if not suspicious_found:
            print("No suspicious IPs detected.")

    else:
        print("\nNo source IPs detected.")

    print("\nAnalysis complete.")


if __name__ == "__main__":
    path = input("Enter log file path: ").strip()

    try:
        analyze_log(path)
    except FileNotFoundError:
        print("Error: Log file not found.")
    except Exception as error:
        print(f"Error: {error}")