from google import genai
import PyPDF2
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def ask_ai(document_text: str, question: str) -> str:
    prompt = f"""
    You are a document assistant.
    Read the document below and answer the question.
    Answer only based on the document content.
    If the answer is not in the document, say "I don't know".

    Document:
    {document_text}

    Question: {question}
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash-8b",
        contents=prompt
    )
    return response.text