import { useChat } from "@/hooks/use-chat";
import { ChatInput } from "../chat/chat-input";

import { AnswerHeader } from "./answer-header";
import { AnswerContent } from "./answer-content";
import { AnswerEmpty } from "./answer-empty";
import { AnswerLoading } from "./answer-loading";

export function AnswerPanel() {
  const chat = useChat();
  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-y-auto p-10">
        <div className="mx-auto max-w-4xl">
          <AnswerHeader />
          {chat.isPending && <AnswerLoading />}
          {!chat.isPending && !chat.data && <AnswerEmpty />}
          {chat.data && <AnswerContent response={chat.data} />}
        </div>
      </div>
      <ChatInput chat={chat} />
    </div>
  );
}
