import apiClient from './client';
import type {
  TransactionsResponse,
  CreateTransactionRequest,
  Transaction,
  UpdateTransactionStatusRequest,
} from '@/types/transactions';

export const transactionsApi = {
  getTransactions: async (
    userId: number,
    options?: { page?: number; per_page?: number; type?: string; status?: string }
  ): Promise<TransactionsResponse> => {
    const params = new URLSearchParams();
    if (options?.page) params.append('page', options.page.toString());
    if (options?.per_page) params.append('per_page', options.per_page.toString());
    if (options?.type) params.append('type', options.type);
    if (options?.status) params.append('status', options.status);
    
    const response = await apiClient.get(`/transactions/${userId}?${params.toString()}`);
    return response.data;
  },

  createTransaction: async (data: CreateTransactionRequest): Promise<Transaction> => {
    const response = await apiClient.post('/transactions', data);
    return response.data;
  },

  updateStatus: async (
    transactionId: number,
    data: UpdateTransactionStatusRequest
  ): Promise<Transaction> => {
    const response = await apiClient.put(`/transactions/${transactionId}/status`, data);
    return response.data;
  },
};

