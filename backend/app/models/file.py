from pydantic import BaseModel

class SavedFile(BaseModel):
    filename: str
    file_path: str
    file_size: int
 