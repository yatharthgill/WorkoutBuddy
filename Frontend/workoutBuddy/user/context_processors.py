# mainPage/context_processors.py
from django.conf import settings

def auth_token(request):
    """Provide auth token and FastAPI base URL to templates.

    Returns:
        dict: { 'token': <session token or ''>, 'FASTAPI_BASE_URL': <value from Django settings> }
    """
    return {
        'token': request.session.get('token'),
        'FASTAPI_BASE_URL': getattr(settings, 'FASTAPI_BASE_URL', '')
    }
