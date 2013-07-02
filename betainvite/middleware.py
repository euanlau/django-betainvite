from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.core.urlresolvers import reverse
from betainvite.conf import settings
from betainvite.models import InvitationKey

is_key_valid = InvitationKey.objects.is_key_valid

class BetaMiddleware(object):
    """
    Add this to your ``MIDDLEWARE_CLASSES`` make all views except for
    those in the account application require that a user be logged in.
    This can be a quick and easy way to restrict views on your site,
    particularly if you remove the ability to create accounts.
    """

    def __init__(self):
        self.private_access = settings.BETA_PRIVATE_MODE
        self.always_allow_views = settings.BETA_ALWAYS_ALLOW_VIEWS
        self.always_allow_modules = settings.BETA_ALWAYS_ALLOW_MODULES
        self.always_allow_urls = [reverse(x) for x in settings.BETA_ALWAYS_ALLOW_URLS]
        self.redirect_url = resolve_url(settings.BETA_REDIRECT_URL)

    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.user.is_authenticated():
            # User is logged in, no need to check anything else.
            return

        full_view_name = '%s.%s' % (view_func.__module__, view_func.__name__)

        if full_view_name in settings.BETA_REGISTRATION_VIEWS:
            if settings.BETA_INVITATION_REQUIRED:
                # invitation is required to register
                invitation_key = request.REQUEST.get('invitation_key', False)
                if invitation_key and is_key_valid(invitation_key):
                    return

                return HttpResponseRedirect(self.redirect_url)

        if not self.private_access:
            # private access is not enabled, just let user to access the view
            return

        whitelisted_modules = ['django.contrib.auth.views', 'django.views.static', 'betainvite.views']
        if self.always_allow_modules:
            whitelisted_modules += self.always_allow_modules

        if full_view_name in self.always_allow_views:
            return
        if '%s' % view_func.__module__ in whitelisted_modules:
            return
        if request.path in self.always_allow_urls:
            return
        else:
            return HttpResponseRedirect(self.redirect_url)
