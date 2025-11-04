import apiClient from './client';
import type {
  AIInsightsResponse,
  RecommendationsRequest,
  RecommendationsResponse,
  StockPrediction,
} from '@/types/ai-insights';
import type { StockPrediction as MarketPrediction } from '@/types/market';

export const aiInsightsApi = {
  getInsights: async (
    userId: number,
    options?: { unread_only?: boolean; limit?: number }
  ): Promise<AIInsightsResponse> => {
    const params = new URLSearchParams();
    if (options?.unread_only) params.append('unread_only', 'true');
    if (options?.limit) params.append('limit', options.limit.toString());
    
    const response = await apiClient.get(`/ai/insights/${userId}?${params.toString()}`);
    return response.data;
  },

  getRecommendations: async (data: RecommendationsRequest): Promise<RecommendationsResponse> => {
    const response = await apiClient.post('/ai/recommendations', data);
    return response.data;
  },

  getPredictions: async (symbol: string): Promise<MarketPrediction> => {
    const response = await apiClient.get(`/ai/predictions/${symbol}`);
    return response.data;
  },

  markAsRead: async (insightId: number): Promise<{ message: string }> => {
    const response = await apiClient.post(`/ai/insights/mark-read/${insightId}`);
    return response.data;
  },
};

