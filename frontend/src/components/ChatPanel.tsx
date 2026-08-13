import { useState } from "react";

import { sendMessage } from "../services/chat";
import type { Message } from "../types/chat";

export default function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi! Ask me anything about your uploaded documents.",
    },
  ]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    const question = input.trim();

    if (!question || loading) {
      return;
    }

    // Add user message
    const userMessage: Message = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    setInput("");
    setLoading(true);

    try {
      const response = await sendMessage({
        question,
      });

      const assistantMessage: Message = {
        role: "assistant",
        content: response.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        padding: "24px",
      }}
    >
      {/* Messages */}

      <div
        style={{
          flex: 1,
          overflowY: "auto",
          marginBottom: "20px",
        }}
      >
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              marginBottom: "16px",
            }}
          >
            <strong>
              {message.role === "user" ? "You" : "AI"}
            </strong>

            <div>{message.content}</div>
          </div>
        ))}
          {loading && (
            <div
              style={{
                marginBottom: "16px",
              }}
            >
              <strong>AI</strong>

                <div style={{ fontStyle: "italic", color: "#666",}} >Thinking...
                </div>
            </div>
          )}
      </div>

      {/* Input */}

      <div
        style={{
          display: "flex",
          gap: "12px",
        }}
      >
        <input
          value={input}
          placeholder="Ask a question..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              handleSend();
            }
          }}
          style={{
            flex: 1,
            padding: "12px",
          }}
        />

        <button
          onClick={handleSend}
          disabled={loading}
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}