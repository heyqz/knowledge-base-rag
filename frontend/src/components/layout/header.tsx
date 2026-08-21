type HeaderProps = {
  onMenuClick: () => void;
};

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="border-b bg-white px-8 py-6">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onMenuClick}
          className="rounded-md p-2 text-xl hover:bg-muted md:hidden"
          aria-label="Open documents"
        >
          ☰
        </button>

        <h1 className="text-3xl font-bold sm:text-4xl">📚 Knowledge Base</h1>
      </div>

      <p className="mt-2 text-gray-500">
        Search across your indexed documents.
      </p>
    </header>
  );
}
