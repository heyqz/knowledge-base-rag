import Sidebar from "./Sidebar";
import ChatPanel from "./ChatPanel";

export default function Layout() {
  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
      }}
    >
      <Sidebar />

      <ChatPanel />
    </div>
  );
}