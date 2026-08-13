export interface ChatRequest {
    question: string;
}

export interface ChatResponse {
    answer: string;
}

export interface Message {
    role: 'user' | 'assistant';
    content: string;
}