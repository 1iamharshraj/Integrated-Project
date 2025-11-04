import apiClient from './client';
import type {
  KYCDocument,
  UploadKYCRequest,
  UpdateKYCStatusRequest,
} from '@/types/kyc';

export const kycApi = {
  getDocuments: async (userId: number): Promise<KYCDocument[]> => {
    const response = await apiClient.get(`/kyc/${userId}`);
    return response.data;
  },

  uploadDocument: async (data: UploadKYCRequest): Promise<KYCDocument> => {
    const response = await apiClient.post('/kyc', data);
    return response.data;
  },

  updateStatus: async (
    documentId: number,
    data: UpdateKYCStatusRequest
  ): Promise<KYCDocument> => {
    const response = await apiClient.put(`/kyc/${documentId}/verify`, data);
    return response.data;
  },
};

