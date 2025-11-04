'use client';

import { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/auth-store';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { behavioralApi } from '@/lib/api/behavioral';
import type { BehavioralMetrics, BehavioralInsightsResponse } from '@/types/behavioral';
import { TrendingUp, Brain, AlertCircle } from 'lucide-react';

export default function BehavioralPage() {
  const { user } = useAuthStore();
  const [metrics, setMetrics] = useState<BehavioralMetrics | null>(null);
  const [insights, setInsights] = useState<BehavioralInsightsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (user?.id) {
      loadBehavioralData();
    }
  }, [user]);

  const loadBehavioralData = async () => {
    try {
      if (user?.id) {
        const [metricsData, insightsData] = await Promise.all([
          behavioralApi.getMetrics(user.id),
          behavioralApi.getInsights(user.id),
        ]);
        setMetrics(metricsData);
        setInsights(insightsData);
      }
    } catch (error) {
      console.error('Failed to load behavioral data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Behavioral Analytics</h1>
        <p className="text-muted-foreground">Track your investment behavior</p>
      </div>

      {metrics && (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <Card className="portfolio-card">
            <CardHeader>
              <CardTitle className="text-sm">Portfolio Check Frequency</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metrics.portfolio_check_frequency}</div>
            </CardContent>
          </Card>

          <Card className="portfolio-card">
            <CardHeader>
              <CardTitle className="text-sm">Trade Volume</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metrics.trade_volume.toFixed(2)}</div>
            </CardContent>
          </Card>

          <Card className="portfolio-card">
            <CardHeader>
              <CardTitle className="text-sm">Nudge Acceptance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {(metrics.nudge_acceptance_rate * 100).toFixed(1)}%
              </div>
            </CardContent>
          </Card>

          <Card className="portfolio-card">
            <CardHeader>
              <CardTitle className="text-sm">Sentiment Avg</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metrics.sentiment_avg.toFixed(2)}</div>
            </CardContent>
          </Card>
        </div>
      )}

      {insights && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                Insights
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {insights.insights.map((insight, index) => (
                  <li key={index} className="text-sm flex items-start gap-2">
                    <AlertCircle className="h-4 w-4 text-muted-foreground mt-0.5" />
                    {insight}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {insights.recommendations.map((rec, index) => (
                  <li key={index} className="text-sm flex items-start gap-2">
                    <AlertCircle className="h-4 w-4 text-primary mt-0.5" />
                    {rec}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
