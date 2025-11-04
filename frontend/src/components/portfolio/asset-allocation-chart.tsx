'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import type { PortfolioPerformance } from '@/types/portfolio';

interface AssetAllocationChartProps {
  performance: PortfolioPerformance | null;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

export function AssetAllocationChart({ performance }: AssetAllocationChartProps) {
  if (!performance?.asset_allocation) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Asset Allocation</CardTitle>
          <CardDescription>Portfolio allocation by asset type</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">No allocation data available</div>
        </CardContent>
      </Card>
    );
  }

  const data = [
    { name: 'Equity', value: performance.asset_allocation.equity },
    { name: 'Debt', value: performance.asset_allocation.debt },
    { name: 'Gold', value: performance.asset_allocation.gold },
    { name: 'International', value: performance.asset_allocation.international },
  ].filter(item => item.value > 0);

  return (
    <Card className="dashboard-card">
      <CardHeader>
        <CardTitle>Asset Allocation</CardTitle>
        <CardDescription>Portfolio allocation by asset type</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

