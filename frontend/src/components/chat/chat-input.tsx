import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

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
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        <Button className="h-12 px-6" onClick={handleSend}>
          Send
        </Button>
      </div>
    </div>
  );
}
