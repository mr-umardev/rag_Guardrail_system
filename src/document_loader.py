import os
import docx
import pdfplumber

from config import DATA_FOLDER


def load_documents():

    folder = DATA_FOLDER
    docs = []

    if not os.path.exists(folder):

        raise Exception(f"Document folder not found: {folder}")

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if file.endswith(".txt"):

            with open(path, "r", encoding="utf-8") as f:

                text = f.read().strip()

                if text:
                    docs.append(text)

        elif file.endswith(".docx"):

            document = docx.Document(path)

            text = "\n".join([p.text for p in document.paragraphs]).strip()

            if text:
                docs.append(text)

        elif file.endswith(".pdf"):

            text = ""

            with pdfplumber.open(path) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

            text = text.strip()

            if text:
                docs.append(text)

    return docs


def chunk_documents(docs, chunk_size=500):

    chunks = []

    for doc in docs:

        words = doc.split()

        if len(words) == 0:
            continue

        for i in range(0, len(words), chunk_size):

            chunk = " ".join(words[i:i + chunk_size])

            chunks.append(chunk)

    return chunks