import { ChatInput } from "../chat/chat-input";
import { Conversation } from "./conversation";

import { AnswerEmpty } from "./answer-empty";
import { useState } from "react";
import type { Message } from "@/types/message";
import { streamMessage } from "@/services/chat";

export function AnswerPanel() {
  const [messages, setMessages] = useState<Message[]>([]);

  async function handleQuestionSubmit(question: string) {
    const assistantId = crypto.randomUUID();

    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: "user",
        content: question,
        status: "completed",
      },
      {
        id: assistantId,
        role: "assistant",
        content: "",
        status: "loading",
        sources: [],
      },
    ]);

    await streamMessage(
      { question },
      {
        onToken: (token) => {
          setMessages((prev) =>
            prev.map((message) => {
              if (message.id !== assistantId) {
                return message;
              }

              return {
                ...message,
                content: message.content + token,
              };
            }),
          );
        },

        onDone: (sources) => {
          setMessages((prev) =>
            prev.map((message) => {
              if (message.id !== assistantId) {
                return message;
              }

              return {
                ...message,
                status: "completed",
                sources,
              };
            }),
          );
        },
      },
    );
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-y-auto p-10">
        <div className="mx-auto max-w-4xl">
          <h2 className="text-4xl font-bold">AI Knowledge Assistant</h2>

          {messages.length === 0 ? (
            <AnswerEmpty />
          ) : (
            <Conversation messages={messages} />
          )}
        </div>
      </div>
      <ChatInput onQuestionSubmit={handleQuestionSubmit} />
    </div>
  );
}
