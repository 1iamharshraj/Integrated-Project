'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { useAuthStore } from '@/store/auth-store';
import { riskProfilingApi } from '@/lib/api/risk-profiling';
import { kycApi } from '@/lib/api/kyc';
import { Check, ChevronRight, ChevronLeft, Upload } from 'lucide-react';

const personalInfoSchema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  phone: z.string().optional(),
});

const questionnaireAnswers = {
  question_1: 3,
  question_2: 4,
  question_3: 2,
  question_4: 3,
  question_5: 4,
  question_6: 3,
  question_7: 2,
  question_8: 4,
  question_9: 3,
  question_10: 3,
};

const demographicsSchema = z.object({
  region: z.string().min(1, 'Region is required'),
  age: z.number().min(18).max(100),
  income: z.number().min(0),
  occupation: z.string().min(1, 'Occupation is required'),
  joint_family_status: z.boolean(),
  language_preference: z.string().min(1),
  religious_event_participation: z.boolean(),
  festival_spending: z.number().min(0),
  gold_investment_ratio: z.number().min(0).max(100),
  real_estate_allocation: z.number().min(0).max(100),
});

export default function OnboardingPage() {
  const router = useRouter();
  const { user, updateProfile } = useAuthStore();
  const [step, setStep] = useState(1);
  const [kycDocument, setKycDocument] = useState<File | null>(null);
  const totalSteps = 8;

  const personalForm = useForm({
    resolver: zodResolver(personalInfoSchema),
    defaultValues: {
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      phone: user?.phone || '',
    },
  });

  const demographicsForm = useForm({
    resolver: zodResolver(demographicsSchema),
    defaultValues: {
      region: '',
      age: 30,
      income: 0,
      occupation: '',
      joint_family_status: false,
      language_preference: 'english',
      religious_event_participation: false,
      festival_spending: 0,
      gold_investment_ratio: 0,
      real_estate_allocation: 0,
    },
  });

  const handleNext = async () => {
    if (step === 1) {
      const isValid = await personalForm.trigger();
      if (isValid) {
        const data = personalForm.getValues();
        await updateProfile(data);
        setStep(2);
      }
    } else if (step === 3) {
      // Skip KYC upload for now, can be implemented later
      setStep(4);
    } else if (step === 4) {
      try {
        await riskProfilingApi.submitQuestionnaire({ answers: questionnaireAnswers });
        setStep(5);
      } catch (error) {
        console.error('Questionnaire submission failed:', error);
      }
    } else if (step === 5) {
      const isValid = await demographicsForm.trigger();
      if (isValid) {
        const data = demographicsForm.getValues();
        try {
          await riskProfilingApi.submitDemographics(data);
          setStep(6);
        } catch (error) {
          console.error('Demographics submission failed:', error);
        }
      }
    } else if (step === 6) {
      try {
        await riskProfilingApi.submitBehavioral({
          behavioral_data: {
            portfolio_check_frequency: 'weekly',
            portfolio_turnover_rate: 0.2,
            major_life_event_occurred: false,
            investment_experience_years: 2,
            risk_tolerance_self_assessment: 5,
            emotional_reaction_to_losses: 'concerned',
            decision_making_style: 'analytical',
          },
        });
        setStep(7);
      } catch (error) {
        console.error('Behavioral submission failed:', error);
      }
    } else if (step === 7) {
      try {
        await riskProfilingApi.calculateRiskProfile();
        setStep(8);
      } catch (error) {
        console.error('Risk profile calculation failed:', error);
      }
    } else {
      setStep(step + 1);
    }
  };

  const handlePrevious = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleComplete = () => {
    router.push('/dashboard');
  };

  const progress = (step / totalSteps) * 100;

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background to-muted">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <div className="space-y-2">
            <CardTitle className="text-2xl">Complete Your Profile</CardTitle>
            <CardDescription>Step {step} of {totalSteps}</CardDescription>
            <Progress value={progress} className="h-2" />
          </div>
        </CardHeader>
        <CardContent>
          {/* Step 1: Personal Information */}
          {step === 1 && (
            <form onSubmit={personalForm.handleSubmit(handleNext)} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="first_name">First Name</Label>
                <Input
                  id="first_name"
                  {...personalForm.register('first_name')}
                />
                {personalForm.formState.errors.first_name && (
                  <p className="text-sm text-destructive">
                    {personalForm.formState.errors.first_name.message}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="last_name">Last Name</Label>
                <Input
                  id="last_name"
                  {...personalForm.register('last_name')}
                />
                {personalForm.formState.errors.last_name && (
                  <p className="text-sm text-destructive">
                    {personalForm.formState.errors.last_name.message}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone">Phone (Optional)</Label>
                <Input
                  id="phone"
                  type="tel"
                  {...personalForm.register('phone')}
                />
              </div>

              <div className="flex justify-end">
                <Button type="submit">
                  Next <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </form>
          )}

          {/* Step 2: Mobile Verification (Optional) */}
          {step === 2 && (
            <div className="space-y-4">
              <p className="text-muted-foreground">
                Mobile verification is optional. You can skip this step and verify later.
              </p>
              <div className="flex justify-between">
                <Button variant="outline" onClick={handlePrevious}>
                  <ChevronLeft className="mr-2 h-4 w-4" /> Previous
                </Button>
                <Button onClick={handleNext}>
                  Skip for Now <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: KYC Document Upload */}
          {step === 3 && (
            <div className="space-y-4">
              <div className="border-2 border-dashed rounded-lg p-8 text-center">
                <Upload className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                <Label htmlFor="kyc-upload" className="cursor-pointer">
                  <span className="text-primary hover:underline">Click to upload</span> or drag and drop
                </Label>
                <Input
                  id="kyc-upload"
                  type="file"
                  className="hidden"
                  accept=".pdf,.jpg,.jpeg,.png"
                  onChange={(e) => setKycDocument(e.target.files?.[0] || null)}
                />
                {kycDocument && (
                  <p className="mt-2 text-sm text-muted-foreground">
                    Selected: {kycDocument.name}
                  </p>
                )}
              </div>
              <div className="flex justify-between">
                <Button variant="outline" onClick={handlePrevious}>
                  <ChevronLeft className="mr-2 h-4 w-4" /> Previous
                </Button>
                <Button onClick={handleNext}>
                  Next <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 4: Risk Profiling Questionnaire */}
          {step === 4 && (
            <div className="space-y-4">
              <p className="text-muted-foreground">
                We'll use your answers to calculate your Q-Score (Questionnaire Score) for risk assessment.
              </p>
              <div className="space-y-2">
                <p className="text-sm">This step will automatically submit default questionnaire answers.</p>
              </div>
              <div className="flex justify-between">
                <Button variant="outline" onClick={handlePrevious}>
                  <ChevronLeft className="mr-2 h-4 w-4" /> Previous
                </Button>
                <Button onClick={handleNext}>
                  Continue <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 5: Demographics */}
          {step === 5 && (
            <form onSubmit={demographicsForm.handleSubmit(handleNext)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="region">Region</Label>
                  <Input id="region" {...demographicsForm.register('region')} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="age">Age</Label>
                  <Input
                    id="age"
                    type="number"
                    {...demographicsForm.register('age', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="income">Annual Income (₹)</Label>
                <Input
                  id="income"
                  type="number"
                  {...demographicsForm.register('income', { valueAsNumber: true })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="occupation">Occupation</Label>
                <Input id="occupation" {...demographicsForm.register('occupation')} />
              </div>

              <div className="space-y-2">
                <Label htmlFor="language_preference">Language Preference</Label>
                <Input id="language_preference" {...demographicsForm.register('language_preference')} />
              </div>

              <div className="flex justify-between">
                <Button variant="outline" onClick={handlePrevious}>
                  <ChevronLeft className="mr-2 h-4 w-4" /> Previous
                </Button>
                <Button type="submit">
                  Next <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </form>
          )}

          {/* Step 6: Behavioral Assessment */}
          {step === 6 && (
            <div className="space-y-4">
              <p className="text-muted-foreground">
                We'll analyze your behavioral patterns to calculate your B-Score.
              </p>
              <div className="flex justify-between">
                <Button variant="outline" onClick={handlePrevious}>
                  <ChevronLeft className="mr-2 h-4 w-4" /> Previous
                </Button>
                <Button onClick={handleNext}>
                  Continue <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 7: Calculate Risk Profile */}
          {step === 7 && (
            <div className="space-y-4">
              <p className="text-muted-foreground">
                Calculating your comprehensive risk profile based on Q-Score, G-Score, and B-Score...
              </p>
              <div className="flex justify-between">
                <Button variant="outline" onClick={handlePrevious}>
                  <ChevronLeft className="mr-2 h-4 w-4" /> Previous
                </Button>
                <Button onClick={handleNext}>
                  Calculate <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 8: Review & Complete */}
          {step === 8 && (
            <div className="space-y-4">
              <div className="flex items-center justify-center w-16 h-16 rounded-full bg-success/10 mx-auto mb-4">
                <Check className="h-8 w-8 text-success" />
              </div>
              <div className="text-center space-y-2">
                <h3 className="text-xl font-semibold">Profile Complete!</h3>
                <p className="text-muted-foreground">
                  Your risk profile has been calculated. You're all set to start using ZeTheta FinArcade.
                </p>
              </div>
              <div className="flex justify-center">
                <Button size="lg" onClick={handleComplete}>
                  Go to Dashboard
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
