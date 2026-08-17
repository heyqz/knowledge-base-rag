import { Skeleton } from "@/components/ui/skeleton";

export function AssistantLoading() {
  return (
    <div className="mt-8 space-y-8">
      {/* AI Answer */}
      <div className="rounded-lg border p-6">
        <div className="space-y-4">
          <Skeleton className="h-5 w-3/4" />
          <Skeleton className="h-5 w-full" />
          <Skeleton className="h-5 w-5/6" />
          <Skeleton className="h-5 w-2/3" />
        </div>
      </div>
      {/* Sources */}
      <div>
        <Skeleton className="mb-4 h-6 w-24" />

        <div className="space-y-3">
          <Skeleton className="h-16 rounded-lg" />
          <Skeleton className="h-16 rounded-lg" />
        </div>
      </div>
    </div>
  );
}
