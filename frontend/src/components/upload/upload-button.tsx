import { useRef } from "react";

import { Upload } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useUploadDocument } from "@/hooks/use-upload-document";

export function UploadButton() {
  const inputRef = useRef<HTMLInputElement>(null);

  const uploadMutation = useUploadDocument();

  function handleClick() {
    inputRef.current?.click();
  }

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) return;

    uploadMutation.mutate(file);

    // 允许再次选择同一个文件
    event.target.value = "";
  }

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        hidden
        onChange={handleFileChange}
      />

      <Button
        className="w-full"
        onClick={handleClick}
        disabled={uploadMutation.isPending}
      >
        <Upload className="mr-2 h-4 w-4" />

        {uploadMutation.isPending ? "Uploading..." : "Upload PDF"}
      </Button>
    </>
  );
}
