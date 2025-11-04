import apiClient from './client';
import type {
  Goal,
  CreateGoalRequest,
  UpdateGoalRequest,
  GoalProgressResponse,
} from '@/types/goals';

export const goalsApi = {
  getGoals: async (userId: number): Promise<Goal[]> => {
    const response = await apiClient.get(`/goals/${userId}`);
    return response.data;
  },

  createGoal: async (data: CreateGoalRequest): Promise<Goal> => {
    const response = await apiClient.post('/goals/create', data);
    return response.data;
  },

  updateGoal: async (goalId: number, data: UpdateGoalRequest): Promise<Goal> => {
    const response = await apiClient.put(`/goals/${goalId}`, data);
    return response.data;
  },

  deleteGoal: async (goalId: number): Promise<{ message: string }> => {
    const response = await apiClient.delete(`/goals/${goalId}`);
    return response.data;
  },

  getGoalProgress: async (userId: number): Promise<GoalProgressResponse> => {
    const response = await apiClient.get(`/goals/progress/${userId}`);
    return response.data;
  },
};

