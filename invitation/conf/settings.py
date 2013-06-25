from django.conf import settings

PRIVATEBETA_ENABLE_BETA = getattr(settings, 'PRIVATEBETA_ENABLE_BETA', True)
PRIVATEBETA_NEVER_ALLOW_VIEWS = getattr(settings, 'PRIVATEBETA_NEVER_ALLOW_VIEWS', [])
PRIVATEBETA_ALWAYS_ALLOW_VIEWS = getattr(settings, 'PRIVATEBETA_ALWAYS_ALLOW_VIEWS', [])
PRIVATEBETA_ALWAYS_ALLOW_MODULES = getattr(settings, 'PRIVATEBETA_ALWAYS_ALLOW_MODULES', [])
PRIVATEBETA_REDIRECT_URL = getattr(settings, 'PRIVATEBETA_REDIRECT_URL', '/invite/')

PRIVATEBETA_REGISTRATION_VIEWS = getattr(settings, 'PRIVATEBETA_REGISTRATION_VIEWS',
                                         ['registration.views.register',])

INVITATIONS_PER_USER = getattr(settings, 'INVITATIONS_PER_USER', 5)
INVITATIONS_VALID_DAYS = getattr(settings, 'INVITATIONS_VALID_DAYS', 30)
INVITE_MODE = getattr(settings, 'INVITE_MODE', False)
