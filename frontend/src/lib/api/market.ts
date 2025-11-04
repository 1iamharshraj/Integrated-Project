import apiClient from './client';
import type {
  MarketIndicesResponse,
  MarketSentiment,
  StockPrediction,
  TechnicalIndicators,
  NewsResponse,
} from '@/types/market';

export const marketApi = {
  getIndices: async (): Promise<MarketIndicesResponse> => {
    const response = await apiClient.get('/market/indices');
    return response.data;
  },

  getSentiment: async (): Promise<MarketSentiment> => {
    const response = await apiClient.get('/market/sentiment');
    return response.data;
  },

  getPredictions: async (symbol: string): Promise<StockPrediction> => {
    const response = await apiClient.get(`/market/predictions/${symbol}`);
    return response.data;
  },

  getNews: async (): Promise<NewsResponse> => {
    const response = await apiClient.get('/market/news');
    return response.data;
  },

  getTechnicalIndicators: async (symbol: string): Promise<TechnicalIndicators> => {
    const response = await apiClient.get(`/market/technical-indicators/${symbol}`);
    return response.data;
  },
};

