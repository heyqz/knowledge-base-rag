import type { ChatResponse } from "@/types/chat";
import { MarkdownRenderer } from "@/components/markdown/markdown-renderer";

import { SourceList } from "./source-list";

type AnswerContentProps = {
  response: ChatResponse;
};

export function AnswerContent({ response }: AnswerContentProps) {
  return (
    <>
      <div className="mt-8 rounded-lg border p-6">
        <MarkdownRenderer>{response.answer}</MarkdownRenderer>
      </div>

      <div className="mt-8">
        <h3 className="mb-4 text-lg font-semibold">Sources</h3>

        <SourceList sources={response.sources} />
      </div>
    </>
  );
}
