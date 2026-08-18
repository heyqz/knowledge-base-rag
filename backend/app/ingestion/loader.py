# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_core.documents import Document

# class PDFLoader:

#     def load(self, pdf_path: str | Path):
#         loader = PyPDFLoader(pdf_path)
#         return loader.load()

# pdf_loader = PDFLoader()
from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image
from langchain_core.documents import Document


class PDFLoader:

    def __init__(
        self,
        ocr_language: str = "eng",
        ocr_dpi: int = 200,
    ):
        self.ocr_language = ocr_language
        self.ocr_dpi = ocr_dpi

    def load(self, pdf_path: str | Path) -> list[Document]:
        pdf_path = Path(pdf_path)
        pdf = pymupdf.open(str(pdf_path))

        documents = []

        total_pages = len(pdf)

        for page_number, page in enumerate(pdf):
            text = page.get_text().strip()

            if len(text) >= 100:
                print(f"Using native text for page {page_number + 1}")

            else:
                print(f"OCR page {page_number + 1}")

                pix = page.get_pixmap(
                    dpi=self.ocr_dpi,
                    colorspace=pymupdf.csRGB,
                    alpha=False,
                )

                ocr_dir = Path("storage/ocr")
                ocr_dir.mkdir(parents=True, exist_ok=True)

                image_path = ocr_dir / f"page-{page_number + 1}.png"
                pix.save(image_path)

                image = Image.open(image_path)

                text = pytesseract.image_to_string(
                    image,
                    lang=self.ocr_language,
                    config="--psm 11",
                ).strip()

                image.close()

                print(f"OCR extracted {len(text)} characters")

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(pdf_path),
                        "total_pages": total_pages,
                        "page": page_number,
                        "page_label": str(page_number + 1),
                    },
                )
            )

        pdf.close()

        return documents


pdf_loader = PDFLoader()