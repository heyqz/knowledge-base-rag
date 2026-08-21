import { Sidebar } from "../sidebar/sidebar";
import { Header } from "./header";
import { AnswerPanel } from "../knowledge/answer-panel";

export function AppLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      <Sidebar />

      <main className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <Header />

        <div className="min-h-0 flex-1">
          <AnswerPanel />
        </div>
      </main>
    </div>
  );
}
