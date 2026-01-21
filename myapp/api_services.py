# myapp/api_services.py
"""
Third-party API integration module for TaskMaster.
Handles integrations with external services like weather, social media, etc.
"""

import requests
from django.conf import settings
from django.contrib.auth.models import User


class WeatherService:
    """Integration with weather API (OpenWeatherMap)."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    @classmethod
    def get_weather(cls, city: str, api_key: str = None) -> dict:
        """
        Fetch weather information for a given city.
        
        Args:
            city (str): City name
            api_key (str): OpenWeatherMap API key
            
        Returns:
            dict: Weather data or error message
        """
        if not api_key:
            api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        
        if not api_key:
            return {'error': 'Weather API key not configured'}
        
        try:
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'
            }
            response = requests.get(cls.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return {
                'city': data.get('name'),
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
            }
        except requests.RequestException as e:
            return {'error': f'Failed to fetch weather: {str(e)}'}


class GitHubService:
    """Integration with GitHub API."""
    
    BASE_URL = "https://api.github.com"
    
    @classmethod
    def get_user_repos(cls, username: str, token: str = None) -> dict:
        """
        Fetch GitHub repositories for a user.
        
        Args:
            username (str): GitHub username
            token (str): GitHub personal access token (optional)
            
        Returns:
            dict: List of repositories or error message
        """
        try:
            headers = {}
            if token:
                headers['Authorization'] = f'token {token}'
            
            url = f"{cls.BASE_URL}/users/{username}/repos"
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            repos = response.json()
            return {
                'username': username,
                'repos': [
                    {
                        'name': repo['name'],
                        'url': repo['html_url'],
                        'description': repo['description'],
                        'stars': repo['stargazers_count'],
                        'language': repo['language'],
                    }
                    for repo in repos[:10]  # Limit to 10 repos
                ]
            }
        except requests.RequestException as e:
            return {'error': f'Failed to fetch GitHub repos: {str(e)}'}


class TwitterService:
    """Integration with Twitter API (X)."""
    
    BASE_URL = "https://api.twitter.com/2"
    
    @classmethod
    def search_tweets(cls, query: str, bearer_token: str = None) -> dict:
        """
        Search tweets (requires Twitter API v2 access).
        
        Args:
            query (str): Search query
            bearer_token (str): Twitter Bearer Token
            
        Returns:
            dict: Search results or error message
        """
        if not bearer_token:
            bearer_token = getattr(settings, 'TWITTER_BEARER_TOKEN', None)
        
        if not bearer_token:
            return {'error': 'Twitter API token not configured'}
        
        try:
            headers = {
                'Authorization': f'Bearer {bearer_token}',
                'User-Agent': 'TaskMaster-Bot/1.0'
            }
            
            params = {
                'query': query,
                'max_results': 10,
                'tweet.fields': 'created_at,author_id,public_metrics'
            }
            
            url = f"{cls.BASE_URL}/tweets/search/recent"
            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return {
                'query': query,
                'results': data.get('data', []),
                'result_count': len(data.get('data', []))
            }
        except requests.RequestException as e:
            return {'error': f'Failed to search tweets: {str(e)}'}


class NotificationService:
    """Send notifications via email or other channels."""
    
    @staticmethod
    def send_task_notification(user: User, task, notification_type: str = 'created') -> bool:
        """
        Send task notification to user.
        
        Args:
            user (User): User to notify
            task (Task): Task related to notification
            notification_type (str): Type of notification ('created', 'assigned', 'updated')
            
        Returns:
            bool: Success status
        """
        # TODO: Implement email notification using Django's send_mail
        # This would integrate with email service (SendGrid, AWS SES, etc.)
        pass
    
    @staticmethod
    def send_comment_notification(user: User, comment, task) -> bool:
        """
        Send comment notification to task owner.
        
        Args:
            user (User): User who made the comment
            comment: Comment object
            task: Task being commented on
            
        Returns:
            bool: Success status
        """
        # TODO: Implement comment notification
        pass


class SlackService:
    """Integration with Slack for notifications."""
    
    @staticmethod
    def send_message(webhook_url: str, message: str, channel: str = None) -> bool:
        """
        Send message to Slack channel.
        
        Args:
            webhook_url (str): Slack webhook URL
            message (str): Message to send
            channel (str): Channel to send to (optional)
            
        Returns:
            bool: Success status
        """
        try:
            payload = {
                'text': message,
            }
            if channel:
                payload['channel'] = channel
            
            response = requests.post(webhook_url, json=payload, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    @staticmethod
    def notify_task_update(webhook_url: str, task, action: str = 'updated') -> bool:
        """
        Send task update notification to Slack.
        
        Args:
            webhook_url (str): Slack webhook URL
            task: Task object
            action (str): Action performed ('created', 'updated', 'completed')
            
        Returns:
            bool: Success status
        """
        message = f"Task {action}: {task.title}\nStatus: {task.get_status_display()}\nPriority: {task.get_priority_display()}"
        return SlackService.send_message(webhook_url, message)
