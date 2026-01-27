"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getDashboard } from "@/lib/api";
import { KPICard } from "@/components/KPICard";
import { RevenueChart } from "@/components/RevenueChart";

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    async function load() {
      try {
        const res = await getDashboard();
        setSummary(res);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="text-muted-foreground">
        Loading dashboard…
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="text-red-500">
        Failed to load dashboard data
      </div>
    );
  }

  const totalRevenue = summary.total_revenue ?? "—";
  const alerts = summary.alerts?.length ?? 0;
  const avgDaily = summary.avg_daily_revenue ?? "—";
  const trend = summary.trend ?? [];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <h1 className="text-2xl font-bold">KPI Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <KPICard title="Total Revenue" value={totalRevenue} />
        <KPICard title="Alerts Detected" value={alerts} />
        <KPICard title="Avg Daily Revenue" value={avgDaily} />
      </div>

      <RevenueChart data={trend} />
    </motion.div>
  );
}
