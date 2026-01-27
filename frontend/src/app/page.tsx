"use client";

import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold">📊 KPI Insight Agent</h1>
          <p className="text-gray-600">
            Monitor KPIs, analyze causes, and talk to your data using AI
          </p>
        </div>

        {/* Navigation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Dashboard */}
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">📊 KPI Dashboard</h2>
              <p className="text-gray-600">
                Monitor revenue trends, alerts, and KPIs in real time.
              </p>
              <Link href="/dashboard">
                <Button>Open Dashboard</Button>
              </Link>
            </CardContent>
          </Card>

          {/* Talk to Data */}
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">💬 Talk to Your Data</h2>
              <p className="text-gray-600">
                Ask questions in natural language and get data-driven answers.
              </p>
              <Link href="/chat">
                <Button>Ask Questions</Button>
              </Link>
            </CardContent>
          </Card>

          {/* Causal Analysis */}
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">🧠 Causal Analysis</h2>
              <p className="text-gray-600">
                Understand *why* KPIs changed using causal reasoning.
              </p>
              <Link href="/causal">
                <Button>View Causes</Button>
              </Link>
            </CardContent>
          </Card>

          {/* Recommendations */}
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">💡 Recommendations</h2>
              <p className="text-gray-600">
                Get actionable recommendations based on KPI behavior.
              </p>
              <Link href="/recommend">
                <Button>Get Recommendations</Button>
              </Link>
            </CardContent>
          </Card>

          {/* KPI Intelligence Agent */}
<Card className="md:col-span-2 border-2 border-indigo-500">
  <CardContent className="p-8 space-y-4 text-center">
    <h2 className="text-2xl font-semibold flex justify-center items-center gap-2">
      🤖 KPI Intelligence Agent
    </h2>

    <p className="text-gray-600 max-w-2xl mx-auto">
      Autonomous agent that monitors KPIs, detects anomalies,
      analyzes root causes, and generates actionable recommendations.
    </p>

    <Link href="/agent">
      <Button className="bg-indigo-600 hover:bg-indigo-700 px-8 py-2">
        Run Agent
      </Button>
    </Link>
  </CardContent>
</Card>

        </div>

        {/* Footer */}
        <div className="text-center text-sm text-gray-500 pt-6">
          Built with FastAPI · Next.js · LLM Agents
        </div>
      </div>
    </main>
  );
}
