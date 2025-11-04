import apiClient from './client';
import type {
  BehavioralMetrics,
  UpdateBehavioralMetricsRequest,
  BehavioralInsightsResponse,
} from '@/types/behavioral';

export const behavioralApi = {
  getMetrics: async (userId: number): Promise<BehavioralMetrics> => {
    const response = await apiClient.get(`/behavioral/metrics/${userId}`);
    return response.data;
  },

  updateMetrics: async (data: UpdateBehavioralMetricsRequest): Promise<BehavioralMetrics> => {
    const response = await apiClient.post('/behavioral/update', data);
    return response.data;
  },

  getInsights: async (userId: number): Promise<BehavioralInsightsResponse> => {
    const response = await apiClient.get(`/behavioral/insights/${userId}`);
    return response.data;
  },
};

