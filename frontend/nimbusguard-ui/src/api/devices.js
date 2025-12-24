import { api } from "./client";

export async function getDevices() {
  const res = await api.get("/devices/all");
  return res.data;
}

export async function addDevice(payload) {
  const res = await api.post("/devices/add", payload);
  return res.data;
}