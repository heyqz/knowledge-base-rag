import { FileText } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import type { Source } from "@/types/source";

type SourceCardProps = {
  source: Source;
};

export function SourceCard({ source }: SourceCardProps) {
  return (
    <Card className="cursor-pointer transition-colors hover:bg-muted">
      <CardContent className="flex items-center gap-3 p-4">
        <FileText className="h-4 w-4 text-muted-foreground" />

        <div className="flex flex-col">
          <span className="text-sm font-medium">{source.filename}</span>

          <span className="text-xs text-muted-foreground">
            Page {source.page}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
