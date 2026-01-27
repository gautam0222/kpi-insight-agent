"use client";

import { useEffect, useState } from "react";
import { getCausalAnalysis } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function CausalPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCausalAnalysis()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="p-6">⏳ Running causal analysis...</p>;
  }

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>🧠 Causal Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            {data.window}
          </p>
          <p className="mt-2 text-lg font-semibold">
            Revenue Change:{" "}
            <span
              className={
                data.direction === "decrease"
                  ? "text-red-600"
                  : "text-green-600"
              }
            >
              {data.change_percent}%
            </span>
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Top Contributing Factors</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {data.top_causes.length === 0 && (
            <p className="text-sm text-muted-foreground">
              No strong causal factors detected.
            </p>
          )}

          {data.top_causes.map((cause: any, idx: number) => (
            <div
              key={idx}
              className="flex items-center justify-between border rounded p-3"
            >
              <div>
                <p className="font-medium">{cause.factor}</p>
                <p className="text-sm text-muted-foreground">
                  {cause.explanation}
                </p>
              </div>
              <Badge variant="destructive">
                {cause.impact}
              </Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}

  