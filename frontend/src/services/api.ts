const API_BASE = "http://localhost:8000";

export async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, options);

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json();
}