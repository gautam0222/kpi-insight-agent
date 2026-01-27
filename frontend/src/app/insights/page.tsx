"use client";

import { useEffect, useState } from "react";
import { getCausalAnalysis, getRecommendations } from "@/lib/api";
import { Card } from "@/components/ui/card";

export default function InsightsPage() {
  const [causal, setCausal] = useState<any>(null);
  const [reco, setReco] = useState<any>(null);

  useEffect(() => {
    getCausalAnalysis().then(setCausal);
    getRecommendations().then(setReco);
  }, []);

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold">🧠 KPI Insights</h1>

      {causal && (
        <Card className="p-4">
          <h2 className="font-semibold mb-2">
            Revenue Change: {causal.change_percent}%
          </h2>
          <ul className="list-disc pl-5">
            {causal.top_causes.map((c: any, i: number) => (
              <li key={i}>
                <strong>{c.factor}:</strong> {c.impact} ({c.confidence})
              </li>
            ))}
          </ul>
        </Card>
      )}

      {reco && (
        <Card className="p-4">
          <h2 className="font-semibold mb-2">Recommended Actions</h2>
          <ul className="list-disc pl-5">
            {reco.recommendations.map((r: any, i: number) => (
              <li key={i}>
                <strong>{r.action}</strong> — {r.reason}
                <span className="ml-2 text-sm text-muted-foreground">
                  [{r.priority}]
                </span>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
