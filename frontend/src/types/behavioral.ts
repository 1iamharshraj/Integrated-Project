export interface BehavioralMetrics {
  user_id: number;
  portfolio_check_frequency: number;
  trade_volume: number;
  life_event: boolean;
  sentiment_avg: number;
  sentiment_variance: number;
  email_tone_positive_ratio: number;
  calendar_stress_events_count: number;
  nudge_acceptance_rate: number;
  reaction_to_market_volatility: number;
  updated_at: string;
}

export interface UpdateBehavioralMetricsRequest {
  user_id: number;
  portfolio_check_frequency?: number;
  trade_volume?: number;
  life_event?: boolean;
  sentiment_avg?: number;
  sentiment_variance?: number;
  email_tone_positive_ratio?: number;
  calendar_stress_events_count?: number;
  nudge_acceptance_rate?: number;
  reaction_to_market_volatility?: number;
}

export interface BehavioralInsight {
  insight: string;
  recommendation: string;
  risk_adjustment: number;
}

export interface BehavioralInsightsResponse {
  insights: string[];
  recommendations: string[];
  risk_adjustments: Record<string, number>;
}

