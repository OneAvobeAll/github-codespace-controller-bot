"""Utility functions for the bot"""
import re
import logging
from typing import Dict, List, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def parse_github_url(url: str) -> Optional[Dict[str, str]]:
    """
    Parse GitHub repository URL and extract owner and repo name
    
    Supports formats:
    - https://github.com/owner/repo
    - https://github.com/owner/repo.git
    - git@github.com:owner/repo.git
    """
    try:
        url = url.strip()
        
        # Remove .git suffix if present
        if url.endswith('.git'):
            url = url[:-4]
        
        # Handle HTTPS URLs
        if url.startswith('https://github.com/'):
            parts = url.split('/')
            if len(parts) >= 5:
                return {
                    'owner': parts[3],
                    'repo': parts[4],
                    'url': url
                }
        
        # Handle SSH URLs
        if url.startswith('git@github.com:'):
            parts = url.replace('git@github.com:', '').split('/')
            if len(parts) >= 2:
                return {
                    'owner': parts[0],
                    'repo': parts[1],
                    'url': url
                }
        
        return None
    
    except Exception as e:
        logger.error(f"Error parsing GitHub URL: {str(e)}")
        return None


def validate_env_var_format(env_string: str) -> Optional[Dict[str, str]]:
    """
    Validate and parse environment variables from string
    
    Expected format:
    KEY1=value1
    KEY2=value2
    """
    try:
        env_dict = {}
        lines = env_string.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' not in line:
                return None
            
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Validate key format (alphanumeric and underscore only)
            if not re.match(r'^[A-Z_][A-Z0-9_]*$', key):
                return None
            
            env_dict[key] = value
        
        return env_dict if env_dict else None
    
    except Exception as e:
        logger.error(f"Error validating environment variables: {str(e)}")
        return None


def validate_command(command: str) -> bool:
    """
    Validate command format
    
    Examples:
    - npm install && npm run build
    - python app.py
    - ./build.sh
    """
    try:
        if not command or len(command) > 500:
            return False
        
        # Basic validation - command should contain alphanumeric, spaces, and common operators
        if not re.match(r'^[a-zA-Z0-9\s\.\-_/&|;()]+$', command):
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Error validating command: {str(e)}")
        return False


def is_valid_github_token(token: str) -> bool:
    """
    Validate GitHub token format
    
    Valid GitHub tokens start with:
    - ghp_ (Personal Access Token)
    - gho_ (OAuth token)
    - ghu_ (User-to-server token)
    - ghs_ (Server-to-server token)
    """
    return token.startswith(('ghp_', 'gho_', 'ghu_', 'ghs_'))


def truncate_token(token: str, visible_chars: int = 10) -> str:
    """
    Truncate token for display purposes
    Shows first visible_chars and hides the rest with dots
    """
    if len(token) <= visible_chars:
        return token
    return token[:visible_chars] + '...' + token[-4:]


def format_duration(minutes: int) -> str:
    """
    Format duration in minutes to human readable format
    """
    if minutes < 60:
        return f"{minutes}m"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes == 0:
        return f"{hours}h"
    
    return f"{hours}h {remaining_minutes}m"


def calculate_cost(machine_type: str, duration_minutes: int) -> float:
    """
    Calculate Codespace cost based on machine type and duration
    
    Rates (per minute):
    - small: $0.07
    - medium: $0.18
    - large: $0.36
    - xlarge: $0.72
    """
    rates = {
        'small': 0.07,
        'medium': 0.18,
        'large': 0.36,
        'xlarge': 0.72
    }
    
    rate = rates.get(machine_type, 0.18)  # Default to medium
    return (duration_minutes / 60) * rate  # Convert minutes to hours and calculate cost


def get_machine_specs(machine_type: str) -> Dict[str, str]:
    """
    Get machine specifications for a given machine type
    """
    specs = {
        'small': {'cpu': '2-Core', 'ram': '8GB', 'storage': '32GB'},
        'medium': {'cpu': '4-Core', 'ram': '16GB', 'storage': '32GB'},
        'large': {'cpu': '8-Core', 'ram': '32GB', 'storage': '64GB'},
        'xlarge': {'cpu': '16-Core', 'ram': '64GB', 'storage': '128GB'},
    }
    
    return specs.get(machine_type, specs['medium'])


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human readable format
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    
    return f"{bytes_value:.2f} PB"


def sanitize_input(user_input: str, max_length: int = 1000) -> Optional[str]:
    """
    Sanitize user input to prevent injection attacks
    """
    try:
        if not user_input or len(user_input) > max_length:
            return None
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', user_input)
        
        return sanitized.strip()
    
    except Exception as e:
        logger.error(f"Error sanitizing input: {str(e)}")
        return None


def create_progress_bar(current: int, total: int, length: int = 10) -> str:
    """
    Create a simple progress bar
    """
    if total == 0:
        percentage = 0
    else:
        percentage = int((current / total) * 100)
    
    filled = int((length * current) // total)
    bar = '█' * filled + '░' * (length - filled)
    
    return f"{bar} {percentage}%"
