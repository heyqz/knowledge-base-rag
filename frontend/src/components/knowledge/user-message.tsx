type UserMessageProps = {
  content: string;
};

export function UserMessage({
  content,
}: UserMessageProps) {
  return (
    <div className="flex justify-end">
      <div className="max-w-[80%] rounded-xl bg-primary px-4 py-3 text-primary-foreground">
        {content}
      </div>
    </div>
  );
}