import { useState } from "react";

import { Sidebar } from "../sidebar/sidebar";
import { Header } from "./header";
import { AnswerPanel } from "../knowledge/answer-panel";

export function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      {/* Desktop Sidebar */}
      <div className="hidden md:block">
        <Sidebar />
      </div>

      {/* Mobile Sidebar */}
      {sidebarOpen && (
        <>
          <div
            className="fixed inset-0 z-40 bg-black/40 md:hidden"
            onClick={() => setSidebarOpen(false)}
          />

          <div className="fixed inset-y-0 left-0 z-50 w-72 md:hidden">
            <Sidebar />
          </div>
        </>
      )}
      <main className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(true)} />

        <div className="min-h-0 flex-1">
          <AnswerPanel />
        </div>
      </main>
    </div>
  );
}
