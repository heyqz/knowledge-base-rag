import { useQuery } from "@tanstack/react-query";

import { getDocuments } from "@/services/document";
import { queryKeys } from "@/lib/query-keys";

export function useDocuments() {
  return useQuery({
    queryKey: queryKeys.documents,
    queryFn: getDocuments,
  });
}
