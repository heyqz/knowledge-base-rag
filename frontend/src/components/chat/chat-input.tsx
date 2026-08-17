import { useState } from "react";
import type { UseMutationResult } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import type { ChatRequest, ChatResponse } from "@/types/chat";

type ChatInputProps = {
  chat: UseMutationResult<ChatResponse, Error, ChatRequest>;
};

export function ChatInput({ chat }: ChatInputProps) {
  const [question, setQuestion] = useState("");

  function handleSend() {
    if (!question.trim()) return;

    chat.mutate({
      question,
    });
    setQuestion("");
  }

  return (
    <div className="border-t bg-background p-6">
      <div className="mx-auto flex max-w-4xl gap-3">
        <Input
          className="h-12"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={
            chat.isPending ? "Generating answer..." : "Ask anything..."
          }
        />

        <Button
          className="h-12 px-6"
          onClick={handleSend}
          disabled={chat.isPending}
        >
          {chat.isPending ? "Think..." : "Send"}
        </Button>
      </div>
    </div>
  );
}
