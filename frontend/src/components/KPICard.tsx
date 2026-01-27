"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";

export function KPICard({
  title,
  value,
  subtitle,
}: {
  title: string;
  value: string | number;
  subtitle?: string;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
    >
      <Card className="p-6">
        <p className="text-sm text-muted-foreground">{title}</p>
        <div className="mt-2 text-3xl font-bold">{value}</div>
        {subtitle && (
          <p className="mt-1 text-xs text-muted-foreground">{subtitle}</p>
        )}
      </Card>
    </motion.div>
  );
}
