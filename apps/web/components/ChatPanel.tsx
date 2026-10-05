"use client";

import { useEffect, useRef, useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import { sendChat, sendFeedback } from "@/lib/api";
import type { ChatResponse } from "@/lib/api";

type Language = "en" | "si";

type HistoryItem = {
  question: string;
  response: ChatResponse;
};

export default function ChatPanel() {
  const [message, setMessage] = useState("");
  const [language, setLanguage] = useState<Language>("en");
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [history, loading]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const cleanMessage = message.trim();

    if (!cleanMessage || loading) return;

    setError("");
    setLoading(true);

    try {
      const response = await sendChat(cleanMessage, language);

      setHistory((currentHistory) => [
        ...currentHistory,
        {
          question: cleanMessage,
          response,
        },
      ]);

      setMessage("");
    } catch (err) {
      console.error("Chat request failed:", err);

      setError(
        language === "si"
          ? "HelaCare API එකට සම්බන්ධ වීමට නොහැකි විය. නැවත උත්සාහ කරන්න."
          : "Could not connect to the HelaCare API. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      if (!loading && message.trim().length >= 2) {
        event.currentTarget.form?.requestSubmit();
      }
    }
  }

  return (
    <section className="assistantShell">
      {/* HEADER */}
      <div className="assistantHeader">
        <div className="headerTop">
          <div className="headerTextBlock">
            <div className="assistantBadge">SOURCE-GROUNDED ASSISTANT</div>

            <h2 className="assistantHeading">Ask HelaCare</h2>

            <p className="assistantSubtext">
              {language === "si"
                ? "තහවුරු කළ සාම්ප්‍රදායික දැනුම, ආරක්ෂක සැලකිල්ල සමඟ"
                : "Verified traditional knowledge with safety-first responses"}
            </p>
          </div>

          <select
  className="languageSelect"
  aria-label="Select language"
  value={language}
  onChange={(event) =>
    setLanguage(event.target.value as "en" | "si")
  }
>
  <option value="en">English</option>
  <option value="si">සිංහල</option>
</select>
        </div>
      </div>

      {/* CONVERSATION */}
      <div className="conversation">
        {history.length === 0 && !loading && (
          <div className="welcomeState">
            <div className="assistantAvatar">H</div>

            <h3>
              {language === "si"
                ? "HelaCare වෙත සාදරයෙන් පිළිගනිමු"
                : "Welcome to HelaCare"}
            </h3>

            <p>
              {language === "si"
                ? "ශ්‍රී ලාංකික සාම්ප්‍රදායික සෞඛ්‍ය දැනුම පිළිබඳ ප්‍රශ්නයක් අසන්න."
                : "Ask about verified Sri Lankan traditional-health knowledge."}
            </p>

            <div className="quickPrompts">
              <button
                type="button"
                onClick={() =>
                  setMessage(
                    language === "si"
                      ? "ගොටුකොළ ගැන කියන්න"
                      : "Tell me about gotukola"
                  )
                }
              >
                🌿 Gotu kola
              </button>

              <button
                type="button"
                onClick={() =>
                  setMessage(
                    language === "si"
                      ? "කොත්තමල්ලි ගැන කියන්න"
                      : "Tell me about koththamalli"
                  )
                }
              >
                🌱 Koththamalli
              </button>

              <button
                type="button"
                onClick={() =>
                  setMessage(
                    language === "si"
                      ? "ඉඟුරු ගැන කියන්න"
                      : "Tell me about ginger"
                  )
                }
              >
                ✨ Ginger
              </button>
            </div>
          </div>
        )}

        {history.map((item, index) => {
          const isUrgent = item.response.triage_level === "urgent";

          return (
            <article key={`${item.question}-${index}`} className="exchange">
              {/* USER */}
              <div className="userRow">
                <div className="userMessage">{item.question}</div>
              </div>

              {/* ASSISTANT */}
              <div className={isUrgent ? "assistantMessage urgent" : "assistantMessage"}>
                <div className="assistantResponseHeader">
                  <div className="miniAvatar">H</div>

                  <div>
                    <div className="statusLine">
                      {isUrgent
                        ? language === "si"
                          ? "හදිසි ආරක්ෂක දැනුම්දීම"
                          : "URGENT SAFETY NOTICE"
                        : language === "si"
                        ? "තහවුරු කළ දැනුම් ප්‍රතිචාරය"
                        : "VERIFIED KNOWLEDGE RESPONSE"}
                    </div>

                    <span className="assistantName">HelaCare</span>
                  </div>
                </div>

                <div className="answerText">{item.response.answer}</div>

                {item.response.sources && item.response.sources.length > 0 && (
                  <div className="sources">
                    <span className="sourceTitle">
                      {language === "si" ? "මූලාශ්‍ර" : "Sources used"}
                    </span>

                    <div className="sourceList">
                      {item.response.sources.map((source) => {
                        if (source.source_url) {
                          return (
                            <a
                              key={source.plant_id}
                              href={source.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="sourceChip"
                            >
                              ↗ {source.name}
                            </a>
                          );
                        }

                        return (
                          <span key={source.plant_id} className="sourceChip">
                            {source.name}
                          </span>
                        );
                      })}
                    </div>
                  </div>
                )}

                {item.response.disclaimer && (
                  <div className="disclaimer">{item.response.disclaimer}</div>
                )}

                <div className="chatFeedback">
                  <span>Was this helpful?</span>
                  <button type="button" onClick={() => void sendFeedback({ audit_id: item.response.audit_id, helpful: true })}>👍</button>
                  <button type="button" onClick={() => void sendFeedback({ audit_id: item.response.audit_id, helpful: false, category: "NOT_HELPFUL" })}>👎</button>
                </div>
              </div>
            </article>
          );
        })}

        {loading && (
          <div className="assistantMessage loadingMessage">
            <div className="miniAvatar">H</div>

            <div className="typingDots">
              <span />
              <span />
              <span />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* ERROR */}
      {error && <div className="errorBox">{error}</div>}

      {/* INPUT */}
      <form className="composer" onSubmit={submit}>
        <div className="inputContainer">
          <textarea
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              language === "si"
                ? "ඔබට දැනගන්න අවශ්‍ය දේ ලියන්න..."
                : "Ask HelaCare about verified traditional knowledge..."
            }
            rows={1}
            disabled={loading}
          />

          <span className="inputHint">
            {language === "si" ? "Enter ↵" : "Enter ↵"}
          </span>
        </div>

        <button
          type="submit"
          className="askButton"
          disabled={loading || message.trim().length < 2}
        >
          {loading
            ? language === "si"
              ? "සිතමින්..."
              : "Thinking..."
            : language === "si"
            ? "Ask HelaCare"
            : "Ask HelaCare"}

          {!loading && <span aria-hidden="true">→</span>}
        </button>
      </form>
    </section>
  );
}