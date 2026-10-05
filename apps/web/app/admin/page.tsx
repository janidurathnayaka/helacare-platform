"use client";

import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useRouter } from "next/navigation";
import {
  adminApi,
  clearAdminToken,
  getAdminToken,
  type Analytics,
  type AuditEvent,
  type Feedback,
  type Plant,
  type Review,
  type SafetyFlag,
  type SourceRecord,
  type Stats,
} from "@/lib/adminApi";

type Tab = "dashboard" | "plants" | "sources" | "reviews" | "feedback" | "safety" | "analytics" | "audit";

const emptyPlant: Omit<Plant, "id"> = {
  external_id: null,
  sinhala_name: null,
  common_name: null,
  scientific_name: null,
  part_used: null,
  traditional_use: "",
  preparation: null,
  safety_note: "Pending qualified clinical/practitioner review; no dosage advice",
  source_url: null,
  verification_status: "UNVERIFIED",
  safety_review_status: "REVIEW_REQUIRED",
  is_verified: false,
};

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

export default function AdminPage() {
  const router = useRouter();
  const [tab, setTab] = useState<Tab>("dashboard");
  const [stats, setStats] = useState<Stats | null>(null);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [plants, setPlants] = useState<Plant[]>([]);
  const [sources, setSources] = useState<SourceRecord[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [feedback, setFeedback] = useState<Feedback[]>([]);
  const [flags, setFlags] = useState<SafetyFlag[]>([]);
  const [audit, setAudit] = useState<AuditEvent[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showPlantForm, setShowPlantForm] = useState(false);
  const [editingPlant, setEditingPlant] = useState<Plant | null>(null);
  const [plantForm, setPlantForm] = useState<Omit<Plant, "id">>(emptyPlant);
  const [showSourceForm, setShowSourceForm] = useState(false);
  const [sourceForm, setSourceForm] = useState({ plant_id: null as number | null, title: "", institution: "", url: "", publication_year: null as number | null, verification_status: "PENDING", notes: "" });
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [reviewForm, setReviewForm] = useState({ plant_id: 0, reviewer_name: "", reviewer_role: "", status: "PENDING", comments: "" });
  const [message, setMessage] = useState("");

  async function loadAll() {
    setLoading(true); setError("");
    try {
      const [s, a, p, so, r, f, sf, au] = await Promise.all([
        adminApi.stats(), adminApi.analytics(), adminApi.plants(), adminApi.sources(), adminApi.reviews(), adminApi.feedback(), adminApi.safetyFlags(), adminApi.audit(),
      ]);
      setStats(s); setAnalytics(a); setPlants(p); setSources(so); setReviews(r); setFeedback(f); setFlags(sf); setAudit(au);
    } catch (err) {
      const text = err instanceof Error ? err.message : "Could not load admin data";
      setError(text);
      if (text.toLowerCase().includes("token") || text.toLowerCase().includes("expired")) {
        clearAdminToken(); router.replace("/admin/login");
      }
    } finally { setLoading(false); }
  }

  useEffect(() => {
    if (!getAdminToken()) { router.replace("/admin/login"); return; }
    void loadAll();
  }, [router]);

  const filteredPlants = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return plants;
    return plants.filter((p) => [p.external_id, p.sinhala_name, p.common_name, p.scientific_name, p.traditional_use].filter(Boolean).join(" ").toLowerCase().includes(q));
  }, [plants, search]);

  function logout() { clearAdminToken(); router.replace("/admin/login"); }
  function openNewPlant() { setEditingPlant(null); setPlantForm(emptyPlant); setShowPlantForm(true); }
  function openEditPlant(plant: Plant) { const { id: _id, ...rest } = plant; setEditingPlant(plant); setPlantForm(rest); setShowPlantForm(true); }

  async function savePlant(event: FormEvent) {
    event.preventDefault(); setMessage("");
    try {
      if (editingPlant) await adminApi.updatePlant(editingPlant.id, plantForm);
      else await adminApi.createPlant(plantForm);
      setShowPlantForm(false); setMessage("Plant record saved."); await loadAll();
    } catch (err) { setMessage(err instanceof Error ? err.message : "Could not save plant"); }
  }

  async function saveSource(event: FormEvent) {
    event.preventDefault();
    await adminApi.createSource({ ...sourceForm, institution: sourceForm.institution || null, notes: sourceForm.notes || null });
    setShowSourceForm(false); setSourceForm({ plant_id: null, title: "", institution: "", url: "", publication_year: null, verification_status: "PENDING", notes: "" });
    await loadAll();
  }

  async function saveReview(event: FormEvent) {
    event.preventDefault();
    await adminApi.createReview({ ...reviewForm, reviewer_role: reviewForm.reviewer_role || null, comments: reviewForm.comments || null });
    setShowReviewForm(false); setReviewForm({ plant_id: 0, reviewer_name: "", reviewer_role: "", status: "PENDING", comments: "" });
    await loadAll();
  }

  async function reindex() {
    setMessage("Rebuilding vector index...");
    const result = await adminApi.reindex();
    setMessage(`RAG index refreshed: ${result.indexed} records × ${result.dimensions} dimensions.`);
  }

  const nav: Array<[Tab, string, string]> = [
    ["dashboard", "⌂", "Dashboard"], ["plants", "🌿", "Plants"], ["sources", "↗", "Sources"], ["reviews", "✓", "Practitioner Reviews"],
    ["feedback", "☻", "User Feedback"], ["safety", "⚠", "Safety Flags"], ["analytics", "▥", "Analytics"], ["audit", "☷", "Audit Logs"],
  ];

  return (
    <main className="adminPage">
      <aside className="adminSidebar">
        <div className="adminSideBrand"><div className="adminSideLogo">H</div><div><strong>HelaCare</strong><span>Curator Console</span></div></div>
        <nav className="adminNav">{nav.map(([id, icon, label]) => <button key={id} className={`adminNavItem ${tab === id ? "active" : ""}`} onClick={() => setTab(id)}><span>{icon}</span>{label}</button>)}</nav>
        <div className="adminSidebarBottom"><div className="adminStatus"><span className="adminStatusDot" /> System online</div><button className="adminLogout" onClick={logout}>Sign out</button></div>
      </aside>

      <section className="adminContent">
        <header className="adminTopbar"><div><span className="adminTopEyebrow">KNOWLEDGE MANAGEMENT</span><h1>{nav.find((x) => x[0] === tab)?.[2]}</h1></div><div className="adminUser"><div><strong>HelaCare Admin</strong><span>Curator</span></div><div className="adminUserAvatar">A</div></div></header>
        {message && <div className="adminNotice">{message}</div>}
        {error && <div className="adminDashboardError">{error}<button onClick={() => void loadAll()}>Retry</button></div>}
        {loading && <div className="adminLoading">Loading curator workspace...</div>}

        {!loading && tab === "dashboard" && <>
          <section className="adminStats">
            {[
              ["🌿", "TOTAL PLANTS", stats?.plants ?? 0, "Knowledge records"], ["✓", "VERIFIED", stats?.verified_plants ?? 0, "Published records"],
              ["↗", "SOURCES", stats?.sources ?? 0, "Evidence records"], ["⚠", "SAFETY FLAGS", stats?.open_safety_flags ?? 0, "Open safety cases"],
            ].map(([icon, label, value, note]) => <div className="adminStatCard" key={String(label)}><span className="adminStatIcon">{icon}</span><div><small>{label}</small><strong>{value}</strong><p>{note}</p></div></div>)}
          </section>
          <section className="adminDashboardGrid">
            <div className="adminPanel"><div className="adminPanelHeader"><div><span className="adminTopEyebrow">RETRIEVAL</span><h2>RAG + pgvector</h2></div><button className="adminPrimaryButton" onClick={() => void reindex()}>Rebuild index</button></div><p className="adminMuted">Verified plant records are ranked with pgvector after exact/lexical search. Answers remain source-grounded and do not invent treatment or dosage.</p></div>
            <div className="adminPanel"><span className="adminTopEyebrow">WORK QUEUE</span><div className="adminQueue"><div><strong>{stats?.pending_plants ?? 0}</strong><span>Plants pending verification</span></div><div><strong>{stats?.pending_reviews ?? 0}</strong><span>Practitioner reviews pending</span></div><div><strong>{stats?.open_feedback ?? 0}</strong><span>User feedback unresolved</span></div></div></div>
          </section>
        </>}

        {!loading && tab === "plants" && <section className="adminPanel">
          <div className="adminPanelHeader"><div><span className="adminTopEyebrow">CURATED KNOWLEDGE</span><h2>Plant Records</h2></div><div className="adminToolbar"><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search plants..." /><button className="adminPrimaryButton" onClick={openNewPlant}>+ Add Plant</button></div></div>
          <div className="adminTableWrapper"><table className="adminTable"><thead><tr><th>Plant</th><th>Scientific name</th><th>Verification</th><th>Safety review</th><th>Actions</th></tr></thead><tbody>
            {filteredPlants.map((p) => <tr key={p.id}><td><div className="adminPlantName"><div className="adminPlantIcon">🌿</div><div><strong>{p.sinhala_name || p.common_name || "Unnamed"}</strong><span>{p.external_id || `#${p.id}`}</span></div></div></td><td><em>{p.scientific_name || "—"}</em></td><td><span className={`adminBadge ${p.is_verified ? "verified" : "pending"}`}>{p.verification_status}</span></td><td><span className="adminBadge review">{p.safety_review_status}</span></td><td><div className="adminRowActions"><button onClick={() => openEditPlant(p)}>Edit</button>{!p.is_verified && <button onClick={async () => { await adminApi.verifyPlant(p.id); await loadAll(); }}>Verify</button>}<button className="danger" onClick={async () => { if (confirm("Delete this plant record?")) { await adminApi.deletePlant(p.id); await loadAll(); } }}>Delete</button></div></td></tr>)}
          </tbody></table></div>
        </section>}

        {!loading && tab === "sources" && <section className="adminPanel"><div className="adminPanelHeader"><div><span className="adminTopEyebrow">EVIDENCE</span><h2>Sources</h2></div><button className="adminPrimaryButton" onClick={() => setShowSourceForm(true)}>+ Add Source</button></div><div className="adminCardsList">{sources.map((s) => <article className="adminListCard" key={s.id}><div><strong>{s.title}</strong><p>{s.institution || "Institution not specified"} {s.publication_year ? `• ${s.publication_year}` : ""}</p><a href={s.url} target="_blank" rel="noreferrer">Open source ↗</a></div><span className="adminBadge review">{s.verification_status}</span></article>)}</div></section>}

        {!loading && tab === "reviews" && <section className="adminPanel"><div className="adminPanelHeader"><div><span className="adminTopEyebrow">HUMAN REVIEW</span><h2>Practitioner Reviews</h2></div><button className="adminPrimaryButton" onClick={() => setShowReviewForm(true)}>+ Add Review</button></div><div className="adminCardsList">{reviews.map((r) => <article className="adminListCard" key={r.id}><div><strong>{r.reviewer_name}</strong><p>{r.reviewer_role || "Practitioner"} • Plant #{r.plant_id}</p><small>{r.comments || "No comments"}</small></div><span className={`adminBadge ${r.status === "APPROVED" ? "verified" : "pending"}`}>{r.status}</span></article>)}</div></section>}

        {!loading && tab === "feedback" && <section className="adminPanel"><div className="adminPanelHeader"><div><span className="adminTopEyebrow">QUALITY</span><h2>User Feedback</h2></div></div><div className="adminCardsList">{feedback.map((f) => <article className="adminListCard" key={f.id}><div><strong>{f.helpful === true ? "Helpful" : f.helpful === false ? "Not helpful" : f.category}</strong><p>{f.comment || "No comment"}</p><small>{formatDate(f.created_at)}</small></div>{f.resolved ? <span className="adminBadge verified">Resolved</span> : <button onClick={async () => { await adminApi.resolveFeedback(f.id); await loadAll(); }}>Resolve</button>}</article>)}</div></section>}

        {!loading && tab === "safety" && <section className="adminPanel"><div className="adminPanelHeader"><div><span className="adminTopEyebrow">SAFETY OPERATIONS</span><h2>Safety Flags</h2></div></div><div className="adminCardsList">{flags.map((f) => <article className="adminListCard safetyCard" key={f.id}><div><strong>{f.severity} • {f.reason}</strong><p>{f.message_excerpt}</p><small>{formatDate(f.created_at)}</small></div>{f.status === "OPEN" ? <button onClick={async () => { await adminApi.closeSafetyFlag(f.id); await loadAll(); }}>Close flag</button> : <span className="adminBadge verified">Closed</span>}</article>)}</div></section>}

        {!loading && tab === "analytics" && <section className="adminDashboardGrid"><div className="adminPanel"><span className="adminTopEyebrow">CHAT LANGUAGES</span><div className="adminMetricBars">{Object.entries(analytics?.languages ?? {}).map(([k, v]) => <div key={k}><span>{k === "si" ? "Sinhala" : "English"}</span><strong>{v}</strong></div>)}</div></div><div className="adminPanel"><span className="adminTopEyebrow">TRIAGE</span><div className="adminMetricBars">{Object.entries(analytics?.triage ?? {}).map(([k, v]) => <div key={k}><span>{k}</span><strong>{v}</strong></div>)}</div></div><div className="adminPanel adminWide"><span className="adminTopEyebrow">RECENT QUERIES</span><div className="adminCardsList">{(analytics?.recent_queries ?? []).map((q) => <div className="adminListCard" key={q.id}><div><strong>{q.message}</strong><small>{q.language} • {q.triage} • {formatDate(q.created_at)}</small></div></div>)}</div></div></section>}

        {!loading && tab === "audit" && <section className="adminPanel"><div className="adminPanelHeader"><div><span className="adminTopEyebrow">ACCOUNTABILITY</span><h2>Audit Log</h2></div></div><div className="adminTableWrapper"><table className="adminTable"><thead><tr><th>Time</th><th>Actor</th><th>Action</th><th>Entity</th><th>Details</th></tr></thead><tbody>{audit.map((a) => <tr key={a.id}><td>{formatDate(a.created_at)}</td><td>{a.actor}</td><td>{a.action}</td><td>{a.entity_type} {a.entity_id ?? ""}</td><td>{a.details || "—"}</td></tr>)}</tbody></table></div></section>}
      </section>

      {showPlantForm && <div className="adminModalBackdrop"><form className="adminModal" onSubmit={savePlant}><div className="adminPanelHeader"><div><span className="adminTopEyebrow">PLANT RECORD</span><h2>{editingPlant ? "Edit Plant" : "Add Plant"}</h2></div><button type="button" onClick={() => setShowPlantForm(false)}>✕</button></div><div className="adminFormGrid">
        <label>External ID<input value={plantForm.external_id ?? ""} onChange={(e) => setPlantForm({ ...plantForm, external_id: e.target.value || null })} /></label>
        <label>Local / Sinhala name<input value={plantForm.sinhala_name ?? ""} onChange={(e) => setPlantForm({ ...plantForm, sinhala_name: e.target.value || null })} /></label>
        <label>Common name<input value={plantForm.common_name ?? ""} onChange={(e) => setPlantForm({ ...plantForm, common_name: e.target.value || null })} /></label>
        <label>Scientific name<input value={plantForm.scientific_name ?? ""} onChange={(e) => setPlantForm({ ...plantForm, scientific_name: e.target.value || null })} /></label>
        <label>Part used<input value={plantForm.part_used ?? ""} onChange={(e) => setPlantForm({ ...plantForm, part_used: e.target.value || null })} /></label>
        <label>Source URL<input value={plantForm.source_url ?? ""} onChange={(e) => setPlantForm({ ...plantForm, source_url: e.target.value || null })} /></label>
        <label className="adminFull">Documented traditional use<textarea required value={plantForm.traditional_use} onChange={(e) => setPlantForm({ ...plantForm, traditional_use: e.target.value })} /></label>
        <label className="adminFull">Preparation / context<textarea value={plantForm.preparation ?? ""} onChange={(e) => setPlantForm({ ...plantForm, preparation: e.target.value || null })} /></label>
        <label className="adminFull">Safety note<textarea value={plantForm.safety_note ?? ""} onChange={(e) => setPlantForm({ ...plantForm, safety_note: e.target.value || null })} /></label>
        <label>Verification<select value={plantForm.verification_status} onChange={(e) => setPlantForm({ ...plantForm, verification_status: e.target.value })}><option>UNVERIFIED</option><option>PENDING</option><option>VERIFIED</option><option>REJECTED</option></select></label>
        <label>Safety review<select value={plantForm.safety_review_status} onChange={(e) => setPlantForm({ ...plantForm, safety_review_status: e.target.value })}><option>REVIEW_REQUIRED</option><option>PENDING</option><option>APPROVED</option><option>REJECTED</option></select></label>
      </div><div className="adminModalActions"><button type="button" onClick={() => setShowPlantForm(false)}>Cancel</button><button className="adminPrimaryButton">Save record</button></div></form></div>}

      {showSourceForm && <div className="adminModalBackdrop"><form className="adminModal" onSubmit={saveSource}><div className="adminPanelHeader"><h2>Add Source</h2><button type="button" onClick={() => setShowSourceForm(false)}>✕</button></div><div className="adminFormGrid"><label>Plant<select value={sourceForm.plant_id ?? ""} onChange={(e) => setSourceForm({ ...sourceForm, plant_id: e.target.value ? Number(e.target.value) : null })}><option value="">General source</option>{plants.map((p) => <option key={p.id} value={p.id}>{p.common_name || p.sinhala_name || p.id}</option>)}</select></label><label>Title<input required value={sourceForm.title} onChange={(e) => setSourceForm({ ...sourceForm, title: e.target.value })} /></label><label>Institution<input value={sourceForm.institution} onChange={(e) => setSourceForm({ ...sourceForm, institution: e.target.value })} /></label><label>Year<input type="number" value={sourceForm.publication_year ?? ""} onChange={(e) => setSourceForm({ ...sourceForm, publication_year: e.target.value ? Number(e.target.value) : null })} /></label><label className="adminFull">URL<input required value={sourceForm.url} onChange={(e) => setSourceForm({ ...sourceForm, url: e.target.value })} /></label><label className="adminFull">Notes<textarea value={sourceForm.notes} onChange={(e) => setSourceForm({ ...sourceForm, notes: e.target.value })} /></label></div><div className="adminModalActions"><button type="button" onClick={() => setShowSourceForm(false)}>Cancel</button><button className="adminPrimaryButton">Save source</button></div></form></div>}

      {showReviewForm && <div className="adminModalBackdrop"><form className="adminModal" onSubmit={saveReview}><div className="adminPanelHeader"><h2>Add Practitioner Review</h2><button type="button" onClick={() => setShowReviewForm(false)}>✕</button></div><div className="adminFormGrid"><label>Plant<select required value={reviewForm.plant_id || ""} onChange={(e) => setReviewForm({ ...reviewForm, plant_id: Number(e.target.value) })}><option value="">Select plant</option>{plants.map((p) => <option key={p.id} value={p.id}>{p.common_name || p.sinhala_name || p.id}</option>)}</select></label><label>Reviewer<input required value={reviewForm.reviewer_name} onChange={(e) => setReviewForm({ ...reviewForm, reviewer_name: e.target.value })} /></label><label>Role<input value={reviewForm.reviewer_role} onChange={(e) => setReviewForm({ ...reviewForm, reviewer_role: e.target.value })} /></label><label>Status<select value={reviewForm.status} onChange={(e) => setReviewForm({ ...reviewForm, status: e.target.value })}><option>PENDING</option><option>APPROVED</option><option>REJECTED</option></select></label><label className="adminFull">Comments<textarea value={reviewForm.comments} onChange={(e) => setReviewForm({ ...reviewForm, comments: e.target.value })} /></label></div><div className="adminModalActions"><button type="button" onClick={() => setShowReviewForm(false)}>Cancel</button><button className="adminPrimaryButton">Save review</button></div></form></div>}
    </main>
  );
}
