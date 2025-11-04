'use client';

import { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/auth-store';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { aiInsightsApi } from '@/lib/api/ai-insights';
import type { AIInsight } from '@/types/ai-insights';
import { formatRelativeTime } from '@/lib/utils/format';
import { Brain, CheckCircle, Circle } from 'lucide-react';

export default function AIInsightsPage() {
  const { user } = useAuthStore();
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');

  useEffect(() => {
    if (user?.id) {
      loadInsights();
    }
  }, [user, filter]);

  const loadInsights = async () => {
    try {
      if (user?.id) {
        const response = await aiInsightsApi.getInsights(user.id, {
          unread_only: filter === 'unread',
        });
        setInsights(response.insights);
      }
    } catch (error) {
      console.error('Failed to load insights:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const markAsRead = async (insightId: number) => {
    try {
      await aiInsightsApi.markAsRead(insightId);
      await loadInsights();
    } catch (error) {
      console.error('Failed to mark as read:', error);
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'portfolio_optimization':
        return 'default';
      case 'risk_adjustment':
        return 'warning';
      case 'market_opportunity':
        return 'success';
      default:
        return 'default';
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Loading insights...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">AI Insights</h1>
          <p className="text-muted-foreground">AI-powered recommendations</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant={filter === 'all' ? 'default' : 'outline'}
            onClick={() => setFilter('all')}
          >
            All
          </Button>
          <Button
            variant={filter === 'unread' ? 'default' : 'outline'}
            onClick={() => setFilter('unread')}
          >
            Unread
          </Button>
        </div>
      </div>

      {insights.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <Brain className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-xl font-semibold mb-2">No Insights Yet</h3>
            <p className="text-muted-foreground">
              AI insights will appear here as your portfolio grows.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {insights.map((insight) => (
            <Card key={insight.id} className="portfolio-card">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant={getTypeColor(insight.type) as any}>
                        {insight.type.replace('_', ' ')}
                      </Badge>
                      {insight.is_read ? (
                        <CheckCircle className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <Circle className="h-4 w-4 text-primary" />
                      )}
                    </div>
                    <CardTitle>{insight.title}</CardTitle>
                    <CardDescription>
                      {formatRelativeTime(insight.created_at)}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm mb-4">{insight.content}</p>
                {!insight.is_read && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => markAsRead(insight.id)}
                  >
                    Mark as Read
                  </Button>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
