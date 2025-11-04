export interface Holding {
  id: number;
  portfolio_id: number;
  asset_type: 'equity' | 'debt' | 'gold' | 'international';
  asset_name: string;
  quantity: number;
  current_price: number;
  purchase_price: number;
  allocation: number;
  ai_recommendation?: 'buy' | 'hold' | 'sell';
  created_at: string;
  updated_at: string;
}

export interface Portfolio {
  id: number;
  user_id: number;
  total_value: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  last_updated: string;
}

export interface PortfolioResponse {
  portfolio: Portfolio;
  holdings: Holding[];
  performance: PortfolioPerformance;
}

export interface PortfolioPerformance {
  total_value: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  asset_allocation: {
    equity: number;
    debt: number;
    gold: number;
    international: number;
  };
  returns_by_asset: {
    equity: number;
    debt: number;
    gold: number;
    international: number;
  };
}

export interface OptimizePortfolioRequest {
  user_id: number;
  risk_category: 'conservative' | 'moderate' | 'aggressive' | 'very_aggressive';
  investment_amount: number;
  goals?: Array<{
    goal_name: string;
    target_amount: number;
    target_date: string;
  }>;
}

export interface OptimizePortfolioResponse {
  allocation: {
    equity: number;
    debt: number;
    gold: number;
    international: number;
  };
  expected_return: number;
  risk_metrics: {
    volatility: number;
    sharpe_ratio: number;
    max_drawdown: number;
  };
  behavioral_adjustments: Record<string, any>;
}

export interface RebalancePortfolioRequest {
  user_id: number;
  target_allocation: {
    equity: number;
    debt: number;
    gold: number;
    international: number;
  };
}

export interface RebalancePortfolioResponse {
  recommendations: Array<{
    action: 'buy' | 'sell';
    asset_type: string;
    asset_name?: string;
    amount: number;
    reason: string;
  }>;
  current_value: number;
}

export interface AddHoldingRequest {
  portfolio_id: number;
  asset_type: 'equity' | 'debt' | 'gold' | 'international';
  asset_name: string;
  quantity: number;
  current_price: number;
  purchase_price: number;
  allocation: number;
  ai_recommendation?: 'buy' | 'hold' | 'sell';
}

