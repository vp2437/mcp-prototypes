import os
import pdfplumber
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PDF Server")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@mcp.tool()
def server_directory():
    """
    Return the directory containing server.py.
    Useful for debugging file path issues.
    """
    return BASE_DIR


@mcp.tool()
def list_pdf_files():
    """
    List all PDF files located beside server.py.
    Use this tool to discover available PDF documents before reading one.
    """
    return [f for f in os.listdir(BASE_DIR) if f.lower().endswith(".pdf")]


@mcp.tool()
def read_pdf(file_path: str) -> str:
    """
    Extract all readable text from a PDF document.

    Use this tool when a user wants to:
    - read a PDF
    - summarize a PDF
    - inspect document contents
    - search document text
    - read a specific page

    Args:
        file_path: PDF filename such as "report.pdf".

    Returns:
        Extracted text grouped by page.
    """
    full_path = os.path.join(BASE_DIR, file_path)

    with pdfplumber.open(full_path) as pdf:
        pages = []
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                pages.append(f"--- Page {i+1} ---\n{text}")
    return "\n\n".join(pages) if pages else "No text found in PDF."

@mcp.tool()
def read_pdf_tables(file_path: str) -> str:
    """
    Extract all tables from a PDF document.

    Use this tool when a user wants data contained in PDF tables.

    Args:
        file_path: PDF filename.

    Returns:
        Tables formatted as tab-separated text.
    """
    full_path = os.path.join(BASE_DIR, file_path)

    with pdfplumber.open(full_path) as pdf:
        all_tables = []
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for j, table in enumerate(tables):
                all_tables.append(f"--- Page {i+1}, Table {j+1} ---")
                for row in table:
                    all_tables.append("\t".join(str(c) if c else "" for c in row))
    return "\n".join(all_tables) if all_tables else "No tables found."

@mcp.tool()
def pdf_metadata(file_path: str) -> str:
    """
    Retrieve metadata from a PDF document.

    Metadata may include:
    - title
    - author
    - creator
    - producer
    - page count

    Args:
        file_path: PDF filename.

    Returns:
        Metadata as text.
    """
    full_path = os.path.join(BASE_DIR, file_path)

    with pdfplumber.open(full_path) as pdf:
        meta = pdf.metadata or {}
        meta["page_count"] = len(pdf.pages)
    return "\n".join(f"{k}: {v}" for k, v in meta.items())

if __name__ == "__main__":
    mcp.run(transport="stdio")