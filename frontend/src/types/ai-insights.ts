export interface AIInsight {
  id: number;
  user_id: number;
  type: 'portfolio_optimization' | 'risk_adjustment' | 'market_opportunity' | 'goal_tracking' | 'behavioral_insight' | 'other';
  title: string;
  content: string;
  data?: Record<string, any>;
  is_read: boolean;
  created_at: string;
}

export interface AIInsightsResponse {
  insights: AIInsight[];
  count: number;
}

export interface Recommendation {
  type: string;
  title: string;
  content: string;
  confidence: number;
  priority: 'high' | 'medium' | 'low';
  action_items: string[];
}

export interface RecommendationsRequest {
  user_id: number;
}

export interface RecommendationsResponse {
  recommendations: Recommendation[];
  confidence_scores: Record<string, number>;
  reasoning: string;
}

