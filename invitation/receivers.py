from .models import InvitationKey
from registration import signals as registration_signals

@receiver(registraiton_signals.user_registered)
def post_user_registration(sender, user, request, **kwargs):
    """
    Mark the invitation key as used post user registration.
    """
    invitation_key = request.REQUEST.get('invitation_key')
    key = InvitationKey.objects.get_key(invitation_key)
    if key:
        key.mark_used(user)

    return
