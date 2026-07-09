"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function SettingsPage() {
  const router = useRouter();
  const [theme, setTheme] = useState("noir");
  const [voiceRate, setVoiceRate] = useState(1.0);
  const [voicePitch, setVoicePitch] = useState(1.0);

  useEffect(() => {
    const savedTheme = localStorage.getItem("zero_theme") || "noir";
    const savedRate = localStorage.getItem("zero_voice_rate") || "1.0";
    const savedPitch = localStorage.getItem("zero_voice_pitch") || "1.0";

    setTheme(savedTheme);
    setVoiceRate(parseFloat(savedRate));
    setVoicePitch(parseFloat(savedPitch));
    document.body.setAttribute("data-theme", savedTheme);
  }, []);

  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
    localStorage.setItem("zero_theme", newTheme);
    document.body.setAttribute("data-theme", newTheme);
  };

  const handleRateChange = (val) => {
    setVoiceRate(val);
    localStorage.setItem("zero_voice_rate", val.toString());
  };

  const handlePitchChange = (val) => {
    setVoicePitch(val);
    localStorage.setItem("zero_voice_pitch", val.toString());
  };

  return (
    <main style={{
      minHeight: "100vh",
      width: "100vw",
      padding: "80px 24px",
      background: "var(--background)",
      color: "var(--foreground)",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      fontFamily: "var(--sans)"
    }}>
      <header style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        height: "64px",
        display: "flex",
        alignItems: "center",
        padding: "0 24px",
        background: "rgba(0,0,0,0.2)",
        backdropFilter: "blur(10px)",
        borderBottom: "1px solid var(--line)",
        zIndex: 100
      }}>
        <Link href="/" style={{
          fontSize: "0.9rem",
          fontWeight: "900",
          color: "#7c4dff",
          textDecoration: "none",
          display: "flex",
          alignItems: "center",
          gap: "8px"
        }}>
          <span>←</span> Back to Zero
        </Link>
      </header>

      <div style={{
        width: "100%",
        maxWidth: "500px",
        display: "flex",
        flexDirection: "column",
        gap: "32px"
      }}>
        <h1 style={{
          fontSize: "2rem",
          fontWeight: "900",
          letterSpacing: "-0.05em",
          margin: "0 0 10px 0"
        }}>Settings</h1>

        <section style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <h2 style={{ fontSize: "0.8rem", fontWeight: "900", textTransform: "uppercase", color: "#7c4dff" }}>Interface Appearance</h2>
          <div style={{ display: "flex", gap: "12px" }}>
            <button onClick={() => handleThemeChange("noir")} style={{
              flex: 1, padding: "16px", borderRadius: "12px", border: theme === "noir" ? "2px solid #7c4dff" : "1px solid var(--line)",
              background: theme === "noir" ? "rgba(124, 77, 255, 0.1)" : "var(--surface)", color: "var(--foreground)",
              fontWeight: "800", cursor: "pointer"
            }}>Noir (Dark)</button>
            <button onClick={() => handleThemeChange("ivory")} style={{
              flex: 1, padding: "16px", borderRadius: "12px", border: theme === "ivory" ? "2px solid #7c4dff" : "1px solid var(--line)",
              background: theme === "ivory" ? "rgba(124, 77, 255, 0.1)" : "var(--surface)", color: "var(--foreground)",
              fontWeight: "800", cursor: "pointer"
            }}>Ivory (Light)</button>
          </div>
        </section>

        <section style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          <h2 style={{ fontSize: "0.8rem", fontWeight: "900", textTransform: "uppercase", color: "#7c4dff" }}>Voice Engine</h2>

          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <label style={{ fontWeight: "800", fontSize: "0.85rem" }}>Speech Rate</label>
              <span style={{ color: "#7c4dff", fontWeight: "900" }}>{voiceRate.toFixed(2)}x</span>
            </div>
            <input type="range" min="0.5" max="1.5" step="0.05" value={voiceRate} onChange={(e) => handleRateChange(parseFloat(e.target.value))}
              style={{ width: "100%", accentColor: "#7c4dff" }} />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <label style={{ fontWeight: "800", fontSize: "0.85rem" }}>Voice Pitch</label>
              <span style={{ color: "#7c4dff", fontWeight: "900" }}>{voicePitch.toFixed(2)}</span>
            </div>
            <input type="range" min="0.5" max="1.5" step="0.05" value={voicePitch} onChange={(e) => handlePitchChange(parseFloat(e.target.value))}
              style={{ width: "100%", accentColor: "#7c4dff" }} />
          </div>
        </section>

        <section style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "20px", padding: "20px", background: "rgba(124, 77, 255, 0.05)", borderRadius: "16px", border: "1px dashed #7c4dff" }}>
          <p style={{ margin: 0, fontSize: "0.8rem", fontWeight: "700", lineHeight: "1.5" }}>
            Zero uses your phone's native Text-to-Speech engine. For more voice options, check your Android System Settings.
          </p>
        </section>
      </div>
    </main>
  );
}
