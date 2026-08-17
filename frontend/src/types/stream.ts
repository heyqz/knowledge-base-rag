import type { Source } from "@/types/chat";

export interface StreamCallbacks {
  onToken: (token: string) => void;
  onDone: (sources: Source[]) => void;
}
