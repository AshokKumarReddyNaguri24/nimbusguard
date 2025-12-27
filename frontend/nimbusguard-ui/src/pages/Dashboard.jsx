import React from "react";

export default function Dashboard() {
  return (
    <div style={{ padding: 20 }}>
      <h2>Dashboard</h2>
      <p style={{ color: "#6b7280" }}>
        Week 1–3: This is a placeholder. Next we’ll show health score, top alerts,
        and predictions.
      </p>

      <div
        style={{
          marginTop: 16,
          padding: 16,
          border: "1px solid #e5e7eb",
          borderRadius: 10,
        }}
      >
        <div style={{ fontWeight: 700 }}>System Status</div>
        <div style={{ marginTop: 8 }}>Backend: expected at /healthcheck</div>
        <div>DBs: running via docker-compose</div>
        <div>AI: anomaly detection via /anomaly/check</div>
      </div>
    </div>
  );
}