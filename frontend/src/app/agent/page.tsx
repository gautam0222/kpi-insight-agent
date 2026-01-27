"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function AgentPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/agent/run`, {
      method: "POST",
    })
      .then((res) => {
        if (!res.ok) throw new Error("Agent failed to run");
        return res.json();
      })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  /* ---------- LOADING STATE ---------- */
  if (loading) {
    return (
      <div className="p-10 text-center text-lg">
        🤖 Agent is analyzing KPIs...
      </div>
    );
  }

  /* ---------- ERROR STATE ---------- */
  if (error) {
    return (
      <div className="p-10 text-center text-red-600">
        ❌ {error}
      </div>
    );
  }

  /* ---------- SAFETY GUARD ---------- */
  if (!data || !data.monitor || !data.causal || !data.recommendations) {
    return (
      <div className="p-10 text-center text-gray-500">
        ⚠️ Agent returned incomplete data
      </div>
    );
  }

  return (
    <div className="space-y-8 p-6 max-w-6xl mx-auto">

      {/* HEADER */}
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          🤖 KPI Intelligence Agent
        </h1>
        <p className="text-gray-600">
          Revenue deviation detected. Agent completed end-to-end analysis.
        </p>
      </div>

      {/* KPI MONITOR */}
      <Card>
        <CardContent className="p-6 space-y-2">
          <h2 className="text-xl font-semibold">📊 KPI Monitor</h2>
          <p><b>Total Revenue:</b> ₹{data.monitor.total_revenue}</p>
          <p><b>Avg Daily Revenue:</b> ₹{data.monitor.avg_daily_revenue}</p>

          {data.monitor.alerts.length > 0 ? (
            data.monitor.alerts.map((a: any, i: number) => (
              <p key={i} className="text-red-600">
                🔴 {a.date} — {a.drop} revenue drop
              </p>
            ))
          ) : (
            <p className="text-green-600">✅ No critical alerts</p>
          )}
        </CardContent>
      </Card>

      {/* CAUSAL ANALYSIS */}
      <Card>
        <CardContent className="p-6 space-y-3">
          <h2 className="text-xl font-semibold">🧠 Causal Analysis</h2>
          <p>
            Revenue changed by <b>{data.causal.change_percent}%</b> (
            {data.causal.direction})
          </p>

          <ul className="list-disc pl-6">
            {data.causal.top_causes.map((c: any, i: number) => (
              <li key={i}>
                <b>{c.factor}</b> — impact ₹{Math.abs(c.impact)}
                <span className="text-gray-600"> ({c.type})</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* RECOMMENDATIONS */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold">💡 Recommendations</h2>

          {data.recommendations.recommendations.map((r: any, i: number) => (
            <div
              key={i}
              className="border-l-4 border-indigo-500 pl-4"
            >
              <p className="font-semibold">{r.action}</p>
              <p className="text-gray-600">{r.reason}</p>
              <p className="text-sm">
                Priority: <b>{r.priority}</b>
              </p>
            </div>
          ))}
        </CardContent>
      </Card>

      <Button
        className="w-full"
        onClick={() => window.location.reload()}
      >
        🔄 Re-Run Agent
      </Button>
    </div>
  );
}
