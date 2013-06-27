from django import template

from betainvite.forms import WaitingListEntryForm
from betainvite.models import InvitationKey

register = template.Library()

@register.simple_tag(takes_context = True)
def remaining_invites(context):
    """
    Get the remaning invites available for the current user

    Syntax::

        {% remaining_invites %}

    """
    request = context['request']
    user = request.user
    remaining_invites = InvitationKey.objects.remaining_invitations_for_user(user)
    return remaining_invites

@register.assignment_tag
def waitinglist_entry_form():
    """
    Get a (new) form object to post a new comment.

    Syntax::

        {% waitinglist_entry_form as [varname] %}

    """
    return WaitingListEntryForm()
