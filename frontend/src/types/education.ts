export interface EducationProgress {
  id: number;
  user_id: number;
  course_id: string;
  course_name: string;
  progress_percent: number;
  completed_modules: string[];
  created_at: string;
  updated_at: string;
}

export interface UpdateEducationProgressRequest {
  user_id: number;
  course_id: string;
  course_name: string;
  progress_percent: number;
  completed_modules: string[];
}

