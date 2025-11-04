'use client';

import { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/auth-store';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { riskProfilingApi } from '@/lib/api/risk-profiling';
import type { RiskProfile } from '@/types/risk-profile';
import { Target, TrendingUp, AlertCircle } from 'lucide-react';
import Link from 'next/link';

export default function RiskProfilingPage() {
  const { user } = useAuthStore();
  const [riskProfile, setRiskProfile] = useState<RiskProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (user?.id) {
      loadRiskProfile();
    }
  }, [user]);

  const loadRiskProfile = async () => {
    try {
      if (user?.id) {
        const profile = await riskProfilingApi.getRiskProfile(user.id);
        setRiskProfile(profile);
      }
    } catch (error) {
      console.error('Failed to load risk profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getRiskCategoryColor = (category: string) => {
    switch (category) {
      case 'conservative':
        return 'bg-blue-500';
      case 'moderate':
        return 'bg-yellow-500';
      case 'aggressive':
        return 'bg-orange-500';
      case 'very_aggressive':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  if (!riskProfile) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Risk Profiling</h1>
          <p className="text-muted-foreground">Complete your risk assessment</p>
        </div>
        <Card>
          <CardContent className="py-12 text-center">
            <AlertCircle className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-xl font-semibold mb-2">No Risk Profile Found</h3>
            <p className="text-muted-foreground mb-6">
              Complete the onboarding process to generate your risk profile.
            </p>
            <Button asChild>
              <Link href="/onboarding">Start Onboarding</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Risk Profiling</h1>
        <p className="text-muted-foreground">Your comprehensive risk assessment</p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="portfolio-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Risk Score
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold mb-2">{riskProfile.risk_score}</div>
            <Badge className={getRiskCategoryColor(riskProfile.risk_category)}>
              {riskProfile.risk_category.replace('_', ' ').toUpperCase()}
            </Badge>
            <div className="mt-4">
              <Progress value={riskProfile.risk_score} className="h-2" />
            </div>
          </CardContent>
        </Card>

        <Card className="portfolio-card">
          <CardHeader>
            <CardTitle>Q-Score</CardTitle>
            <CardDescription>Questionnaire Score</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{riskProfile.q_score?.toFixed(1) || 'N/A'}</div>
            <p className="text-sm text-muted-foreground mt-2">Based on questionnaire answers</p>
          </CardContent>
        </Card>

        <Card className="portfolio-card">
          <CardHeader>
            <CardTitle>Confidence</CardTitle>
            <CardDescription>Profile Confidence Level</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{riskProfile.confidence?.toFixed(0) || 'N/A'}%</div>
            <p className="text-sm text-muted-foreground mt-2">Assessment confidence</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Score Breakdown</CardTitle>
          <CardDescription>Detailed component scores</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Q-Score</span>
                <span className="text-sm font-bold">{riskProfile.q_score?.toFixed(1) || 'N/A'}</span>
              </div>
              <Progress value={riskProfile.q_score || 0} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">G-Score</span>
                <span className="text-sm font-bold">{riskProfile.g_score?.toFixed(1) || 'N/A'}</span>
              </div>
              <Progress value={riskProfile.g_score || 0} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">B-Score</span>
                <span className="text-sm font-bold">{riskProfile.b_score?.toFixed(1) || 'N/A'}</span>
              </div>
              <Progress value={riskProfile.b_score || 0} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Cultural Modifier</span>
                <span className="text-sm font-bold">{riskProfile.cultural_modifier?.toFixed(2) || 'N/A'}</span>
              </div>
              <Progress value={(riskProfile.cultural_modifier || 0) * 10} className="h-2" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <Button variant="outline" asChild>
              <Link href="/risk-profiling/questionnaire">Retake Questionnaire</Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/risk-profiling/demographics">Update Demographics</Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/risk-profiling/behavioral">Update Behavioral Assessment</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
