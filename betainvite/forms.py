from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Field
from .models import WaitingListEntry

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

class WaitingListEntryForm(forms.ModelForm):
    class Meta:
        model = WaitingListEntry
        exclude = ['invited',]

    def clean_email(self):
        value = self.cleaned_data["email"]

        user_exists = User.objects.filter(email=value).exists()
        if user_exists:
            raise forms.ValidationError(
                _("User already exists")
            )

        try:
            entry = WaitingListEntry.objects.get(email=value)
        except WaitingListEntry.DoesNotExist:
            return value
        else:
            raise forms.ValidationError(
                "The email address %(email)s already registered on %(date)s." % {
                    "email": value,
                    "date": entry.created.strftime("%m/%d/%y"),
                }
            )

    def __init__(self, *args, **kwargs):
        super(WaitingListEntryForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "your@email.com"
        self.fields["email"].label = ""

        self.helper = FormHelper()
        self.helper.form_id = 'waitlist-signup-form'
        self.helper.form_class = 'validate form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action =  reverse('waitlist_signup')
        self.helper.help_text_inline = False
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                 Field('email', css_class='input-large')
            ),
            Submit('submit', 'Subscribe', css_class='btn btn-success btn-large')
        )


class InvitationKeyForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(InvitationKeyForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = _("Email Address")
        self.fields["email"].label = ""

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('email', css_class='input-large'),
        )
