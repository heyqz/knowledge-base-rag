from datetime import datetime

from app.models.document import Document
from app.storage.database import db


class DocumentRepository:
    def __init__(self):
        self._create_table()

    def _create_table(self):
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                status TEXT NOT NULL,
                uploaded_at TEXT NOT NULL
            )
            """
        )

    def create(self, document: Document) -> Document:
        db.execute(
            """
            INSERT INTO documents (id, filename, original_filename, file_path, file_size, status, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                document.id,
                document.filename,
                document.original_filename,
                document.file_path,
                document.file_size,
                document.status,
                datetime.now().isoformat(),
            ),
        )
        return document

    def get_by_id(self, document_id: str) -> Document | None:
        row = db.execute(
            "SELECT * FROM documents WHERE id = ?", (document_id,)
        ).fetchone()
        if row:
            return Document(
                id=row["id"],
                filename=row["filename"],
                original_filename=row["original_filename"],
                file_path=row["file_path"],
                file_size=row["file_size"],
                status=row["status"],
                uploaded_at=datetime.fromisoformat(row["uploaded_at"]),
            )
        return None

    def list_all(self) -> list[Document]:
        rows = db.execute(
            "SELECT * FROM documents ORDER BY uploaded_at DESC"
        ).fetchall()

        documents = []

        for row in rows:
            documents.append(
                Document(
                    id=row["id"],
                    filename=row["filename"],
                    original_filename=row["original_filename"],
                    file_path=row["file_path"],
                    file_size=row["file_size"],
                    status=row["status"],
                    uploaded_at=datetime.fromisoformat(row["uploaded_at"]),
                )
            )

        return documents

    def delete(self, document_id: str):
        db.execute(
            "DELETE FROM documents WHERE id = ?",
            (document_id,),
        )


document_repository = DocumentRepository()
