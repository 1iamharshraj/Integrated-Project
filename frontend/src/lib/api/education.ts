import apiClient from './client';
import type {
  EducationProgress,
  UpdateEducationProgressRequest,
} from '@/types/education';

export const educationApi = {
  getProgress: async (userId: number): Promise<EducationProgress[]> => {
    const response = await apiClient.get(`/education/${userId}`);
    return response.data;
  },

  updateProgress: async (data: UpdateEducationProgressRequest): Promise<EducationProgress> => {
    const response = await apiClient.post('/education/progress', data);
    return response.data;
  },
};

