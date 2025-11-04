'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { formatCurrency, formatPercentage } from '@/lib/utils/format';
import { Wallet, TrendingUp, TrendingDown } from 'lucide-react';
import type { Portfolio, PortfolioPerformance } from '@/types/portfolio';

interface PortfolioSummaryProps {
  portfolio: Portfolio | null;
  performance: PortfolioPerformance | null;
}

export function PortfolioSummary({ portfolio, performance }: PortfolioSummaryProps) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card className="portfolio-card">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Value</CardTitle>
          <Wallet className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {portfolio ? formatCurrency(Number(portfolio.total_value)) : '₹0'}
          </div>
          {performance && (
            <p className={`text-xs mt-1 ${performance.total_gain_loss_percent >= 0 ? 'text-success' : 'text-destructive'}`}>
              {formatPercentage(performance.total_gain_loss_percent)}
            </p>
          )}
        </CardContent>
      </Card>

      <Card className="portfolio-card">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Gain/Loss</CardTitle>
          {performance?.total_gain_loss_percent && performance.total_gain_loss_percent >= 0 ? (
            <TrendingUp className="h-4 w-4 text-success" />
          ) : (
            <TrendingDown className="h-4 w-4 text-destructive" />
          )}
        </CardHeader>
        <CardContent>
          <div className={`text-2xl font-bold ${performance && performance.total_gain_loss >= 0 ? 'text-success' : 'text-destructive'}`}>
            {performance ? formatCurrency(Number(performance.total_gain_loss)) : '₹0'}
          </div>
          <p className="text-xs text-muted-foreground mt-1">Total return</p>
        </CardContent>
      </Card>

      <Card className="portfolio-card">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Return %</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className={`text-2xl font-bold ${performance && performance.total_gain_loss_percent >= 0 ? 'text-success' : 'text-destructive'}`}>
            {performance ? formatPercentage(performance.total_gain_loss_percent) : '0%'}
          </div>
          <p className="text-xs text-muted-foreground mt-1">Overall performance</p>
        </CardContent>
      </Card>
    </div>
  );
}

