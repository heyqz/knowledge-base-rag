import { Sidebar } from "../sidebar/sidebar";
import { Header } from "./header";
import { AnswerPanel } from "../knowledge/answer-panel";

export function AppLayout() {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />

      <main className="flex flex-1 flex-col">
        <Header />

        <AnswerPanel />
      </main>
    </div>
  );
}
