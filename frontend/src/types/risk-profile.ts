export interface RiskProfile {
  id: number;
  user_id: number;
  q_score: number;
  g_score: number;
  b_score: number;
  risk_score: number;
  risk_category: 'conservative' | 'moderate' | 'aggressive' | 'very_aggressive';
  confidence: number;
  cultural_modifier: number;
  base_score: number;
  created_at: string;
  updated_at: string;
}

export interface QuestionnaireRequest {
  answers: Record<string, number>;
}

export interface QuestionnaireResponse {
  q_score: number;
  risk_score: number;
  message: string;
}

export interface DemographicsRequest {
  region: string;
  age: number;
  income: number;
  occupation: string;
  joint_family_status: boolean;
  language_preference: string;
  religious_event_participation: boolean;
  festival_spending: number;
  gold_investment_ratio: number;
  real_estate_allocation: number;
}

export interface DemographicsResponse {
  base_modifier: number;
  regional_factor: number;
  demographic_factor: number;
  tradition_factor: number;
  cultural_modifier: number;
}

export interface LifeEvent {
  event_type: string;
  impact: 'positive' | 'neutral' | 'negative';
  date: string;
}

export interface LifeEventsRequest {
  life_events: LifeEvent[];
}

export interface LifeEventsResponse {
  life_event_impact: number;
  adjusted_risk_score: number;
}

export interface BehavioralData {
  portfolio_check_frequency: 'daily' | 'weekly' | 'monthly' | 'rarely';
  portfolio_turnover_rate: number;
  major_life_event_occurred: boolean;
  investment_experience_years: number;
  risk_tolerance_self_assessment: number;
  emotional_reaction_to_losses: 'calm' | 'concerned' | 'anxious' | 'panicked';
  decision_making_style: 'analytical' | 'intuitive' | 'emotional';
}

export interface BehavioralRequest {
  behavioral_data: BehavioralData;
}

export interface BehavioralResponse {
  b_score: number;
  behavioral_insights: string[];
}

export interface CalculateRiskProfileResponse {
  risk_score: number;
  risk_category: 'conservative' | 'moderate' | 'aggressive' | 'very_aggressive';
  confidence: number;
  factors: {
    q_score: number;
    g_score: number;
    b_score: number;
    cultural_modifier: number;
    base_score: number;
  };
}

