import { useDocuments } from "@/hooks/use-documents";
import { DocumentCard } from "./document-card";
import { UploadButton } from "@/components/upload/upload-button";

export function Sidebar() {
  const { data, isLoading, error } = useDocuments();
  console.log(data);

  return (
    <aside className="flex h-full w-72 flex-col border-r bg-background">
      {/* Header */}
      <div className="border-b p-6">
        <h2 className="text-xl font-semibold">
          📂 Documents ({data?.documents?.length})
        </h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Your indexed documents
        </p>
      </div>
      {/* Body */}
      <div className="flex-1 overflow-y-auto p-4">
        {isLoading && (
          <p className="text-sm text-muted-foreground">Loading...</p>
        )}

        {error && (
          <p className="text-sm text-red-500">Failed to load documents.</p>
        )}

        <div className="space-y-3">
          {data?.documents?.map((document) => (
            <DocumentCard key={document.id} document={document} />
          ))}
        </div>
      </div>
      {/* Footer */}
      <div className="border-t p-4">
        <UploadButton />
      </div>
    </aside>
  );
}
