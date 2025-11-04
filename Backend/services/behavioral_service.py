"""
Behavioral Service
Behavioral analytics and insights
"""

from datetime import datetime, timedelta

class BehavioralService:
    """Service for behavioral analytics"""
    
    @staticmethod
    def analyze_behavioral_metrics(behavioral_data):
        """Analyze behavioral metrics and generate insights"""
        insights = []
        recommendations = []
        risk_adjustments = {}
        
        # Portfolio check frequency analysis
        check_freq = behavioral_data.get('portfolio_check_frequency', 0)
        if check_freq > 5:
            insights.append({
                'type': 'warning',
                'message': 'High portfolio check frequency detected. Consider reducing to avoid emotional decision-making.',
                'severity': 'medium'
            })
            risk_adjustments['check_frequency_impact'] = -0.05  # Reduce risk tolerance
        
        # Turnover rate analysis
        turnover_rate = float(behavioral_data.get('portfolio_turnover_rate', 0))
        if turnover_rate > 0.5:
            insights.append({
                'type': 'warning',
                'message': 'High portfolio turnover rate. Frequent trading may reduce returns due to transaction costs.',
                'severity': 'high'
            })
            recommendations.append({
                'action': 'reduce_trading',
                'reason': 'High turnover rate detected',
                'priority': 'high'
            })
        
        # Life events impact
        if behavioral_data.get('major_life_event_occurred', False):
            insights.append({
                'type': 'info',
                'message': 'Major life event detected. Consider reviewing your risk profile and investment strategy.',
                'severity': 'medium'
            })
            risk_adjustments['life_event_impact'] = -0.10  # Reduce risk tolerance
        
        # Sentiment variance analysis
        sentiment_variance = float(behavioral_data.get('sentiment_variance', 0))
        if sentiment_variance > 0.3:
            insights.append({
                'type': 'warning',
                'message': 'High sentiment variance detected. Consider adopting a more systematic investment approach.',
                'severity': 'medium'
            })
        
        # Email tone analysis
        email_tone_ratio = float(behavioral_data.get('email_tone_positive_ratio', 0.5))
        if email_tone_ratio < 0.3:
            insights.append({
                'type': 'info',
                'message': 'Negative sentiment detected in communications. Consider reviewing your investment strategy.',
                'severity': 'low'
            })
        
        # Market volatility reaction
        reaction = behavioral_data.get('reaction_to_market_volatility', 'moderate')
        if reaction == 'aggressive':
            recommendations.append({
                'action': 'review_risk_tolerance',
                'reason': 'Aggressive reaction to volatility may indicate need for risk profile adjustment',
                'priority': 'medium'
            })
        
        return {
            'insights': insights,
            'recommendations': recommendations,
            'risk_adjustments': risk_adjustments
        }
    
    @staticmethod
    def calculate_behavioral_score(behavioral_data):
        """Calculate behavioral risk score"""
        score = 50.0  # Base score
        
        # Adjust based on various factors
        check_freq = behavioral_data.get('portfolio_check_frequency', 1)
        if check_freq > 5:
            score -= 5
        
        turnover = float(behavioral_data.get('portfolio_turnover_rate', 0))
        if turnover > 0.5:
            score += 10  # High turnover = more aggressive
        
        if behavioral_data.get('major_life_event_occurred', False):
            score -= 10
        
        # Clamp to 0-100
        score = max(0, min(100, score))
        return round(score, 2)

