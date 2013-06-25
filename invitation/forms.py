from django import forms
from django.utils.translation import ugettext_lazy as _

class WaitingListEntryForm(forms.ModelForm):
    class Meta:
        model = WaitingListEntry

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

class InvitationKeyForm(forms.Form):
    email = forms.EmailField()
