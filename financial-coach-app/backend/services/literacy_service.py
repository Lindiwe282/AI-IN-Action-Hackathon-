import random
from datetime import datetime, timedelta

class LiteracyService:
    def __init__(self):
        self.tips_database = {
            'budgeting': [
                {
                    'title': 'The 50/30/20 Rule',
                    'content': 'Allocate 50% of income to needs, 30% to wants, and 20% to savings and debt repayment.',
                    'difficulty': 'beginner',
                    'category': 'budgeting'
                },
                {
                    'title': 'Track Your Expenses',
                    'content': 'Monitor where your money goes for at least one month to identify spending patterns.',
                    'difficulty': 'beginner',
                    'category': 'budgeting'
                },
                {
                    'title': 'Zero-Based Budgeting',
                    'content': 'Assign every dollar a purpose so your income minus expenses equals zero.',
                    'difficulty': 'intermediate',
                    'category': 'budgeting'
                }
            ],
            'saving': [
                {
                    'title': 'Pay Yourself First',
                    'content': 'Set up automatic transfers to savings before you have a chance to spend the money.',
                    'difficulty': 'beginner',
                    'category': 'saving'
                },
                {
                    'title': 'Emergency Fund Goal',
                    'content': 'Aim to save 3-6 months of living expenses for unexpected situations.',
                    'difficulty': 'beginner',
                    'category': 'saving'
                },
                {
                    'title': 'High-Yield Savings Accounts',
                    'content': 'Use high-yield savings accounts to earn more interest on your emergency fund.',
                    'difficulty': 'intermediate',
                    'category': 'saving'
                }
            ],
            'investing': [
                {
                    'title': 'Start Early with Compound Interest',
                    'content': 'Time is your biggest ally in investing. Start as early as possible to benefit from compound interest.',
                    'difficulty': 'beginner',
                    'category': 'investing'
                },
                {
                    'title': 'Diversification is Key',
                    'content': 'Don\'t put all your eggs in one basket. Spread investments across different asset classes.',
                    'difficulty': 'intermediate',
                    'category': 'investing'
                },
                {
                    'title': 'Dollar-Cost Averaging',
                    'content': 'Invest a fixed amount regularly regardless of market conditions to reduce timing risk.',
                    'difficulty': 'intermediate',
                    'category': 'investing'
                }
            ],
            'debt': [
                {
                    'title': 'Pay More Than Minimum',
                    'content': 'Always pay more than the minimum payment on credit cards to reduce interest charges.',
                    'difficulty': 'beginner',
                    'category': 'debt'
                },
                {
                    'title': 'Debt Avalanche Method',
                    'content': 'Focus on paying off debts with the highest interest rates first to minimize total interest paid.',
                    'difficulty': 'intermediate',
                    'category': 'debt'
                },
                {
                    'title': 'Debt Snowball Method',
                    'content': 'Pay off smallest debts first for psychological wins and momentum.',
                    'difficulty': 'beginner',
                    'category': 'debt'
                }
            ]
        }
        
        self.quiz_questions = [
            {
                'question': 'What percentage of your income should ideally go to savings?',
                'options': ['5%', '10%', '20%', '30%'],
                'correct_answer': 2,
                'explanation': 'Financial experts recommend saving at least 20% of your income.',
                'category': 'saving'
            },
            {
                'question': 'What is compound interest?',
                'options': [
                    'Interest earned only on the principal amount',
                    'Interest earned on both principal and previously earned interest',
                    'Interest that compounds monthly',
                    'Interest that never changes'
                ],
                'correct_answer': 1,
                'explanation': 'Compound interest is earned on both the original principal and the accumulated interest from previous periods.',
                'category': 'investing'
            },
            {
                'question': 'How many months of expenses should you have in an emergency fund?',
                'options': ['1-2 months', '3-6 months', '8-10 months', '12 months'],
                'correct_answer': 1,
                'explanation': 'Most financial experts recommend having 3-6 months of living expenses in an emergency fund.',
                'category': 'saving'
            }
        ]
    
    def get_personalized_tips(self, user_preferences):
        """Get personalized financial literacy tips"""
        try:
            # Extract user preferences
            experience_level = user_preferences.get('experience_level', 'beginner').lower()
            interests = user_preferences.get('interests', ['budgeting', 'saving'])
            daily_tips = user_preferences.get('daily_tips', True)
            
            personalized_tips = []
            
            # Get tips based on interests and experience level
            for interest in interests:
                if interest in self.tips_database:
                    category_tips = [
                        tip for tip in self.tips_database[interest]
                        if tip['difficulty'] == experience_level or experience_level == 'all'
                    ]
                    personalized_tips.extend(category_tips[:2])  # Limit to 2 per category
            
            # Add daily tip if requested
            if daily_tips:
                daily_tip = self._get_daily_tip(experience_level)
                personalized_tips.insert(0, daily_tip)
            
            # Add learning path recommendations
            learning_path = self._generate_learning_path(experience_level, interests)
            
            return {
                'personalized_tips': personalized_tips,
                'learning_path': learning_path,
                'recommended_resources': self._get_recommended_resources(interests),
                'next_steps': self._get_next_steps(experience_level, interests)
            }
            
        except Exception as e:
            raise Exception(f"Error getting personalized tips: {str(e)}")
    
    def _get_daily_tip(self, experience_level):
        """Get tip of the day"""
        all_tips = []
        for category_tips in self.tips_database.values():
            all_tips.extend([
                tip for tip in category_tips
                if tip['difficulty'] == experience_level or experience_level == 'all'
            ])
        
        if all_tips:
            tip = random.choice(all_tips)
            tip['is_daily_tip'] = True
            return tip
        
        return {
            'title': 'Daily Financial Wisdom',
            'content': 'The best time to start investing was 20 years ago. The second best time is now.',
            'difficulty': 'beginner',
            'category': 'general',
            'is_daily_tip': True
        }
    
    def _generate_learning_path(self, experience_level, interests):
        """Generate personalized learning path"""
        learning_paths = {
            'beginner': [
                {'step': 1, 'topic': 'Basic Budgeting', 'estimated_time': '1 week'},
                {'step': 2, 'topic': 'Emergency Fund Building', 'estimated_time': '2 weeks'},
                {'step': 3, 'topic': 'Debt Management', 'estimated_time': '2 weeks'},
                {'step': 4, 'topic': 'Introduction to Investing', 'estimated_time': '3 weeks'},
                {'step': 5, 'topic': 'Retirement Planning Basics', 'estimated_time': '2 weeks'}
            ],
            'intermediate': [
                {'step': 1, 'topic': 'Advanced Budgeting Strategies', 'estimated_time': '1 week'},
                {'step': 2, 'topic': 'Investment Diversification', 'estimated_time': '2 weeks'},
                {'step': 3, 'topic': 'Tax Optimization', 'estimated_time': '2 weeks'},
                {'step': 4, 'topic': 'Real Estate Investing', 'estimated_time': '3 weeks'},
                {'step': 5, 'topic': 'Advanced Retirement Strategies', 'estimated_time': '2 weeks'}
            ],
            'advanced': [
                {'step': 1, 'topic': 'Portfolio Management', 'estimated_time': '2 weeks'},
                {'step': 2, 'topic': 'Alternative Investments', 'estimated_time': '3 weeks'},
                {'step': 3, 'topic': 'Estate Planning', 'estimated_time': '2 weeks'},
                {'step': 4, 'topic': 'Business Finance', 'estimated_time': '3 weeks'},
                {'step': 5, 'topic': 'Advanced Tax Strategies', 'estimated_time': '2 weeks'}
            ]
        }
        
        return learning_paths.get(experience_level, learning_paths['beginner'])
    
    def _get_recommended_resources(self, interests):
        """Get recommended educational resources"""
        resources = {
            'budgeting': [
                {
                    'type': 'book',
                    'title': 'You Need A Budget',
                    'author': 'Jesse Mecham',
                    'description': 'Practical budgeting methodology'
                },
                {
                    'type': 'app',
                    'title': 'Mint',
                    'description': 'Free budgeting and expense tracking app'
                }
            ],
            'investing': [
                {
                    'type': 'book',
                    'title': 'The Bogleheads Guide to Investing',
                    'author': 'Taylor Larimore',
                    'description': 'Simple, effective investment strategies'
                },
                {
                    'type': 'website',
                    'title': 'Investopedia',
                    'description': 'Comprehensive investment education'
                }
            ],
            'saving': [
                {
                    'type': 'book',
                    'title': 'The Automatic Millionaire',
                    'author': 'David Bach',
                    'description': 'Automated saving strategies'
                }
            ],
            'debt': [
                {
                    'type': 'book',
                    'title': 'The Total Money Makeover',
                    'author': 'Dave Ramsey',
                    'description': 'Step-by-step debt elimination plan'
                }
            ]
        }
        
        recommended = []
        for interest in interests:
            if interest in resources:
                recommended.extend(resources[interest])
        
        return recommended
    
    def _get_next_steps(self, experience_level, interests):
        """Get recommended next steps"""
        next_steps = []
        
        if 'budgeting' in interests:
            if experience_level == 'beginner':
                next_steps.append({
                    'action': 'Create your first budget',
                    'description': 'Use the 50/30/20 rule to allocate your income',
                    'priority': 'high'
                })
            else:
                next_steps.append({
                    'action': 'Optimize your budget',
                    'description': 'Review and adjust your budget categories for better efficiency',
                    'priority': 'medium'
                })
        
        if 'saving' in interests:
            next_steps.append({
                'action': 'Set up automatic savings',
                'description': 'Automate transfers to your savings account',
                'priority': 'high'
            })
        
        if 'investing' in interests:
            if experience_level == 'beginner':
                next_steps.append({
                    'action': 'Open an investment account',
                    'description': 'Consider a low-cost brokerage account for index fund investing',
                    'priority': 'medium'
                })
            else:
                next_steps.append({
                    'action': 'Review your portfolio allocation',
                    'description': 'Ensure your investments align with your risk tolerance',
                    'priority': 'medium'
                })
        
        return next_steps
    
    def evaluate_quiz(self, quiz_data):
        """Evaluate financial literacy quiz"""
        try:
            answers = quiz_data.get('answers', [])
            selected_questions = quiz_data.get('questions', [])
            
            if not answers or not selected_questions:
                # Provide default quiz questions if none selected
                selected_questions = self.quiz_questions[:3]
            
            results = []
            correct_count = 0
            
            for i, question in enumerate(selected_questions):
                if i < len(answers):
                    user_answer = answers[i]
                    is_correct = user_answer == question['correct_answer']
                    if is_correct:
                        correct_count += 1
                    
                    results.append({
                        'question': question['question'],
                        'user_answer': question['options'][user_answer] if 0 <= user_answer < len(question['options']) else 'No answer',
                        'correct_answer': question['options'][question['correct_answer']],
                        'is_correct': is_correct,
                        'explanation': question['explanation'],
                        'category': question['category']
                    })
            
            score_percentage = (correct_count / len(selected_questions)) * 100 if selected_questions else 0
            
            # Generate personalized feedback
            feedback = self._generate_quiz_feedback(score_percentage, results)
            
            return {
                'score': correct_count,
                'total_questions': len(selected_questions),
                'score_percentage': score_percentage,
                'results': results,
                'feedback': feedback,
                'recommended_learning': self._get_learning_recommendations_from_quiz(results)
            }
            
        except Exception as e:
            raise Exception(f"Error evaluating quiz: {str(e)}")
    
    def _generate_quiz_feedback(self, score_percentage, results):
        """Generate personalized feedback based on quiz results"""
        if score_percentage >= 90:
            overall_feedback = "Excellent! You have a strong understanding of financial concepts."
        elif score_percentage >= 70:
            overall_feedback = "Good job! You have a solid foundation but there's room for improvement."
        elif score_percentage >= 50:
            overall_feedback = "You're on the right track, but consider reviewing some key concepts."
        else:
            overall_feedback = "Don't worry - everyone starts somewhere! Focus on learning the basics."
        
        # Category-specific feedback
        categories_missed = {}
        for result in results:
            if not result['is_correct']:
                category = result['category']
                categories_missed[category] = categories_missed.get(category, 0) + 1
        
        specific_feedback = []
        for category, count in categories_missed.items():
            specific_feedback.append(f"Review {category} concepts - missed {count} question(s)")
        
        return {
            'overall': overall_feedback,
            'specific': specific_feedback,
            'grade': self._get_grade(score_percentage)
        }
    
    def _get_grade(self, score_percentage):
        """Convert percentage to letter grade"""
        if score_percentage >= 90:
            return 'A'
        elif score_percentage >= 80:
            return 'B'
        elif score_percentage >= 70:
            return 'C'
        elif score_percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    def _get_learning_recommendations_from_quiz(self, results):
        """Get learning recommendations based on quiz performance"""
        weak_categories = []
        
        category_performance = {}
        for result in results:
            category = result['category']
            if category not in category_performance:
                category_performance[category] = {'correct': 0, 'total': 0}
            
            category_performance[category]['total'] += 1
            if result['is_correct']:
                category_performance[category]['correct'] += 1
        
        # Identify categories where performance is below 70%
        for category, performance in category_performance.items():
            accuracy = (performance['correct'] / performance['total']) * 100
            if accuracy < 70:
                weak_categories.append(category)
        
        recommendations = []
        for category in weak_categories:
            if category in self.tips_database:
                category_tips = self.tips_database[category][:2]  # Get first 2 tips
                recommendations.extend(category_tips)
        
        return recommendations
    
    def get_resources(self, query_params):
        """Get educational resources based on query parameters"""
        try:
            resource_type = query_params.get('type', 'all')
            category = query_params.get('category', 'all')
            difficulty = query_params.get('difficulty', 'all')
            
            all_resources = [
                {
                    'type': 'book',
                    'title': 'Rich Dad Poor Dad',
                    'author': 'Robert Kiyosaki',
                    'category': 'general',
                    'difficulty': 'beginner',
                    'description': 'Fundamental concepts about money and investing'
                },
                {
                    'type': 'book',
                    'title': 'The Intelligent Investor',
                    'author': 'Benjamin Graham',
                    'category': 'investing',
                    'difficulty': 'advanced',
                    'description': 'Classic guide to value investing'
                },
                {
                    'type': 'website',
                    'title': 'Khan Academy Personal Finance',
                    'url': 'https://www.khanacademy.org/economics-finance-domain/core-finance',
                    'category': 'general',
                    'difficulty': 'beginner',
                    'description': 'Free online courses on personal finance'
                },
                {
                    'type': 'podcast',
                    'title': 'The Dave Ramsey Show',
                    'category': 'debt',
                    'difficulty': 'beginner',
                    'description': 'Daily advice on money and debt management'
                },
                {
                    'type': 'app',
                    'title': 'Personal Capital',
                    'category': 'investing',
                    'difficulty': 'intermediate',
                    'description': 'Investment tracking and financial planning'
                }
            ]
            
            # Filter resources based on query parameters
            filtered_resources = all_resources
            
            if resource_type != 'all':
                filtered_resources = [r for r in filtered_resources if r['type'] == resource_type]
            
            if category != 'all':
                filtered_resources = [r for r in filtered_resources if r['category'] == category]
            
            if difficulty != 'all':
                filtered_resources = [r for r in filtered_resources if r['difficulty'] == difficulty]
            
            return {
                'resources': filtered_resources,
                'total_count': len(filtered_resources),
                'categories_available': list(set(r['category'] for r in all_resources)),
                'types_available': list(set(r['type'] for r in all_resources))
            }
            
        except Exception as e:
            raise Exception(f"Error getting resources: {str(e)}")