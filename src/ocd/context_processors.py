from django.conf import settings


def analytics(request):

    """OPENCOMMUNITY_ANALYTICS setup in the request context."""

    analytics = {
        'piwik': settings.OPENCOMMUNITY_ANALYTICS.get('piwik'),
        'ga': settings.OPENCOMMUNITY_ANALYTICS.get('ga')
    }

    return {'analytics': analytics}
