from pathlib import Path

import mammoth
from xhtml2pdf import pisa


def export_pdf(
    docx_path: str | Path,
    output_path: str | Path,
) -> None:
    """Generate an ordre de mission PDF file from a .docx document (via html conversion).

    Parameters
    ----------
    docx_path:
        Path to the `.docx` file to convert.
    output_path:
        Path where the generated document should be saved.
    """
    docx_path = Path(docx_path)
    output_path = Path(output_path)

    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w+b") as pdf_file:
        pisa.CreatePDF(result.value, dest=pdf_file)
