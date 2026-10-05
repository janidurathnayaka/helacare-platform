export type ChatSource = {
  plant_id: number;
  name: string;
  source_url: string | null;
};

export type ChatResponse = {
  audit_id: number | null;
  triage_level: "normal" | "urgent";
  answer: string;
  sources: ChatSource[];
  disclaimer: string;
};

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function sendChat(
  message: string,
  language: "en" | "si",
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, language }),
  });

  if (!response.ok) {
    throw new Error(`HelaCare API error: ${response.status}`);
  }

  return response.json();
}

export async function sendFeedback(payload: { audit_id: number | null; helpful: boolean | null; category?: string; comment?: string }) {
  const response = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_audit_id: payload.audit_id, helpful: payload.helpful, category: payload.category ?? "GENERAL", comment: payload.comment ?? null }),
  });
  if (!response.ok) throw new Error(`Feedback error: ${response.status}`);
  return response.json();
}
