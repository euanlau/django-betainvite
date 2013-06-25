from django.conf import settings


"""
Is invitation required to register
"""
BETA_INVITATION_REQUIRED = getattr(settings, 'BETA_INVITATION_REQUIRED', False)

"""
List of registration views that require invitations
"""
BETA_REGISTRATION_VIEWS = getattr(settings, 'BETA_REGISTRATION_VIEWS',
                                  ['registration.views.register',])

"""
Limit access to registered user or invited new user only
"""
BETA_PRIVATE_MODE = getattr(settings, 'BETA_PRIVATE_MODE', True)


"""
A list of full view names that should always pass through when private
beta is enabled
"""
BETA_ALWAYS_ALLOW_VIEWS = getattr(settings, 'BETA_ALWAYS_ALLOW_VIEWS', [])


"""
List of views that can be accessed when private mode is enabled
"""
BETA_ALWAYS_ALLOW_MODULES = getattr(settings, 'BETA_ALWAYS_ALLOW_MODULES', [])

"""
Redirect URL when user does not have private beta access
"""
BETA_REDIRECT_URL = getattr(settings, 'BETA_REDIRECT_URL', 'waitlist_signup')

"""
Number of invitations given to each user
"""
INVITATIONS_PER_USER = getattr(settings, 'INVITATIONS_PER_USER', 5)

"""
Number of days before the invitations expire
"""
INVITATIONS_VALID_DAYS = getattr(settings, 'INVITATIONS_VALID_DAYS', 30)
