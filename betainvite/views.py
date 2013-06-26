
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from betainvite.models import InvitationKey
from betainvite.forms import InvitationKeyForm, WaitingListEntryForm
from betainvite.conf import settings

from .signals import signed_up

remaining_invitations_for_user = InvitationKey.objects.remaining_invitations_for_user

def waitlist_signup(request, form_class=WaitingListEntryForm,
                    template_name="betainvite/waitlist_signup.html",
                    post_save_redirect=None):
    form = form_class(request.POST or None)
    if form.is_valid():
        entry = form.save()
        signed_up.send(sender=waitlist_signup, entry=entry)
        if post_save_redirect is None:
            post_save_redirect = reverse("waitlist_success")
        if not post_save_redirect.startswith("/"):
            post_save_redirect = reverse(post_save_redirect)
        return redirect(post_save_redirect)
    ctx = {
        "form": form,
    }
    return render_to_response(template_name, ctx, RequestContext(request))

@login_required
def invite(request, success_url=None,
           form_class=InvitationKeyForm,
           template_name='betainvite/invitation_form.html',
           extra_context=None):
    extra_context = extra_context is not None and extra_context.copy() or {}
    remaining_invitations = remaining_invitations_for_user(request.user)
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if remaining_invitations > 0 and form.is_valid():
            invitation = InvitationKey.objects.create_invitation(request.user)
            invitation.send_to(form.cleaned_data["email"])
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return HttpResponseRedirect(success_url or reverse('invitation_complete'))
    else:
        form = form_class()
    extra_context.update({
            'form': form,
            'remaining_invitations': remaining_invitations,
        })
    return render_to_response(template_name, extra_context, RequestContext(request))
