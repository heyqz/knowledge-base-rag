import { SourceCard } from "./source-card";
import type { Source } from "@/types/chat";

type SourceListProps = {
  sources: Source[];
};

export function SourceList({ sources }: SourceListProps) {
  const uniqueSources = Array.from(
    new Map(
      sources.map((source) => [`${source.filename}-${source.page}`, source]),
    ).values(),
  );

  return (
    <div className="space-y-3">
      {uniqueSources.map((source) => (
        <SourceCard key={`${source.filename}-${source.page}`} source={source} />
      ))}
    </div>
  );
}
