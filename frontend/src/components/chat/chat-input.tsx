import { useState } from "react";
import type { UseMutationResult } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import type { ChatRequest, ChatResponse } from "@/types/chat";
import { streamMessage } from "@/services/chat";

type ChatInputProps = {
  onQuestionSubmit: (quesiont: string) => void;
};

export function ChatInput({ onQuestionSubmit }: ChatInputProps) {
  const [question, setQuestion] = useState("");

  async function handleSend() {
    if (!question.trim()) return;

    onQuestionSubmit(question);

    setQuestion("");
  }

  return (
    <div className="border-t bg-background p-6">
      <div className="mx-auto flex max-w-4xl gap-3">
        <Input
          className="h-12"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={"Generating answer..."}
        />

        <Button
          className="h-12 px-6"
          onClick={handleSend}
        >
          Send
        </Button>
      </div>
    </div>
  );
}
