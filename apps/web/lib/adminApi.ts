export type Plant = {
  id: number;
  external_id: string | null;
  sinhala_name: string | null;
  common_name: string | null;
  scientific_name: string | null;
  part_used: string | null;
  traditional_use: string;
  preparation: string | null;
  safety_note: string | null;
  source_url: string | null;
  verification_status: string;
  safety_review_status: string;
  is_verified: boolean;
};

export type SourceRecord = {
  id: number;
  plant_id: number | null;
  title: string;
  institution: string | null;
  url: string;
  publication_year: number | null;
  verification_status: string;
  notes: string | null;
  created_at: string;
};

export type Review = {
  id: number;
  plant_id: number;
  reviewer_name: string;
  reviewer_role: string | null;
  status: string;
  comments: string | null;
  created_at: string;
};

export type Feedback = {
  id: number;
  chat_audit_id: number | null;
  helpful: boolean | null;
  category: string;
  comment: string | null;
  resolved: boolean;
  created_at: string;
};

export type SafetyFlag = {
  id: number;
  chat_audit_id: number | null;
  message_excerpt: string;
  severity: string;
  reason: string;
  status: string;
  created_at: string;
};

export type AuditEvent = {
  id: number;
  actor: string;
  action: string;
  entity_type: string;
  entity_id: string | null;
  details: string | null;
  created_at: string;
};

export type Stats = {
  plants: number;
  verified_plants: number;
  pending_plants: number;
  sources: number;
  pending_reviews: number;
  open_feedback: number;
  open_safety_flags: number;
  chat_audits: number;
};

export type Analytics = {
  languages: Record<string, number>;
  triage: Record<string, number>;
  feedback: Record<string, number>;
  recent_queries: Array<{
    id: number;
    message: string;
    language: string;
    triage: string;
    created_at: string;
  }>;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";
const TOKEN_KEY = "helacare_admin_token";

export function getAdminToken() {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem(TOKEN_KEY);
}

export function setAdminToken(token: string) {
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearAdminToken() {
  sessionStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getAdminToken();
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed: ${response.status}`);
  }
  if (response.status === 204) return undefined as T;
  return response.json();
}

export async function adminLogin(email: string, password: string) {
  return request<{ access_token: string; token_type: string; expires_in_minutes: number }>("/admin/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export const adminApi = {
  stats: () => request<Stats>("/admin/stats"),
  analytics: () => request<Analytics>("/admin/analytics"),
  plants: () => request<Plant[]>("/admin/plants"),
  createPlant: (payload: Omit<Plant, "id">) => request<Plant>("/admin/plants", { method: "POST", body: JSON.stringify(payload) }),
  updatePlant: (id: number, payload: Omit<Plant, "id">) => request<Plant>(`/admin/plants/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  verifyPlant: (id: number) => request<Plant>(`/admin/plants/${id}/verify`, { method: "POST" }),
  deletePlant: (id: number) => request<void>(`/admin/plants/${id}`, { method: "DELETE" }),
  sources: () => request<SourceRecord[]>("/admin/sources"),
  createSource: (payload: Omit<SourceRecord, "id" | "created_at">) => request<SourceRecord>("/admin/sources", { method: "POST", body: JSON.stringify(payload) }),
  updateSource: (id: number, payload: Omit<SourceRecord, "id" | "created_at">) => request<SourceRecord>(`/admin/sources/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteSource: (id: number) => request<void>(`/admin/sources/${id}`, { method: "DELETE" }),
  reviews: () => request<Review[]>("/admin/reviews"),
  createReview: (payload: Omit<Review, "id" | "created_at">) => request<Review>("/admin/reviews", { method: "POST", body: JSON.stringify(payload) }),
  updateReview: (id: number, payload: Omit<Review, "id" | "created_at">) => request<Review>(`/admin/reviews/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  feedback: () => request<Feedback[]>("/admin/feedback"),
  resolveFeedback: (id: number) => request<Feedback>(`/admin/feedback/${id}/resolve`, { method: "POST" }),
  safetyFlags: () => request<SafetyFlag[]>("/admin/safety-flags"),
  closeSafetyFlag: (id: number) => request<SafetyFlag>(`/admin/safety-flags/${id}/close`, { method: "POST" }),
  audit: () => request<AuditEvent[]>("/admin/audit"),
  reindex: () => request<{ indexed: number; dimensions: number }>("/admin/rag/reindex", { method: "POST" }),
};
