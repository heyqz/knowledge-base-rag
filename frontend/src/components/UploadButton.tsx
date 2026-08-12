import { uploadDocument } from "../services/document";

type Props = {
  onUploaded: () => void;
};

export default function UploadButton({ onUploaded }: Props) {
  async function handleChange(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = e.target.files?.[0];

    if (!file) return;

    await uploadDocument(file);

    onUploaded();
  }

  return (
    <input
      type="file"
      accept=".pdf"
      onChange={handleChange}
    />
  );
}