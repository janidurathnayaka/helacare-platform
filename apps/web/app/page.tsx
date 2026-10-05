import ChatPanel from "@/components/ChatPanel";

export default function HomePage() {
  return (
    <main className="helacare-shell">
      <div className="bg-orb orb-1" />
      <div className="bg-orb orb-2" />
      <div className="bg-grid" />

      {/* LEFT SIDE */}
      <section className="hero-panel">
        <div className="brand-row">
          <div className="brand-badge">H</div>

          <div>
            <h1>HelaCare</h1>
            <span className="brand-subtitle">
              Traditional Health Companion
            </span>
          </div>
        </div>

        <div className="hero-content">
          <p className="eyebrow">
            SRI LANKAN DIGITAL HEALTH KNOWLEDGE
          </p>

          <h2 className="hero-title">
            Traditional
            <br />
            knowledge,
            <br />
            <span>delivered</span>
            <br />
            <span>responsibly.</span>
          </h2>

          <p className="hero-text">
            HelaCare is a source-grounded assistant for Sri Lankan
            traditional health knowledge. It retrieves verified
            records, applies a safety gate first, and shows sources
            behind answers.
          </p>

          <div className="feature-list">
            <div className="feature-item">
              <span>01</span>
              <p>Verified records only</p>
            </div>

            <div className="feature-item">
              <span>02</span>
              <p>Emergency red-flag gate</p>
            </div>

            <div className="feature-item">
              <span>03</span>
              <p>Auditable source trail</p>
            </div>
          </div>
        </div>

        <div className="hero-footer">
          HelaCare • Sri Lankan Traditional Knowledge
        </div>
      </section>

      {/* RIGHT SIDE CHAT */}
      <section className="chat-panel">
        <ChatPanel />
      </section>
    </main>
  );
}