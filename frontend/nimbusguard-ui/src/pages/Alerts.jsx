import React, { useEffect, useState } from "react";
import { getAlerts } from "../api/alerts";

export default function Alerts() {
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");
  const [alerts, setAlerts] = useState([]);

  async function load() {
    setLoading(true);
    setErr("");
    try {
      const data = await getAlerts();
      const list = Array.isArray(data) ? data : data.alerts || [];
      setAlerts(list);
    } catch (e) {
      setErr(e?.message || "Failed to load alerts");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  function sevStyle(sev) {
    const s = (sev || "").toLowerCase();
    if (s === "critical") return { fontWeight: 700, color: "crimson" };
    if (s === "warning") return { fontWeight: 700, color: "#b45309" };
    return { color: "green" };
  }

  return (
    <div style={{ padding: 20 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <h2 style={{ margin: 0 }}>Alerts</h2>
        <button onClick={load} style={{ cursor: "pointer" }}>
          Refresh
        </button>
      </div>

      {loading && <p>Loading alerts…</p>}
      {err && <p style={{ color: "crimson" }}>{err}</p>}
      {!loading && !err && alerts.length === 0 && (
        <p style={{ color: "#6b7280" }}>No alerts detected.</p>
      )}

      {!loading && !err && alerts.length > 0 && (
        <div style={{ marginTop: 12, overflowX: "auto" }}>
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              border: "1px solid #e5e7eb",
            }}
          >
            <thead>
              <tr style={{ background: "#f9fafb" }}>
                <th style={th}>Time</th>
                <th style={th}>Device ID</th>
                <th style={th}>Metric</th>
                <th style={th}>Value</th>
                <th style={th}>Severity</th>
                <th style={th}>Z-Score</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((a) => (
                <tr key={a.id ?? `${a.device_id}-${a.metric_name}-${a.created_at}`}>
                  <td style={td}>{a.created_at ?? a.timestamp ?? "-"}</td>
                  <td style={td}>{a.device_id ?? "-"}</td>
                  <td style={td}>{a.metric_name ?? a.metric ?? "-"}</td>
                  <td style={td}>{(a.metric_value ?? a.value ?? "-")}</td>
                  <td style={{ ...td, ...sevStyle(a.severity) }}>
                    {a.severity ?? "normal"}
                  </td>
                  <td style={td}>
                    {typeof a.z_score === "number" ? a.z_score.toFixed(2) : (a.z_score ?? "-")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

const th = { padding: 10, textAlign: "left", borderBottom: "1px solid #e5e7eb" };
const td = { padding: 10, borderBottom: "1px solid #e5e7eb" };