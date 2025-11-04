'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { marketApi } from '@/lib/api/market';
import type { MarketIndicesResponse, MarketSentiment } from '@/types/market';
import { formatCurrency, formatPercentage } from '@/lib/utils/format';
import { TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';

export default function MarketPage() {
  const [indices, setIndices] = useState<MarketIndicesResponse | null>(null);
  const [sentiment, setSentiment] = useState<MarketSentiment | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadMarketData();
  }, []);

  const loadMarketData = async () => {
    try {
      const [indicesData, sentimentData] = await Promise.all([
        marketApi.getIndices(),
        marketApi.getSentiment(),
      ]);
      setIndices(indicesData);
      setSentiment(sentimentData);
    } catch (error) {
      console.error('Failed to load market data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Loading market data...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Market Data</h1>
        <p className="text-muted-foreground">Real-time market insights</p>
      </div>

      {sentiment && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Market Sentiment
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <Badge
                  variant={
                    sentiment.overall_sentiment === 'bullish'
                      ? 'success'
                      : sentiment.overall_sentiment === 'bearish'
                      ? 'destructive'
                      : 'default'
                  }
                  className="text-lg px-4 py-2"
                >
                  {sentiment.overall_sentiment.toUpperCase()}
                </Badge>
                <p className="text-sm text-muted-foreground mt-2">
                  Confidence: {(sentiment.confidence * 100).toFixed(1)}%
                </p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold">{sentiment.daily_sentiment_score.toFixed(2)}</p>
                <p className="text-sm text-muted-foreground">Daily Score</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {indices && (
        <div className="grid gap-6 md:grid-cols-3">
          {Object.entries(indices).map(([key, index]) => (
            <Card key={key} className="portfolio-card">
              <CardHeader>
                <CardTitle className="text-lg">{index.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="text-2xl font-bold">{formatCurrency(index.value)}</div>
                  <div className="flex items-center gap-2">
                    {index.change >= 0 ? (
                      <TrendingUp className="h-4 w-4 text-success" />
                    ) : (
                      <TrendingDown className="h-4 w-4 text-destructive" />
                    )}
                    <span
                      className={`text-sm font-medium ${
                        index.change >= 0 ? 'text-success' : 'text-destructive'
                      }`}
                    >
                      {formatPercentage(index.change_percent)}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {formatCurrency(Math.abs(index.change))}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
