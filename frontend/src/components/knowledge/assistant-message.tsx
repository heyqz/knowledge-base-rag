import type { AssistantMessage as AssistantMessageType } from "@/types/message";

import { MarkdownRenderer } from "@/components/markdown/markdown-renderer";

import { SourceList } from "./source-list";
import { Skeleton } from "@/components/ui/skeleton";

type AssistantMessageProps = Pick<
  AssistantMessageType,
  "content" | "status" | "sources"
>;

export function AssistantMessage({
  content,
  sources,
  status,
}: AssistantMessageProps) {
  return (
    <div className="space-y-6">
      <div className="rounded-xl border p-6">
        {status === "loading" && content.length === 0 ? (
          <div className="space-y-3">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        ) : (
          <MarkdownRenderer>{content}</MarkdownRenderer>
        )}
      </div>

      {status === "completed" && sources.length > 0 && (
        <div>
          <h3 className="mb-4 text-lg font-semibold">Sources</h3>

          <SourceList sources={sources} />
        </div>
      )}
    </div>
  );
}
