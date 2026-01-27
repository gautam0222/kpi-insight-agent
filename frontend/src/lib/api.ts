const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

if (!BASE_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not defined");
}

/* ---------------- DASHBOARD / MONITOR ---------------- */

export async function getDashboard() {
  const res = await fetch(`${BASE_URL}/monitor`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch dashboard data");
  }

  return res.json();
}

/* ---------------- TALK TO DATA ---------------- */

export async function askData(question: string) {
  const res = await fetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    throw new Error("Failed to ask data");
  }

  return res.json();
}

/* ---------------- CAUSAL ANALYSIS ---------------- */

export async function getCausalAnalysis() {
  const res = await fetch(`${BASE_URL}/causal`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch causal analysis");
  }

  return res.json();
}

/* ---------------- RECOMMENDATIONS ---------------- */

export async function getRecommendations() {
  const res = await fetch(`${BASE_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  return res.json();
}

