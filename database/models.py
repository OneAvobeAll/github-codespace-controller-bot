"""Database models for MongoDB"""
from datetime import datetime
from typing import Dict, List, Optional


class User:
    """
    User model for storing user information and settings
    """
    collection_name = 'users'
    
    @staticmethod
    def schema():
        return {
            'user_id': int,
            'username': str,
            'first_name': str,
            'last_name': str,
            'github_tokens': [
                {
                    '_id': str,  # Token ID
                    'token': str,
                    'is_active': bool,
                    'added_at': datetime,
                    'last_used': datetime
                }
            ],
            'applications': [str],  # Application IDs
            'billing_alerts': bool,
            'usage_limits': {
                'monthly_hours': int,
                'monthly_storage_gb': int,
            },
            'created_at': datetime,
            'updated_at': datetime,
        }


class Application:
    """
    Application model for storing application configurations
    """
    collection_name = 'applications'
    
    @staticmethod
    def schema():
        return {
            '_id': str,  # Application ID
            'user_id': int,
            'name': str,
            'repo_url': str,  # GitHub repository URL
            'forked_repo': str,  # Forked repository name
            'env_vars': {
                # KEY: value pairs
            },
            'build_command': str,
            'start_command': str,
            'docker_enabled': bool,
            'docker_file': str,  # Path to Dockerfile if exists
            'status': str,  # 'active', 'stopped', 'error'
            'codespace_id': str,
            'codespace_name': str,
            'machine_type': str,  # 'small', 'medium', 'large', 'xlarge'
            'created_at': datetime,
            'updated_at': datetime,
            'last_started': datetime,
            'last_stopped': datetime,
        }


class Codespace:
    """
    Codespace model for tracking active Codespaces
    """
    collection_name = 'codespaces'
    
    @staticmethod
    def schema():
        return {
            '_id': str,  # Codespace ID from GitHub
            'user_id': int,
            'app_id': str,
            'codespace_name': str,
            'repo_name': str,
            'branch': str,
            'state': str,  # 'Available', 'In Progress', 'Failed'
            'web_url': str,
            'machine_type': str,
            'created_at': datetime,
            'started_at': datetime,
            'last_used_at': datetime,
            'retention_period_minutes': int,
        }


class BillingLog:
    """
    Billing and usage log model
    """
    collection_name = 'billing_logs'
    
    @staticmethod
    def schema():
        return {
            'user_id': int,
            'app_id': str,
            'codespace_id': str,
            'action': str,  # 'started', 'stopped', 'created', 'deleted'
            'machine_type': str,
            'duration_minutes': int,
            'cost': float,
            'timestamp': datetime,
        }
