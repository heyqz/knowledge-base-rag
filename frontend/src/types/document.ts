export type DocumentStatus = "indexed" | "uploaded";

export interface Document {
  id: string;
  filename: string;
  status: DocumentStatus;
  uploaded_at: string;
}

export interface DocumentListResponse {
  documents: Document[];
}
