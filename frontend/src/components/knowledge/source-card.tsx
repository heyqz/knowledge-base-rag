import { Card, CardContent } from "@/components/ui/card";
import type { Source } from "@/types/source";

type SourceCardProps = {
  source: Source;
};

export function SourceCard({ source }: SourceCardProps) {
  return (
    <Card className="transition-colors hover:bg-muted">
      <CardContent className="flex items-center gap-2 px-3 py-2">
        📄
        <span className="min-w-0 flex-1 truncate text-xs font-medium">
          {source.filename}
        </span>
        <span className="shrink-0 text-xs text-muted-foreground">
          Page {source.page + 1}
        </span>
      </CardContent>
    </Card>
  );
}
