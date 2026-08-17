import type { Message } from "@/types/message";

import { AssistantMessage } from "./assistant-message";
import { UserMessage } from "./user-message";

type ConversationProps = {
  messages: Message[];
};

export function Conversation({ messages }: ConversationProps) {
  return (
    <div className="space-y-8">
      {messages.map((message) => {
        if (message.role === "user") {
          return <UserMessage key={message.id} content={message.content} />;
        }

        return (
          <AssistantMessage
            key={message.id}
            content={message.content}
            sources={message.sources}
            status={message.status}
          />
        );
      })}
    </div>
  );
}
