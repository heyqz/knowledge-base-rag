import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type MarkdownProps = {
  children: string;
};

export function MarkdownRenderer({ children }: MarkdownProps) {
  return (
    <div className="prose prose-neutral max-w-none dark:prose-invert">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children}</ReactMarkdown>
    </div>
  );
}
