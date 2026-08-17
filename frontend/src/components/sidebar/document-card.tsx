import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Document } from "@/types/document";

type DocumentCardProps = {
  document: Document;
};

export function DocumentCard({ document }: DocumentCardProps) {
  return (
    <Card className="cursor-pointer transition-colors hover:bg-muted">
      <CardContent className="flex items-center gap-3 p-4">
        <div className="flex min-w-0 items-center gap-3">
          {/* <FileText className="h-4 w-4 text-muted-foreground" /> */}
          <span className="truncate text-sm font-medium">
            📋 {document.filename}
          </span>
        </div>
        <Badge
          variant={document.status === "indexed" ? "default" : "secondary"}
        >
          {document.status}
        </Badge>
      </CardContent>
    </Card>
  );
}
