'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth-store';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { goalsApi } from '@/lib/api/goals';
import type { GoalProgressResponse } from '@/types/goals';
import { formatCurrency, formatDate } from '@/lib/utils/format';
import { ArrowLeft, Target, TrendingUp } from 'lucide-react';

export default function GoalDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuthStore();
  const [goalProgress, setGoalProgress] = useState<GoalProgressResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (user?.id) {
      loadGoalProgress();
    }
  }, [user, params.id]);

  const loadGoalProgress = async () => {
    try {
      if (user?.id) {
        const progress = await goalsApi.getGoalProgress(user.id);
        const goal = progress.goals.find((g) => g.goal.id === Number(params.id));
        if (goal) {
          setGoalProgress({
            ...progress,
            goals: [goal],
          });
        }
      }
    } catch (error) {
      console.error('Failed to load goal progress:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  if (!goalProgress || goalProgress.goals.length === 0) {
    return (
      <div className="space-y-6">
        <Button variant="outline" onClick={() => router.back()}>
          <ArrowLeft className="mr-2 h-4 w-4" /> Back
        </Button>
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-muted-foreground">Goal not found</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const goalData = goalProgress.goals[0];
  const goal = goalData.goal;
  const progress = (goal.current_amount / goal.target_amount) * 100;
  const daysRemaining = Math.ceil(
    (new Date(goal.target_date).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" onClick={() => router.back()}>
          <ArrowLeft className="mr-2 h-4 w-4" /> Back
        </Button>
        <div>
          <h1 className="text-3xl font-bold">{goal.goal_name}</h1>
          <p className="text-muted-foreground">Goal details and progress</p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="portfolio-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Progress
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-muted-foreground">Current Amount</span>
                  <span className="font-medium">{formatCurrency(goal.current_amount)}</span>
                </div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-muted-foreground">Target Amount</span>
                  <span className="font-medium">{formatCurrency(goal.target_amount)}</span>
                </div>
                <Progress value={progress} className="h-3 mt-4" />
                <p className="text-center text-sm text-muted-foreground mt-2">
                  {progress.toFixed(1)}% Complete
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="portfolio-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Achievement Probability
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="text-center">
                <div className="text-4xl font-bold mb-2">
                  {(goalData.achievement_probability * 100).toFixed(1)}%
                </div>
                <p className="text-sm text-muted-foreground">
                  Probability of achieving this goal
                </p>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Recommended Monthly</span>
                  <span className="font-medium">
                    {formatCurrency(goalData.recommended_monthly_contribution)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Projected Value</span>
                  <span className="font-medium">{formatCurrency(goalData.projected_value)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Time to Goal</span>
                  <span className="font-medium">{goalData.time_to_goal} months</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Goal Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-sm text-muted-foreground">Goal Type</p>
              <p className="font-medium capitalize">{goal.goal_type.replace('_', ' ')}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Priority</p>
              <Badge>{goal.priority}</Badge>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Target Date</p>
              <p className="font-medium">{formatDate(goal.target_date)}</p>
              <p className="text-xs text-muted-foreground mt-1">
                {daysRemaining > 0 ? `${daysRemaining} days remaining` : 'Overdue'}
              </p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Created</p>
              <p className="font-medium">{formatDate(goal.created_at)}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {goalProgress.recommended_allocations && (
        <Card>
          <CardHeader>
            <CardTitle>Recommended Allocation</CardTitle>
            <CardDescription>AI-recommended portfolio allocation for this goal</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-4">
              <div>
                <p className="text-sm text-muted-foreground">Equity</p>
                <p className="text-2xl font-bold">
                  {(goalProgress.recommended_allocations.equity * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Debt</p>
                <p className="text-2xl font-bold">
                  {(goalProgress.recommended_allocations.debt * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Gold</p>
                <p className="text-2xl font-bold">
                  {(goalProgress.recommended_allocations.gold * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">International</p>
                <p className="text-2xl font-bold">
                  {(goalProgress.recommended_allocations.international * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

