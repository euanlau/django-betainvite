from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url

from betainvite.conf import settings
from betainvite.models import InvitationKey

is_key_valid = InvitationKey.objects.is_key_valid

def is_invited(backend, user=None, *args, **kwargs):
    if user:
        return {'user': user}

    if settings.BETA_INVITATION_REQUIRED:
        auth = kwargs.get('auth', None)

        invitation_key = auth.request.session.get('invitation_key', False)
        if invitation_key and is_key_valid(invitation_key):
            return None
        redirect_url = resolve_url(settings.BETA_REDIRECT_URL)
        return HttpResponseRedirect(redirect_url)
    return None
