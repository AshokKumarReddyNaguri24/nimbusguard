import { api } from "./client";

export async function getAlerts() {
  const res = await api.get("/alerts");
  return res.data;
}