from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from betainvite.views import invite, waitlist_signup

urlpatterns = patterns('',
    url(r'^invite/complete/$',
        TemplateView.as_view(template_name='betainvite/invitation_complete.html'),
        name='invitation_complete'),
    url(r'^invite/$',
        invite,
        name='invitation_invite'),
    url(r"^waitlist/signup/$",
        waitlist_signup,
        name="waitlist_signup"),
    url(r"^waitlist/success/$",
        TemplateView.as_view(template_name="betainvite/waitlist_success.html"),
        name="waitlist_success"),
)
