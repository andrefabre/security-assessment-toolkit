#!/usr/bin/env python3
"""
Web Interface for Family Data Footprint Auditor
Flask-based web application for interactive assessments
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
from pathlib import Path
import sys

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.family_auditor import FamilyDataAuditor
from src.utils.logger import setup_logging

app = Flask(__name__, 
            template_folder='web_templates', 
            static_folder='web_static')

# Global variable to store current assessment
current_assessment = None
assessment_results = None

@app.route('/')
def index():
    """Home page with family setup"""
    return render_template('index.html')

@app.route('/api/start_assessment', methods=['POST'])
def start_assessment():
    """Start a new family assessment"""
    global current_assessment, assessment_results
    
    data = request.json
    family_name = data.get('family_name', 'Unknown Family')
    
    # Initialize the assessment
    current_assessment = FamilyDataAuditor(
        family_name=family_name,
        config_path="./config/default.json",
        output_dir="./reports"
    )
    
    return jsonify({
        'status': 'success',
        'message': f'Assessment started for {family_name}',
        'family_name': family_name
    })

@app.route('/api/add_member', methods=['POST'])
def add_member():
    """Add a family member to the assessment"""
    global current_assessment
    
    if not current_assessment:
        return jsonify({'status': 'error', 'message': 'No assessment started'})
    
    data = request.json
    member_name = data.get('member_name')
    age_group = data.get('age_group', 'adult')
    
    current_assessment.add_family_member(member_name, age_group)
    
    return jsonify({
        'status': 'success',
        'message': f'Added {member_name} to assessment'
    })

@app.route('/assessment/<member_name>')
def member_assessment(member_name):
    """Show assessment form for a specific member"""
    return render_template('member_assessment.html', member_name=member_name)

@app.route('/api/submit_member_assessment', methods=['POST'])
def submit_member_assessment():
    """Submit assessment responses for a member"""
    data = request.json
    member_name = data.get('member_name')
    responses = data.get('responses', {})
    
    # Store responses in session or database
    # For now, we'll just return success
    return jsonify({
        'status': 'success',
        'message': f'Assessment completed for {member_name}'
    })

@app.route('/api/run_assessment', methods=['POST'])
def run_assessment():
    """Run the complete family assessment"""
    global current_assessment, assessment_results
    
    if not current_assessment:
        return jsonify({'status': 'error', 'message': 'No assessment started'})
    
    try:
        # Run the assessment
        assessment_results = current_assessment.run_assessment()
        
        return jsonify({
            'status': 'success',
            'message': 'Assessment completed successfully',
            'report_path': assessment_results.get('report_path'),
            'results_summary': {
                'family_name': assessment_results.get('family_name'),
                'total_members': len(assessment_results.get('family_members', [])),
                'overall_risk': assessment_results.get('family_summary', {}).get('family_risk_profile', {}).get('overall_risk', 0)
            }
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Assessment failed: {str(e)}'
        })

@app.route('/results')
def show_results():
    """Show assessment results"""
    global assessment_results
    
    if not assessment_results:
        return "No assessment results available", 404
    
    return render_template('results.html', results=assessment_results)

@app.route('/api/get_questions/<category>')
def get_questions(category):
    """Get questions for a specific assessment category"""
    questions = {
        'social_media': [
            {
                'id': 'sm1',
                'question': 'Do you have accounts on Facebook, Instagram, or Twitter?',
                'type': 'multiple_choice',
                'options': ['None', '1-2 platforms', '3-5 platforms', '5+ platforms']
            },
            {
                'id': 'sm2', 
                'question': 'How often do you review your social media privacy settings?',
                'type': 'multiple_choice',
                'options': ['Never', 'Rarely', 'Every few months', 'Monthly', 'Weekly']
            },
            {
                'id': 'sm3',
                'question': 'Do you share personal information (location, workplace, family details) on social media?',
                'type': 'multiple_choice',
                'options': ['Frequently', 'Sometimes', 'Rarely', 'Never']
            },
            {
                'id': 'sm4',
                'question': 'Are your social media profiles set to private?',
                'type': 'multiple_choice',
                'options': ['All public', 'Mostly public', 'Mixed', 'Mostly private', 'All private']
            }
        ],
        'privacy_settings': [
            {
                'id': 'ps1',
                'question': 'Do you use privacy-focused web browsers or extensions?',
                'type': 'multiple_choice',
                'options': ['No privacy tools', 'Basic ad blockers', 'Privacy extensions', 'Privacy-focused browser', 'Advanced privacy setup']
            },
            {
                'id': 'ps2',
                'question': 'How do you manage passwords?',
                'type': 'multiple_choice',
                'options': ['Same password everywhere', 'Few different passwords', 'Many unique passwords', 'Password manager', 'Password manager + 2FA']
            },
            {
                'id': 'ps3',
                'question': 'Do you review app permissions on your mobile devices?',
                'type': 'multiple_choice',
                'options': ['Never', 'When installing', 'Sometimes', 'Regularly', 'Very frequently']
            }
        ],
        'data_exposure': [
            {
                'id': 'de1',
                'question': 'Have you checked if your email appears in data breaches?',
                'type': 'multiple_choice',
                'options': ['Never checked', 'Checked once', 'Check occasionally', 'Monitor regularly']
            },
            {
                'id': 'de2',
                'question': 'Do you receive unwanted marketing emails or calls?',
                'type': 'multiple_choice',
                'options': ['Constantly', 'Frequently', 'Sometimes', 'Rarely', 'Never']
            },
            {
                'id': 'de3',
                'question': 'How much personal information can someone find about you online?',
                'type': 'multiple_choice',
                'options': ['Everything', 'A lot', 'Some basics', 'Very little', 'Almost nothing']
            }
        ]
    }
    
    return jsonify(questions.get(category, []))

if __name__ == '__main__':
    # Setup logging
    setup_logging(verbose=True)
    
    # Create necessary directories
    Path('web_templates').mkdir(exist_ok=True)
    Path('web_static').mkdir(exist_ok=True)
    Path('reports').mkdir(exist_ok=True)
    
    print("Starting Family Data Footprint Auditor Web Interface...")
    print("Open your browser to: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)