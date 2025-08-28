import csv
import json
import re

# --- PII detection regex ---
phone_pattern = re.compile(r"\b(\d{10})\b")
aadhaar_pattern = re.compile(r"\b\d{4}\s\d{4}\s\d{4}\b")
passport_pattern = re.compile(r"\b[A-Z][0-9]{7}\b")
upi_pattern = re.compile(r"\b[\w.\-]+@[\w]+\b")
email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def mask_phone(phone: str) -> str:
    return phone[:2] + "XXXXXX" + phone[-2:]


def mask_name(name: str) -> str:
    # Mask each word keeping first letter + rest as X
    return " ".join([w[0] + "X" * (len(w) - 1) for w in name.split()])


def redact_json(record: dict) -> tuple[dict, bool]:
    is_pii = False
    redacted = {}

    for key, value in record.items():
        if isinstance(value, str):
            if phone_pattern.fullmatch(value):
                redacted[key] = mask_phone(value)
                is_pii = True
            elif aadhaar_pattern.fullmatch(value):
                redacted[key] = "[REDACTED_AADHAAR]"
                is_pii = True
            elif passport_pattern.fullmatch(value):
                redacted[key] = "[REDACTED_PASSPORT]"
                is_pii = True
            elif upi_pattern.fullmatch(value):
                redacted[key] = "[REDACTED_UPI]"
                is_pii = True
            elif email_pattern.fullmatch(value):
                parts = value.split("@")
                redacted[key] = parts[0][:2] + "XXX@" + parts[1]
                is_pii = True
            elif key.lower() == "name":
                redacted[key] = mask_name(value)
                is_pii = True
            else:
                redacted[key] = value
        else:
            redacted[key] = value

    return redacted, is_pii


def process_csv(input_file: str, output_file: str):
    with open(input_file, newline="", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ["record_id", "redacted_data_json", "is_pii"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        preview_count = 0

        for row in reader:
            record_id = row["record_id"]
            try:
                record = json.loads(row["data_json"].replace("'", '"'))
            except json.JSONDecodeError:
                record = {"_data": row["data_json"]}

            redacted_record, is_pii = redact_json(record)

            writer.writerow({
                "record_id": record_id,
                "redacted_data_json": json.dumps(redacted_record),
                "is_pii": str(is_pii)
            })

            # Show first 5 rows as preview
            if preview_count < 5:
                print(f"Input: {record}")
                print(f"Redacted: {redacted_record}, PII: {is_pii}")
                print("-" * 50)
                preview_count += 1


if __name__ == "__main__":
    process_csv("iscp_pii_dataset.csv", "redacted_output_shivam_raj.csv")
