export interface MarketIndex {
  name: string;
  value: number;
  change: number;
  change_percent: number;
  timestamp: string;
}

export interface MarketIndicesResponse {
  nifty_50: MarketIndex;
  sensex: MarketIndex;
  nifty_bank: MarketIndex;
}

export interface MarketSentiment {
  overall_sentiment: 'bullish' | 'bearish' | 'neutral';
  confidence: number;
  news_count: number;
  daily_sentiment_score: number;
}

export interface StockPrediction {
  symbol: string;
  expected_return: number;
  volatility: number;
  prediction_confidence: number;
  technical_indicators: {
    rsi: number;
    macd: number;
    sma_50: number;
    sma_200: number;
    bollinger_upper: number;
    bollinger_lower: number;
    support_level: number;
    resistance_level: number;
    [key: string]: number;
  };
}

export interface TechnicalIndicators {
  [key: string]: number;
}

export interface NewsArticle {
  id: number;
  title: string;
  content: string;
  source: string;
  url: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  sentiment_score: number;
  published_at: string;
}

export interface NewsResponse {
  articles: NewsArticle[];
  total: number;
  page: number;
  per_page: number;
}

