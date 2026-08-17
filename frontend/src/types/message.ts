import type { Source } from "./chat";

export type UserMessage = {
  id: string;
  role: "user";
  content: string;
  status: "completed";
};

export type AssistantMessage = {
  id: string;
  role: "assistant";
  content: string;
  status: "loading" | "completed";
  sources: Source[];
};

export type Message =
  | UserMessage
  | AssistantMessage;