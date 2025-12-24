import React, { useState } from "react";
import { addDevice } from "../api/devices";
import { useNavigate } from "react-router-dom";

export default function AddDevice() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    ip_address: "",
    device_type: "",
    location: "",
  });

  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  function update(k, v) {
    setForm((p) => ({ ...p, [k]: v }));
  }

  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    setMsg("");

    if (!form.name || !form.ip_address || !form.device_type) {
      setErr("Name, IP address, and device type are required.");
      return;
    }

    setLoading(true);
    try {
      await addDevice(form);
      setMsg("Device added successfully.");
      // small delay so user sees the message
      setTimeout(() => navigate("/devices"), 600);
    } catch (e) {
      setErr(e?.response?.data?.detail || e?.message || "Failed to add device");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 20, maxWidth: 520 }}>
      <h2>Add Device</h2>

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 10 }}>
        <label>
          Name *
          <input
            value={form.name}
            onChange={(e) => update("name", e.target.value)}
            style={input}
            placeholder="Router-1"
          />
        </label>

        <label>
          IP Address *
          <input
            value={form.ip_address}
            onChange={(e) => update("ip_address", e.target.value)}
            style={input}
            placeholder="192.168.1.1"
          />
        </label>

        <label>
          Device Type *
          <input
            value={form.device_type}
            onChange={(e) => update("device_type", e.target.value)}
            style={input}
            placeholder="router / switch / firewall"
          />
        </label>

        <label>
          Location
          <input
            value={form.location}
            onChange={(e) => update("location", e.target.value)}
            style={input}
            placeholder="Boston Office"
          />
        </label>

        <button disabled={loading} type="submit" style={{ padding: 10, cursor: "pointer" }}>
          {loading ? "Adding…" : "Add Device"}
        </button>

        {msg && <div style={{ color: "green" }}>{msg}</div>}
        {err && <div style={{ color: "crimson" }}>{err}</div>}
      </form>
    </div>
  );
}

const input = { width: "100%", padding: 10, marginTop: 4 };