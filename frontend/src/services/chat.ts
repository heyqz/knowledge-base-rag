import type { ChatRequest, ChatResponse } from "@/types/chat";
import { parseSSE } from "@/utils/sse";
import type { StreamCallbacks } from "@/types/stream";

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

export async function streamMessage(
  request: ChatRequest,
  callbacks: StreamCallbacks,
): Promise<void> {
  const response = await fetch(`${BASE_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Failed to stream response");
  }

  if (!response.body) {
    throw new Error("Response body is null");
  }

  const reader = response.body.getReader();

  const decoder = new TextDecoder();

  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();

    if (done) {
      break;
    }

    buffer += decoder.decode(value, { stream: true });
    buffer = parseSSE(buffer, callbacks);
  }
}
