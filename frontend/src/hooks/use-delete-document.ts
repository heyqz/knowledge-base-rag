import { useMutation, useQueryClient } from "@tanstack/react-query";

import { deleteDocument } from "@/services/document";
import { queryKeys } from "@/lib/query-keys";

export function useDeleteDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteDocument,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.documents,
      });
    },
  });
}
