import { create } from 'zustand';
import type {
  Portfolio,
  Holding,
  PortfolioPerformance,
} from '@/types/portfolio';
import { portfolioApi } from '@/lib/api/portfolio';

interface PortfolioState {
  portfolio: Portfolio | null;
  holdings: Holding[];
  performance: PortfolioPerformance | null;
  isLoading: boolean;
  error: string | null;
  fetchPortfolio: (userId: number) => Promise<void>;
  fetchPerformance: (userId: number) => Promise<void>;
  clearError: () => void;
}

export const usePortfolioStore = create<PortfolioState>((set, get) => ({
  portfolio: null,
  holdings: [],
  performance: null,
  isLoading: false,
  error: null,

  fetchPortfolio: async (userId: number) => {
    try {
      set({ isLoading: true, error: null });
      const response = await portfolioApi.getPortfolio(userId);
      set({
        portfolio: response.portfolio,
        holdings: response.holdings,
        performance: response.performance,
        isLoading: false,
      });
    } catch (error: any) {
      set({
        error: error.response?.data?.error || error.message || 'Failed to fetch portfolio',
        isLoading: false,
      });
    }
  },

  fetchPerformance: async (userId: number) => {
    try {
      set({ isLoading: true, error: null });
      const performance = await portfolioApi.getPerformance(userId);
      set({ performance, isLoading: false });
    } catch (error: any) {
      set({
        error: error.response?.data?.error || error.message || 'Failed to fetch performance',
        isLoading: false,
      });
    }
  },

  clearError: () => set({ error: null }),
}));

