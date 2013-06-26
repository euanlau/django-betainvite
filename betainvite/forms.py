from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Field
from .models import WaitingListEntry

class WaitingListEntryForm(forms.ModelForm):
    class Meta:
        model = WaitingListEntry
        exclude = ['invited',]

    def clean_email(self):
        value = self.cleaned_data["email"]
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

        self.helper.layout = Layout(
            Fieldset(
                '',
                 Field('email', css_class='input-large')
            ),
            Submit('submit', 'Subscribe', css_class='btn btn-success btn-large')
        )


class InvitationKeyForm(forms.Form):
    email = forms.EmailField()
