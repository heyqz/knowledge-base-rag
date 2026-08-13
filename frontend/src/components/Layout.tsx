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
      <div style={{ flex: 1 }}>      
        <ChatPanel />
      </div>
    </div>
  );
}