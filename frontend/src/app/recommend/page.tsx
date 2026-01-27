"use client";

import { useEffect, useState } from "react";
import { getRecommendations } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function RecommendPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getRecommendations()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="p-6">⏳ Generating recommendations...</p>;
  }

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>💡 Actionable Recommendations</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {data.recommendations.map((rec: any, idx: number) => (
            <div
              key={idx}
              className="border rounded p-4 flex justify-between items-start"
            >
              <div>
                <p className="font-semibold">{rec.action}</p>
                <p className="text-sm text-muted-foreground">
                  {rec.reason}
                </p>
                <p className="text-xs mt-1">
                  Expected Impact: {rec.expected_impact}
                </p>
              </div>

              <Badge
                variant={
                  rec.priority === "High"
                    ? "destructive"
                    : rec.priority === "Medium"
                    ? "secondary"
                    : "outline"
                }
              >
                {rec.priority}
              </Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
