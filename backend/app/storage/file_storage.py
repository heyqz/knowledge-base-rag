from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.models.file import SavedFile

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class FileStorage:
    def save(self, file: UploadFile) -> SavedFile:
        suffix = Path(file.filename).suffix
        filename = f"{uuid4()}{suffix}"
        destination = UPLOAD_DIR / filename
        with open(destination, "wb") as f:
            f.write(file.file.read())
       
        return SavedFile(
            filename=filename,
            file_path=str(destination),
            file_size=destination.stat().st_size,
        )
        
    def delete(self, file_path: str):
        path = Path(file_path)
        if path.exists():
            path.unlink()
            
    def exists(self, file_path: str) -> bool:
        return Path(file_path).exists()
    
file_storage = FileStorage()