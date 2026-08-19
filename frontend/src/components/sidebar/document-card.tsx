import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Document } from "@/types/document";
import { Trash2 } from "lucide-react";
import { useDeleteDocument } from "@/hooks/use-delete-document";

type DocumentCardProps = {
  document: Document;
};

export function DocumentCard({ document }: DocumentCardProps) {
  const deleteDocument = useDeleteDocument();
  const handleDelete = () => {
    deleteDocument.mutate(document.id);
  };

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
        <button
          type="button"
          onClick={handleDelete}
          disabled={deleteDocument.isPending}
          className="shrink-0 rounded-md p-1.5 text-muted-foreground hover:bg-destructive/10 hover:text-destructive disabled:opacity-50"
          aria-label={`Delete ${document.filename}`}
        >
          <Trash2 className="h-4 w-4" />
        </button>
      </CardContent>
    </Card>
  );
}
