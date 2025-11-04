import apiClient from './client';
import type { MarketSentiment, NewsResponse } from '@/types/market';

export const newsApi = {
  scrapeNews: async (): Promise<{ message: string }> => {
    const response = await apiClient.post('/news/scrape');
    return response.data;
  },

  getSentiment: async (options?: { limit?: number; date?: string }): Promise<MarketSentiment & { articles?: any[] }> => {
    const params = new URLSearchParams();
    if (options?.limit) params.append('limit', options.limit.toString());
    if (options?.date) params.append('date', options.date);
    
    const response = await apiClient.get(`/news/sentiment?${params.toString()}`);
    return response.data;
  },
};

