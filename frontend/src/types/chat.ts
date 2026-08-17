export interface Source {
  filename: string;
  page: number;
  score: number;
}

export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}
