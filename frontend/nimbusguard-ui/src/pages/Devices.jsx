import React, { useEffect, useState } from "react";
import { getDevices } from "../api/devices";

export default function Devices() {
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");
  const [devices, setDevices] = useState([]);

  async function load() {
    setLoading(true);
    setErr("");
    try {
      const data = await getDevices();
      // Backend might return {devices:[...]} or just [...]
      const list = Array.isArray(data) ? data : data.devices || [];
      setDevices(list);
    } catch (e) {
      setErr(e?.message || "Failed to load devices");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <h2 style={{ margin: 0 }}>Devices</h2>
        <button onClick={load} style={{ cursor: "pointer" }}>
          Refresh
        </button>
      </div>

      {loading && <p>Loading devices…</p>}
      {err && <p style={{ color: "crimson" }}>{err}</p>}
      {!loading && !err && devices.length === 0 && (
        <p style={{ color: "#6b7280" }}>No devices found. Add one first.</p>
      )}

      {!loading && !err && devices.length > 0 && (
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
                <th style={th}>ID</th>
                <th style={th}>Name</th>
                <th style={th}>IP Address</th>
                <th style={th}>Type</th>
                <th style={th}>Location</th>
                <th style={th}>Status</th>
                <th style={th}>Last Seen</th>
              </tr>
            </thead>
            <tbody>
              {devices.map((d) => (
                <tr key={d.id ?? `${d.name}-${d.ip_address}`}>
                  <td style={td}>{d.id ?? "-"}</td>
                  <td style={td}>{d.name ?? "-"}</td>
                  <td style={td}>{d.ip_address ?? "-"}</td>
                  <td style={td}>{d.device_type ?? "-"}</td>
                  <td style={td}>{d.location ?? "-"}</td>
                  <td style={td}>{d.status ?? "unknown"}</td>
                  <td style={td}>{d.last_seen ?? "-"}</td>
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