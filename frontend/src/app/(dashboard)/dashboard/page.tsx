'use client';

import { useEffect } from 'react';
import { useAuthStore } from '@/store/auth-store';
import { usePortfolioStore } from '@/store/portfolio-store';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { formatCurrency, formatPercentage } from '@/lib/utils/format';
import { TrendingUp, TrendingDown, Wallet, Target, Brain } from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { portfolio, holdings, performance, fetchPortfolio, isLoading } = usePortfolioStore();

  useEffect(() => {
    if (user?.id) {
      fetchPortfolio(user.id);
    }
  }, [user, fetchPortfolio]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back, {user?.first_name}!
        </p>
      </div>

      {/* Portfolio Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="portfolio-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Portfolio Value</CardTitle>
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
            <CardTitle className="text-sm font-medium">Total Gain/Loss</CardTitle>
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
            <p className="text-xs text-muted-foreground mt-1">
              {holdings.length} holdings
            </p>
          </CardContent>
        </Card>

        <Card className="portfolio-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Goals</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground mt-1">
              Create your first goal
            </p>
          </CardContent>
        </Card>

        <Card className="portfolio-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Insights</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground mt-1">
              New recommendations
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Holdings Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Holdings</CardTitle>
          <CardDescription>Your portfolio holdings</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Loading...</div>
          ) : holdings.length > 0 ? (
            <div className="space-y-4">
              {holdings.slice(0, 5).map((holding) => {
                const gainLoss = (holding.current_price - holding.purchase_price) * holding.quantity;
                const gainLossPercent = ((holding.current_price - holding.purchase_price) / holding.purchase_price) * 100;

                return (
                  <div key={holding.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <div className="font-medium">{holding.asset_name}</div>
                      <div className="text-sm text-muted-foreground">
                        {holding.asset_type} • {holding.quantity} units
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">{formatCurrency(holding.current_price * holding.quantity)}</div>
                      <div className={`text-sm ${gainLoss >= 0 ? 'text-success' : 'text-destructive'}`}>
                        {formatPercentage(gainLossPercent)}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              No holdings yet. Add your first holding to get started.
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

