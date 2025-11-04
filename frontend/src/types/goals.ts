export interface Goal {
  id: number;
  user_id: number;
  goal_name: string;
  target_amount: number;
  target_date: string;
  goal_type: 'retirement' | 'education' | 'house' | 'vacation' | 'emergency' | 'other';
  priority: 'high' | 'medium' | 'low';
  current_amount: number;
  created_at: string;
  updated_at: string;
}

export interface CreateGoalRequest {
  user_id: number;
  goal_name: string;
  target_amount: number;
  target_date: string;
  goal_type: 'retirement' | 'education' | 'house' | 'vacation' | 'emergency' | 'other';
  priority: 'high' | 'medium' | 'low';
}

export interface UpdateGoalRequest {
  goal_name?: string;
  target_amount?: number;
  target_date?: string;
  goal_type?: 'retirement' | 'education' | 'house' | 'vacation' | 'emergency' | 'other';
  priority?: 'high' | 'medium' | 'low';
}

export interface GoalProgress {
  goal: Goal;
  achievement_probability: number;
  recommended_monthly_contribution: number;
  projected_value: number;
  time_to_goal: number;
}

export interface GoalProgressResponse {
  goals: GoalProgress[];
  achievement_probability: number;
  recommended_allocations: {
    equity: number;
    debt: number;
    gold: number;
    international: number;
  };
}

