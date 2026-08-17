import type { ChatRequest, ChatResponse } from "@/types/chat";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Failed to send message.");
  }

  return response.json();
}
