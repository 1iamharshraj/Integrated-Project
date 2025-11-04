import apiClient from './client';
import type {
  PortfolioResponse,
  OptimizePortfolioRequest,
  OptimizePortfolioResponse,
  RebalancePortfolioRequest,
  RebalancePortfolioResponse,
  AddHoldingRequest,
  PortfolioPerformance,
} from '@/types/portfolio';

export const portfolioApi = {
  getPortfolio: async (userId: number): Promise<PortfolioResponse> => {
    const response = await apiClient.get(`/portfolio/${userId}`);
    return response.data;
  },

  optimizePortfolio: async (data: OptimizePortfolioRequest): Promise<OptimizePortfolioResponse> => {
    const response = await apiClient.post('/portfolio/optimize', data);
    return response.data;
  },

  rebalancePortfolio: async (data: RebalancePortfolioRequest): Promise<RebalancePortfolioResponse> => {
    const response = await apiClient.post('/portfolio/rebalance', data);
    return response.data;
  },

  getPerformance: async (userId: number): Promise<PortfolioPerformance> => {
    const response = await apiClient.get(`/portfolio/performance/${userId}`);
    return response.data;
  },

  addHolding: async (data: AddHoldingRequest): Promise<{ message: string; holding: any }> => {
    const response = await apiClient.post('/portfolio/holdings', data);
    return response.data;
  },

  deleteHolding: async (holdingId: number): Promise<{ message: string }> => {
    const response = await apiClient.delete(`/portfolio/holdings/${holdingId}`);
    return response.data;
  },
};

