import type { StreamCallbacks } from "@/types/stream";
import type { ChatResponse, Source } from "@/types/chat";

export interface StreamEvent {
  token?: string;
  done?: boolean;
  sources?: Source[];
}

export function parseSSE(buffer: string, callbacks: StreamCallbacks): string {
  const rawEvents = buffer.split("\n\n");

  // 保留最后一个不完整的 event
  const remainingBuffer = rawEvents.pop() ?? "";

  for (const event of rawEvents) {
    if (!event.startsWith("data: ")) {
      continue;
    }

    try {
      const json: StreamEvent = JSON.parse(event.replace("data: ", ""));

      if (json.token) {
        console.log(json.token);
        callbacks.onToken(json.token);
      }

      if (json.done) {
        callbacks.onDone(json.sources ?? []);
      }
    } catch (error) {
      console.error("Failed to parse SSE event:", error);
    }
  }

  return remainingBuffer;
}
