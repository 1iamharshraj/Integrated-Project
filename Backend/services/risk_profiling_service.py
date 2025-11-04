"""
Risk Profiling Service
Combines Q-Score (40%), G-Score (35%), B-Score (25%) from Project 25
Applies cultural modifiers from Project 29
"""

import json
from decimal import Decimal

class RiskProfilingService:
    """Service for risk profiling calculations"""
    
    @staticmethod
    def calculate_q_score(answers):
        """
        Calculate Q-Score from questionnaire answers
        Q-Score weight: 40%
        """
        # Placeholder implementation - replace with actual questionnaire logic
        # This should calculate based on risk tolerance questions
        total_score = 0
        max_score = 0
        
        for question_id, answer in answers.items():
            # Assume answers are scored 1-5 (1=very conservative, 5=very aggressive)
            if isinstance(answer, (int, float)):
                total_score += answer
                max_score += 5
        
        if max_score == 0:
            return 0.0
        
        q_score = (total_score / max_score) * 100
        return round(q_score, 2)
    
    @staticmethod
    def calculate_g_score(goals_data):
        """
        Calculate G-Score based on goals
        G-Score weight: 35%
        """
        # Placeholder implementation
        # G-Score considers goal timelines, amounts, and priorities
        if not goals_data or not isinstance(goals_data, list):
            return 50.0  # Default moderate score
        
        total_score = 0
        count = 0
        
        for goal in goals_data:
            # Short-term goals (less than 5 years) = higher risk tolerance
            # Long-term goals (10+ years) = can handle more risk
            years_to_goal = goal.get('years_to_goal', 5)
            if years_to_goal < 3:
                total_score += 30  # Conservative
            elif years_to_goal < 7:
                total_score += 50  # Moderate
            else:
                total_score += 70  # Aggressive
            count += 1
        
        if count == 0:
            return 50.0
        
        g_score = total_score / count
        return round(g_score, 2)
    
    @staticmethod
    def calculate_b_score(behavioral_data):
        """
        Calculate B-Score based on behavioral assessment
        B-Score weight: 25%
        """
        # Placeholder implementation
        # B-Score considers portfolio check frequency, turnover rate, life events
        if not behavioral_data:
            return 50.0
        
        score = 50.0  # Base score
        
        # Portfolio check frequency (high frequency = more risk-averse)
        check_freq = behavioral_data.get('portfolio_check_frequency', 1)
        if check_freq > 5:
            score -= 10  # More conservative
        elif check_freq < 2:
            score += 10  # More aggressive
        
        # Turnover rate (high turnover = more aggressive)
        turnover = behavioral_data.get('portfolio_turnover_rate', 0)
        if turnover > 0.5:
            score += 15
        elif turnover < 0.1:
            score -= 15
        
        # Life events (major events = more conservative)
        if behavioral_data.get('major_life_event_occurred', False):
            score -= 20
        
        # Clamp between 0 and 100
        score = max(0, min(100, score))
        return round(score, 2)
    
    @staticmethod
    def calculate_cultural_modifiers(demographics):
        """
        Calculate cultural modifiers from Project 29
        Base_modifier × Regional_factor × Demographic_factor × Tradition_factor
        """
        if not demographics:
            return {
                'base_modifier': 1.0,
                'regional_factor': 1.0,
                'demographic_factor': 1.0,
                'tradition_factor': 1.0,
                'cultural_modifier': 1.0
            }
        
        # Regional factors (based on Indian states/regions)
        region = demographics.get('region', '').lower()
        regional_factors = {
            'north': 0.95,  # More conservative
            'south': 1.05,  # Slightly more aggressive
            'east': 0.98,
            'west': 1.02,
            'central': 0.97
        }
        regional_factor = regional_factors.get(region, 1.0)
        
        # Demographic factors
        age = demographics.get('age', 35)
        income = demographics.get('income', 500000)
        
        # Age factor (younger = more risk-tolerant)
        if age < 30:
            age_factor = 1.05
        elif age < 45:
            age_factor = 1.0
        else:
            age_factor = 0.95
        
        # Income factor (higher income = more risk-tolerant)
        if income > 1000000:
            income_factor = 1.03
        elif income > 500000:
            income_factor = 1.0
        else:
            income_factor = 0.97
        
        demographic_factor = (age_factor + income_factor) / 2
        
        # Tradition factor
        joint_family = demographics.get('joint_family_status', False)
        gold_ratio = demographics.get('gold_investment_ratio', 0.1)
        real_estate_allocation = demographics.get('real_estate_allocation', 0.3)
        
        # Joint family = more conservative
        family_factor = 0.98 if joint_family else 1.0
        
        # High gold/real estate = more traditional = more conservative
        traditional_allocation = gold_ratio + real_estate_allocation
        if traditional_allocation > 0.5:
            tradition_factor = 0.95
        elif traditional_allocation > 0.3:
            tradition_factor = 0.98
        else:
            tradition_factor = 1.0
        
        tradition_factor = tradition_factor * family_factor
        
        # Base modifier
        base_modifier = 1.0
        
        # Calculate final cultural modifier
        cultural_modifier = base_modifier * regional_factor * demographic_factor * tradition_factor
        
        return {
            'base_modifier': base_modifier,
            'regional_factor': round(regional_factor, 4),
            'demographic_factor': round(demographic_factor, 4),
            'tradition_factor': round(tradition_factor, 4),
            'cultural_modifier': round(cultural_modifier, 4)
        }
    
    @staticmethod
    def calculate_comprehensive_risk_profile(q_score, g_score, b_score, cultural_modifiers):
        """
        Calculate comprehensive risk profile
        Final Score = (Q-Score × 0.4 + G-Score × 0.35 + B-Score × 0.25) × Cultural_Modifier
        """
        # Weighted combination
        base_score = (q_score * 0.4) + (g_score * 0.35) + (b_score * 0.25)
        
        # Apply cultural modifier
        cultural_modifier = cultural_modifiers.get('cultural_modifier', 1.0)
        final_score = base_score * cultural_modifier
        
        # Clamp to 0-100
        final_score = max(0, min(100, final_score))
        
        # Determine risk category
        if final_score < 30:
            risk_category = 'conservative'
        elif final_score < 70:
            risk_category = 'moderate'
        else:
            risk_category = 'aggressive'
        
        # Calculate confidence (based on how many factors we have)
        confidence = 0.8  # Base confidence
        if q_score is None or q_score == 0:
            confidence -= 0.2
        if g_score is None or g_score == 0:
            confidence -= 0.15
        if b_score is None or b_score == 0:
            confidence -= 0.1
        
        confidence = max(0.5, min(1.0, confidence))
        
        return {
            'risk_score': round(final_score, 2),
            'risk_category': risk_category,
            'confidence': round(confidence, 2),
            'factors': {
                'q_score': q_score,
                'g_score': g_score,
                'b_score': b_score,
                'cultural_modifier': cultural_modifier,
                'base_score': round(base_score, 2)
            }
        }

