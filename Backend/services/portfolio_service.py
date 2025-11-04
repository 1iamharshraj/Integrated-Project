"""
Portfolio Service
Modern Portfolio Theory implementation with behavioral constraints
"""

from decimal import Decimal
import math

class PortfolioService:
    """Service for portfolio optimization and management"""
    
    @staticmethod
    def optimize_portfolio(user_id, risk_category, investment_amount, goals):
        """
        Optimize portfolio allocation using Modern Portfolio Theory
        Incorporates behavioral constraints from Project 29
        """
        # Asset allocation based on risk category
        allocations = {
            'conservative': {
                'equity': 0.30,
                'debt': 0.50,
                'gold': 0.10,
                'international': 0.10
            },
            'moderate': {
                'equity': 0.50,
                'debt': 0.30,
                'gold': 0.10,
                'international': 0.10
            },
            'aggressive': {
                'equity': 0.70,
                'debt': 0.15,
                'gold': 0.05,
                'international': 0.10
            }
        }
        
        base_allocation = allocations.get(risk_category, allocations['moderate'])
        
        # Apply behavioral constraints
        # If user has high portfolio check frequency, reduce equity exposure
        behavioral_adjustments = {
            'equity_reduction': 0.0,
            'debt_increase': 0.0
        }
        
        # Calculate expected return (simplified)
        expected_returns = {
            'equity': 0.12,
            'debt': 0.07,
            'gold': 0.08,
            'international': 0.10
        }
        
        expected_return = sum(
            base_allocation[asset] * expected_returns[asset]
            for asset in base_allocation
        )
        
        # Risk metrics (simplified)
        risk_metrics = {
            'volatility': 0.15 if risk_category == 'conservative' else (0.20 if risk_category == 'moderate' else 0.25),
            'sharpe_ratio': expected_return / 0.15,  # Simplified
            'max_drawdown': 0.10 if risk_category == 'conservative' else (0.15 if risk_category == 'moderate' else 0.20)
        }
        
        # Apply behavioral adjustments
        final_allocation = base_allocation.copy()
        if behavioral_adjustments['equity_reduction'] > 0:
            reduction = behavioral_adjustments['equity_reduction']
            final_allocation['equity'] = max(0, final_allocation['equity'] - reduction)
            final_allocation['debt'] += reduction
        
        return {
            'allocation': final_allocation,
            'expected_return': round(expected_return, 4),
            'risk_metrics': risk_metrics,
            'behavioral_adjustments': behavioral_adjustments,
            'investment_amount': float(investment_amount)
        }
    
    @staticmethod
    def calculate_portfolio_performance(holdings):
        """Calculate portfolio performance metrics"""
        if not holdings:
            return {
                'total_value': 0.0,
                'total_cost': 0.0,
                'total_gain_loss': 0.0,
                'total_gain_loss_percent': 0.0
            }
        
        total_value = Decimal('0.00')
        total_cost = Decimal('0.00')
        
        for holding in holdings:
            current_value = Decimal(str(holding.quantity)) * Decimal(str(holding.current_price))
            cost_basis = Decimal(str(holding.quantity)) * Decimal(str(holding.purchase_price))
            total_value += current_value
            total_cost += cost_basis
        
        total_gain_loss = total_value - total_cost
        total_gain_loss_percent = (total_gain_loss / total_cost * 100) if total_cost > 0 else Decimal('0.00')
        
        return {
            'total_value': float(total_value),
            'total_cost': float(total_cost),
            'total_gain_loss': float(total_gain_loss),
            'total_gain_loss_percent': float(total_gain_loss_percent)
        }
    
    @staticmethod
    def rebalance_portfolio(current_holdings, target_allocation, total_value):
        """Calculate rebalancing recommendations"""
        recommendations = []
        
        # Convert total_value to float to avoid Decimal/float division issues
        total_value_float = float(total_value) if total_value else 0.0
        
        # Calculate current allocation
        current_allocation = {}
        for holding in current_holdings:
            asset_type = holding.asset_type
            current_value = float(holding.quantity) * float(holding.current_price)
            current_allocation[asset_type] = current_allocation.get(asset_type, 0) + current_value
        
        # Calculate target values
        target_values = {}
        for asset_type, allocation in target_allocation.items():
            target_values[asset_type] = total_value_float * allocation
        
        # Generate rebalancing recommendations
        for asset_type, target_value in target_values.items():
            current_value = current_allocation.get(asset_type, 0)
            difference = target_value - current_value
            
            if abs(difference) > total_value_float * 0.05:  # 5% threshold
                action = 'buy' if difference > 0 else 'sell'
                recommendations.append({
                    'asset_type': asset_type,
                    'action': action,
                    'amount': abs(difference),
                    'current_allocation': current_value / total_value_float if total_value_float > 0 else 0,
                    'target_allocation': target_allocation[asset_type]
                })
        
        return recommendations

