import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");

  function onSubmit(e) {
    e.preventDefault();
    // Week 1-3: no real auth. Just gate UI.
    if (!email || !pw) return;
    localStorage.setItem("ng_authed", "true");
    navigate("/dashboard");
  }

  return (
    <div style={{ padding: 20, maxWidth: 420 }}>
      <h2 style={{ marginBottom: 8 }}>Login</h2>
      <p style={{ marginTop: 0, color: "#6b7280" }}>
        Week 1–3 demo login (local only).
      </p>

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 10 }}>
        <label>
          Email
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: "100%", padding: 10, marginTop: 4 }}
            placeholder="you@example.com"
          />
        </label>

        <label>
          Password
          <input
            value={pw}
            onChange={(e) => setPw(e.target.value)}
            type="password"
            style={{ width: "100%", padding: 10, marginTop: 4 }}
            placeholder="••••••••"
          />
        </label>

        <button type="submit" style={{ padding: 10, cursor: "pointer" }}>
          Sign in
        </button>
      </form>
    </div>
  );
}