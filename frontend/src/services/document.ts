import { apiFetch } from "./api";
import type {
  DocumentListResponse,
} from "../types/document";

export function listDocuments() {
  return apiFetch<DocumentListResponse>("/documents");
}

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  return apiFetch<DocumentListResponse>("/documents/upload", {
    method: "POST",
    body: formData,
  });
}