import pymupdf
from mcp.server.mcpserver import MCPServer

# from lib.vision_client import describe_image
from lib.vision import describe_image


def register(mcp: MCPServer):
    @mcp.tool()
    def extract_pdf_text(file_path: str) -> str:
        """Extract raw text from a local PDF file. Use this first for text-based PDFs."""
        doc = pymupdf.open(file_path)
        text = "\n".join(page.get_text() for page in doc.pages())
        doc.close()
        if not text.strip():
            return "No extractable text found. This is likely a scanned/image PDF — use extract_pdf_via_vision instead."
        return text

    @mcp.tool()
    def extract_pdf_via_vision(
        file_path: str,
        page: int = 0,
        prompt: str = "Extract and transcribe all text and describe any diagrams on this page.",
    ) -> str:
        """
        Extract content from a scanned/image PDF page using a vision model.
        Use when extract_pdf_text returns no text.
        You can customize the prompt based on what you need — e.g.
        'Extract this table as markdown' or 'Describe the chart and its data points'.
        """
        doc = pymupdf.open(file_path)
        page_count = len(doc)
        if page >= page_count:
            doc.close()
            return f"Page {page} out of range. PDF has {page_count} pages."

        pix = doc[page].get_pixmap(dpi=150)
        img_path = f"/tmp/pdf_page_{page}.png"
        pix.save(img_path)
        doc.close()

        return describe_image(img_path, prompt=prompt)

    @mcp.tool()
    def pdf_page_count(file_path: str) -> str:
        """Get the total number of pages in a PDF."""
        doc = pymupdf.open(file_path)
        count = len(doc)
        doc.close()
        return f"{count} pages"
