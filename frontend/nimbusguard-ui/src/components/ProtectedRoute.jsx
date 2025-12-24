import React from "react";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const isAuthed = localStorage.getItem("ng_authed") === "true";
  if (!isAuthed) return <Navigate to="/login" replace />;
  return children;
}