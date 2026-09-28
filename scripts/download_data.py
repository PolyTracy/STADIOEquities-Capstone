"""
Fallback downloader for the public UCI Bank Marketing dataset.

The dataset is already committed under data/external/bank-additional-full.csv.
Run this only if you need to re-fetch it from source:

    python scripts/download_data.py

Source: UCI Machine Learning Repository (ID 222), Bank Marketing.
Moro, S., Rita, P. and Cortez, P. (2014) 'Bank Marketing', UCI Machine
Learning Repository. https://doi.org/10.24432/C5K306
"""
import io
import zipfile
import urllib.request
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"
DEST = Path(__file__).resolve().parents[1] / "data" / "external"
TARGET = "bank-additional/bank-additional-full.csv"


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    print("Downloading:", URL)
    raw = urllib.request.urlopen(URL).read()
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        inner = outer.read("bank-additional.zip")
    with zipfile.ZipFile(io.BytesIO(inner)) as z:
        csv_bytes = z.read(TARGET)
    out = DEST / "bank-additional-full.csv"
    out.write_bytes(csv_bytes)
    print("Saved:", out, f"({out.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
