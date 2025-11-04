import apiClient from './client';
import type {
  QuestionnaireRequest,
  QuestionnaireResponse,
  DemographicsRequest,
  DemographicsResponse,
  LifeEventsRequest,
  LifeEventsResponse,
  BehavioralRequest,
  BehavioralResponse,
  CalculateRiskProfileResponse,
  RiskProfile,
} from '@/types/risk-profile';

export const riskProfilingApi = {
  submitQuestionnaire: async (data: QuestionnaireRequest): Promise<QuestionnaireResponse> => {
    const response = await apiClient.post('/risk-profiling/questionnaire', data);
    return response.data;
  },

  submitDemographics: async (data: DemographicsRequest): Promise<DemographicsResponse> => {
    const response = await apiClient.post('/risk-profiling/demographics', data);
    return response.data;
  },

  submitLifeEvents: async (data: LifeEventsRequest): Promise<LifeEventsResponse> => {
    const response = await apiClient.post('/risk-profiling/life-events', data);
    return response.data;
  },

  submitBehavioral: async (data: BehavioralRequest): Promise<BehavioralResponse> => {
    const response = await apiClient.post('/risk-profiling/behavioral', data);
    return response.data;
  },

  calculateRiskProfile: async (): Promise<CalculateRiskProfileResponse> => {
    const response = await apiClient.post('/risk-profiling/calculate');
    return response.data;
  },

  getRiskProfile: async (userId: number): Promise<RiskProfile> => {
    const response = await apiClient.get(`/risk-profiling/profile/${userId}`);
    return response.data;
  },
};

