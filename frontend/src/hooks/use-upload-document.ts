import { useMutation, useQueryClient } from "@tanstack/react-query";

import { uploadDocument } from "@/services/document";
import { queryKeys } from "@/lib/query-keys";

export function useUploadDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: uploadDocument,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.documents,
      });
    },
  });
}