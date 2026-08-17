import { useMutation } from "@tanstack/react-query";

import { sendMessage } from "@/services/chat";

export function useChat() {
  return useMutation({
    mutationFn: sendMessage,
  });
}