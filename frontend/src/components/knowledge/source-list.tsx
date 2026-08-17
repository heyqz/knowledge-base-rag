import { SourceCard } from "./source-card";
import type { Source } from "@/types/chat";

type SourceListPorps = {
  sources: Source[];
};

export function SourceList({ sources }: SourceListPorps) {
  return (
    <div className="space-y-3">
      {sources.map((source) => (
        <SourceCard key={`${source.filename}-${source.page}`} source={source} />
      ))}
    </div>
  );
}
