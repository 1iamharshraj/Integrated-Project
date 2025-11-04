export interface Transaction {
  id: number;
  user_id: number;
  portfolio_id?: number;
  type: 'buy' | 'sell' | 'deposit' | 'withdrawal';
  asset_name?: string;
  quantity?: number;
  price?: number;
  amount: number;
  status: 'pending' | 'completed' | 'failed' | 'cancelled';
  created_at: string;
  updated_at: string;
}

export interface CreateTransactionRequest {
  user_id: number;
  portfolio_id?: number;
  type: 'buy' | 'sell' | 'deposit' | 'withdrawal';
  asset_name?: string;
  quantity?: number;
  price?: number;
  amount: number;
  status?: 'pending' | 'completed' | 'failed' | 'cancelled';
}

export interface UpdateTransactionStatusRequest {
  status: 'pending' | 'completed' | 'failed' | 'cancelled';
}

export interface TransactionsResponse {
  transactions: Transaction[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

