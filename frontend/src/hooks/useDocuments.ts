import { useEffect, useState } from "react";
import { listDocuments } from "../services/document";
import type { DocumentResponse } from "../types/document";

export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>();

  async function refresh() {
    setLoading(true);

    try {
      const result = await listDocuments();
      setDocuments(result.documents);
      setError(undefined);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  return {
    documents,
    loading,
    error,
    refresh,
  };
}