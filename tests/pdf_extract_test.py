from unittest.mock import MagicMock, patch

import pytest

from tools.pdf_extract import register

DEFAULT_PROMPT = (
    "Extract and transcribe all text and describe any diagrams on this page."
)


@pytest.fixture()
def registered_tools():
    tools = {}
    mcp = MagicMock()
    mcp.tool.side_effect = lambda: (lambda fn: tools.setdefault(fn.__name__, fn))
    register(mcp)
    return tools


def test_extract_pdf_text_joins_pages(registered_tools):
    extract_pdf_text = registered_tools["extract_pdf_text"]
    page1, page2 = MagicMock(), MagicMock()
    page1.get_text.return_value = "hello"
    page2.get_text.return_value = "world"
    doc = MagicMock()
    doc.__iter__.return_value = [page1, page2]

    with patch("tools.pdf_extract.pymupdf.open", return_value=doc) as mock_open:
        result = extract_pdf_text("/tmp/sample.pdf")

    assert result == "hello\nworld"
    mock_open.assert_called_once_with("/tmp/sample.pdf")
    doc.close.assert_called_once()


def test_extract_pdf_text_scanned_fallback(registered_tools):
    extract_pdf_text = registered_tools["extract_pdf_text"]
    page = MagicMock()
    page.get_text.return_value = "   \n  "
    doc = MagicMock()
    doc.__iter__.return_value = [page]

    with patch("tools.pdf_extract.pymupdf.open", return_value=doc):
        result = extract_pdf_text("/tmp/scan.pdf")

    assert result.startswith("No extractable text found")
    doc.close.assert_called_once()


def test_vision_success(registered_tools):
    extract_pdf_via_vision = registered_tools["extract_pdf_via_vision"]
    doc = MagicMock()
    doc.__len__.return_value = 1
    page = doc.__getitem__.return_value
    pix = page.get_pixmap.return_value

    with (
        patch("tools.pdf_extract.pymupdf.open", return_value=doc),
        patch(
            "tools.pdf_extract.describe_image", return_value="VISION TEXT"
        ) as mock_describe,
    ):
        result = extract_pdf_via_vision("/tmp/scan.pdf")

    assert result == "VISION TEXT"
    page.get_pixmap.assert_called_once_with(dpi=150)
    pix.save.assert_called_once_with("/tmp/pdf_page_0.png")
    doc.close.assert_called_once()
    mock_describe.assert_called_once_with("/tmp/pdf_page_0.png", prompt=DEFAULT_PROMPT)


def test_vision_custom_prompt_and_page(registered_tools):
    extract_pdf_via_vision = registered_tools["extract_pdf_via_vision"]
    doc = MagicMock()
    doc.__len__.return_value = 5
    pix = doc.__getitem__.return_value.get_pixmap.return_value

    with (
        patch("tools.pdf_extract.pymupdf.open", return_value=doc),
        patch("tools.pdf_extract.describe_image", return_value="ok") as mock_describe,
    ):
        result = extract_pdf_via_vision(
            "/tmp/scan.pdf", page=2, prompt="Extract this table as markdown"
        )

    assert result == "ok"
    doc.__getitem__.assert_called_once_with(2)
    doc.__getitem__.return_value.get_pixmap.assert_called_once_with(dpi=150)
    pix.save.assert_called_once_with("/tmp/pdf_page_2.png")
    mock_describe.assert_called_once_with(
        "/tmp/pdf_page_2.png", prompt="Extract this table as markdown"
    )


def test_vision_out_of_range_no_crash(registered_tools):
    extract_pdf_via_vision = registered_tools["extract_pdf_via_vision"]
    doc = MagicMock()
    doc.__len__.return_value = 3

    def _simulate_closed_doc():
        doc.__len__.side_effect = ValueError("document closed")

    doc.close.side_effect = _simulate_closed_doc

    with (
        patch("tools.pdf_extract.pymupdf.open", return_value=doc),
        patch("tools.pdf_extract.describe_image") as mock_describe,
    ):
        result = extract_pdf_via_vision("/tmp/scan.pdf", page=5)

    assert result == "Page 5 out of range. PDF has 3 pages."
    doc.close.assert_called_once()
    mock_describe.assert_not_called()


def test_pdf_page_count(registered_tools):
    pdf_page_count = registered_tools["pdf_page_count"]
    doc = MagicMock()
    doc.__len__.return_value = 4

    with patch("tools.pdf_extract.pymupdf.open", return_value=doc):
        result = pdf_page_count("/tmp/doc.pdf")

    assert result == "4 pages"
    doc.close.assert_called_once()


def test_register_exposes_three_tools():
    tools = {}
    mcp = MagicMock()
    mcp.tool.side_effect = lambda: (lambda fn: tools.setdefault(fn.__name__, fn))

    register(mcp)

    assert mcp.tool.call_count == 3
    assert set(tools) == {
        "extract_pdf_text",
        "extract_pdf_via_vision",
        "pdf_page_count",
    }
