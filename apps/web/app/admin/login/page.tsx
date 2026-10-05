"use client";

import { useState } from "react";
import type { FormEvent } from "react";
import { useRouter } from "next/navigation";
import { adminLogin, setAdminToken } from "@/lib/adminApi";

export default function AdminLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@helacare.local");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const result = await adminLogin(email.trim(), password);
      setAdminToken(result.access_token);
      router.replace("/admin");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="adminLoginPage">
      <div className="adminGlow adminGlowOne" />
      <div className="adminGlow adminGlowTwo" />
      <section className="adminLoginCard">
        <div className="adminLoginBrand">
          <div className="adminLogo">H</div>
          <div>
            <h1>HelaCare</h1>
            <p>Admin & Curator Portal</p>
          </div>
        </div>
        <div className="adminLoginHeading">
          <span className="adminEyebrow">SECURE KNOWLEDGE MANAGEMENT</span>
          <h2>Welcome back</h2>
          <p>Sign in to curate verified knowledge, sources, safety reviews and feedback.</p>
        </div>
        <form className="adminLoginForm" onSubmit={submit}>
          <label>Email address<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /></label>
          <label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter admin password" required /></label>
          {error && <div className="adminLoginError">{error}</div>}
          <button className="adminLoginButton" disabled={loading}>{loading ? "Signing in..." : "Sign in"}<span>→</span></button>
        </form>
        <div className="adminLoginFooter"><span>●</span> JWT-protected curator access</div>
      </section>
    </main>
  );
}
