export interface KYCDocument {
  id: number;
  user_id: number;
  document_type: 'aadhaar' | 'pan' | 'bank_statement';
  document_url: string;
  status: 'pending' | 'verified' | 'rejected';
  verified_at?: string;
  created_at: string;
}

export interface UploadKYCRequest {
  user_id: number;
  document_type: 'aadhaar' | 'pan' | 'bank_statement';
  document_url: string;
}

export interface UpdateKYCStatusRequest {
  status: 'pending' | 'verified' | 'rejected';
}

