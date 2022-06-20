# Read pdf.

from pathlib import Path

from PyPDF2 import PdfReader


def read():
    pdf = Path('source/1110210.pdf')
    reader = PdfReader(pdf)
    for page in reader.pages:
        text = page.extract_text()
        print(text)


if __name__ == '__main__':
    read()
