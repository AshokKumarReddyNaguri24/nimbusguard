import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const isAuthed = localStorage.getItem("ng_authed") === "true";

  function logout() {
    localStorage.removeItem("ng_authed");
    navigate("/login");
  }

  return (
    <div style={{ padding: "12px 16px", borderBottom: "1px solid #e5e7eb" }}>
      <div style={{ display: "flex", gap: 14, alignItems: "center" }}>
        <div style={{ fontWeight: 800 }}>NimbusGuard</div>

        {isAuthed && (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/devices">Devices</Link>
            <Link to="/devices/add">Add Device</Link>
            <Link to="/alerts">Alerts</Link>

            <div style={{ flex: 1 }} />

            <button onClick={logout} style={{ cursor: "pointer" }}>
              Logout
            </button>
          </>
        )}

        {!isAuthed && (
          <>
            <div style={{ flex: 1 }} />
            <Link to="/login">Login</Link>
          </>
        )}
      </div>
    </div>
  );
}