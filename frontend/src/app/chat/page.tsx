"use client";

import { useState } from "react";
import { askData } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    if (!question.trim()) return;

    setLoading(true);
    setData(null);

    try {
      const res = await askData(question);
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>💬 Talk to Your Data</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g. What was the avg revenue in last 10 days?"
          />
          <Button onClick={handleAsk} disabled={loading}>
            {loading ? "Thinking..." : "Ask"}
          </Button>
        </CardContent>
      </Card>

      {data && (
        <Card>
          <CardHeader>
            <CardTitle>📊 Answer</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p><strong>Result:</strong> {String(data.result)}</p>
            <p className="text-sm text-muted-foreground">{data.explanation}</p>
            <pre className="bg-black text-green-400 p-3 rounded text-xs">
              {data.code}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
