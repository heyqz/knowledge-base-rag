import { useDocuments } from "../hooks/useDocuments";
import UploadButton from "./UploadButton";

export default function Sidebar() {
  const { documents, loading, refresh,error } = useDocuments();

  return (
    <aside
      style={{
        width: 280,
        borderRight: "1px solid #ddd",
        padding: 20,
      }}
    >
      <h2>Knowledge Base</h2>

      <hr />

      <h3>Documents</h3>

      {loading && <p>Loading...</p>}

      {error && <p>{error}</p>}

      {!loading &&
        documents.map((doc) => (
          <div key={doc.id}>
            📄 {doc.filename}
          </div>
        ))}

      <br />

      <UploadButton onUploaded={refresh}/>
    </aside>
  );
}