'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  TrendingUp, 
  Shield, 
  Zap, 
  Brain, 
  Target, 
  BarChart3, 
  BookOpen,
  Check,
  ArrowRight,
  Star,
  Users,
  Award
} from 'lucide-react';

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="hero-section relative py-20 md:py-32">
        <div className="container px-4 mx-auto relative z-10">
          <div className="max-w-3xl mx-auto text-center space-y-8">
            <Badge className="mb-4">India's First AI-Driven Investment Platform</Badge>
            <h1 className="text-4xl md:text-6xl font-bold text-white">
              Invest Smarter with AI-Powered Advisory
            </h1>
            <p className="text-xl md:text-2xl text-white/90">
              ZeTheta FinArcade combines cutting-edge AI with behavioral insights to optimize your investment strategy
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link href="/register">Get Started Free</Link>
              </Button>
              <Button size="lg" variant="outline" className="bg-white/10 text-white border-white/20 hover:bg-white/20" asChild>
                <Link href="/dashboard">View Dashboard</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="py-12 bg-muted/50">
        <div className="container px-4 mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary">₹50Cr+</div>
              <div className="text-sm text-muted-foreground mt-1">Assets Managed</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">10K+</div>
              <div className="text-sm text-muted-foreground mt-1">Active Users</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">98%</div>
              <div className="text-sm text-muted-foreground mt-1">Accuracy Rate</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">24/7</div>
              <div className="text-sm text-muted-foreground mt-1">AI Monitoring</div>
            </div>
          </div>
        </div>
      </section>

      {/* AI Features */}
      <section className="py-20">
        <div className="container px-4 mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">AI-Powered Features</h2>
            <p className="text-muted-foreground text-lg">
              Everything you need for intelligent investment management
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Brain className="w-8 h-8" />,
                title: 'AI Risk Profiling',
                description: 'Comprehensive risk assessment using Q-Score, G-Score, and B-Score with cultural modifiers',
              },
              {
                icon: <TrendingUp className="w-8 h-8" />,
                title: 'Portfolio Optimization',
                description: 'Automated portfolio rebalancing based on your risk profile and investment goals',
              },
              {
                icon: <Shield className="w-8 h-8" />,
                title: 'Behavioral Analytics',
                description: 'Track and adjust for behavioral biases in your investment decisions',
              },
              {
                icon: <Target className="w-8 h-8" />,
                title: 'Goal-Based Planning',
                description: 'Monte Carlo simulations to achieve your financial goals with confidence',
              },
              {
                icon: <BarChart3 className="w-8 h-8" />,
                title: 'Market Predictions',
                description: 'AI-powered market sentiment analysis and stock predictions',
              },
              {
                icon: <Zap className="w-8 h-8" />,
                title: 'Real-time Insights',
                description: 'Get instant AI recommendations and alerts for portfolio adjustments',
              },
            ].map((feature, index) => (
              <Card key={index} className="feature-card">
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary mb-4">
                    {feature.icon}
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{feature.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Dashboard Preview */}
      <section className="py-20 bg-muted/30">
        <div className="container px-4 mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Your Investment Dashboard</h2>
            <p className="text-muted-foreground text-lg">
              Everything you need to manage your investments in one place
            </p>
          </div>
          <Card className="dashboard-card">
            <CardContent className="p-8">
              <div className="grid md:grid-cols-3 gap-6">
                <div className="space-y-2">
                  <div className="text-sm text-muted-foreground">Portfolio Value</div>
                  <div className="text-2xl font-bold">₹12,45,000</div>
                  <div className="text-sm text-success">+12.5%</div>
                </div>
                <div className="space-y-2">
                  <div className="text-sm text-muted-foreground">Risk Profile</div>
                  <div className="text-2xl font-bold">Moderate</div>
                  <div className="text-sm text-muted-foreground">Score: 65</div>
                </div>
                <div className="space-y-2">
                  <div className="text-sm text-muted-foreground">Active Goals</div>
                  <div className="text-2xl font-bold">3</div>
                  <div className="text-sm text-muted-foreground">On Track</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Education Section */}
      <section className="py-20">
        <div className="container px-4 mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Learn & Grow</h2>
            <p className="text-muted-foreground text-lg">
              Comprehensive financial education to make informed decisions
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: 'Investment Basics',
                description: 'Learn the fundamentals of investing',
                progress: 75,
              },
              {
                title: 'Risk Management',
                description: 'Understand and manage investment risks',
                progress: 50,
              },
              {
                title: 'Portfolio Optimization',
                description: 'Master portfolio construction and rebalancing',
                progress: 30,
              },
            ].map((course, index) => (
              <Card key={index} className="education-card">
                <CardHeader>
                  <CardTitle>{course.title}</CardTitle>
                  <CardDescription>{course.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progress</span>
                      <span>{course.progress}%</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div
                        className="bg-primary h-2 rounded-full transition-all"
                        style={{ width: `${course.progress}%` }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-muted/30">
        <div className="container px-4 mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Simple, Transparent Pricing</h2>
            <p className="text-muted-foreground text-lg">
              Choose the plan that works for you
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              {
                name: 'Starter',
                price: 'Free',
                period: 'First Year',
                features: [
                  'AI-powered portfolio management',
                  'Up to ₹1 Lakh investment',
                  'Basic educational resources',
                  'Email support',
                ],
                buttonText: 'Get Started',
                buttonVariant: 'outline' as const,
              },
              {
                name: 'Professional',
                price: '₹499',
                period: 'per month',
                features: [
                  'Everything in Starter',
                  'Unlimited investment',
                  'Advanced AI analytics',
                  'Tax loss harvesting',
                  'Priority support',
                ],
                buttonText: 'Start Professional',
                buttonVariant: 'default' as const,
                popular: true,
              },
              {
                name: 'Enterprise',
                price: '₹999',
                period: 'per month',
                features: [
                  'Everything in Professional',
                  'Dedicated AI advisor',
                  'Alternative investments',
                  '24/7 phone support',
                  'Quarterly reviews',
                ],
                buttonText: 'Contact Sales',
                buttonVariant: 'outline' as const,
              },
            ].map((plan, index) => (
              <Card key={index} className={`pricing-card ${plan.popular ? 'featured ring-2 ring-primary' : ''}`}>
                {plan.popular && (
                  <div className="pricing-badge">Most Popular</div>
                )}
                <CardHeader>
                  <CardTitle>{plan.name}</CardTitle>
                  <div className="mt-4">
                    <span className="text-4xl font-bold">{plan.price}</span>
                    <span className="text-muted-foreground">/{plan.period}</span>
                  </div>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3 mb-6">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <Check className="w-5 h-5 text-success" />
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Button variant={plan.buttonVariant} className="w-full" size="lg">
                    {plan.buttonText}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 hero-section">
        <div className="container px-4 mx-auto text-center relative z-10">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Start Your Investment Journey?
          </h2>
          <p className="text-xl text-white/90 mb-8">
            Join thousands of investors who trust ZeTheta FinArcade
          </p>
          <Button size="lg" variant="secondary" asChild>
            <Link href="/register">
              Get Started Free
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
