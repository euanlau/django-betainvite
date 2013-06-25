import os
import random
import datetime
import urllib
import uuid
from django.db import models
from django.conf import settings
from django.utils.http import int_to_base36
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from betainvite.conf import settings as appsettings

class WaitingListEntry(models.Model):
    email = models.EmailField(_("email address"), unique=True)
    created = models.DateTimeField(_("created"), default=datetime.datetime.now,
                                   editable=False)
    invited = models.BooleanField(_('Invited'), default=False)

    class Meta:
        verbose_name = _("waiting list entry")
        verbose_name_plural = _("waiting list entries")

    def __unicode__(self):
        return self.email

class InvitationKeyManager(models.Manager):
    def get_key(self, invitation_key):
        """
        Return InvitationKey, or None if it doesn't (or shouldn't) exist.
        """
        # Don't bother hitting database if invitation_key doesn't match pattern.
        try:
            key = self.get(key=invitation_key)
        except self.model.DoesNotExist:
            return None

        return key

    def is_key_valid(self, invitation_key):
        """
        Check if an ``InvitationKey`` is valid or not, returning a boolean,
        ``True`` if the key is valid.
        """
        invitation_key = self.get_key(invitation_key)
        return invitation_key and invitation_key.is_usable()

    def create_invitation(self, user=None):
        """
        Create an ``InvitationKey`` and returns it.

        The key for the ``InvitationKey`` will be a uuid
        from a combination of the ``User``'s username and a random salt.
        """
        key = uuid.uuid4().hex
        return self.create(from_user=user, key=key)

    def remaining_invitations_for_user(self, user):
        """
        Return the number of remaining invitations for a given ``User``.
        """
        invitation_user, created = InvitationUser.objects.get_or_create(
            inviter=user,
            defaults={'invitations_remaining': appsettings.INVITATIONS_PER_USER})
        return invitation_user.invitations_remaining

    def delete_expired_keys(self):
        for key in self.all():
            if key.key_expired():
                key.delete()


class InvitationKey(models.Model):
    key = models.CharField(_('invitation key'), max_length=40)
    date_invited = models.DateTimeField(_('date invited'),
                                        default=datetime.datetime.now)
    from_user = models.ForeignKey(User, null=True, blank=True,
                                  related_name='invitations_sent')
    registrant = models.ForeignKey(User, null=True, blank=True,
                                  related_name='invitations_used')

    objects = InvitationKeyManager()

    def __unicode__(self):
        return u"Invitation %s on %s" % (self.key, self.date_invited)

    def get_absolute_url(self, view='registration.views.register'):
        from django.core.urlresolvers import reverse

        params = { 'invitation_key' : self.key }
        url = reverse(view) + '?' + urllib.urlencode(params)
        return url

    def is_usable(self):
        """
        Return whether this key is still valid for registering a new user.
        """
        return self.registrant is None and not self.key_expired()

    def key_expired(self):
        """
        Determine whether this ``InvitationKey`` has expired, returning
        a boolean -- ``True`` if the key has expired.

        The date the key has been created is incremented by the number of days
        specified in the setting ``INVITATIONS_VALID_DAYS`` (which should be
        the number of days after invite during which a user is allowed to
        create their account); if the result is less than or equal to the
        current date, the key has expired and this method returns ``True``.

        """
        expiration_date = datetime.timedelta(days=appsettings.INVITATIONS_VALID_DAYS)
        return self.date_invited + expiration_date <= datetime.datetime.now()
    key_expired.boolean = True

    def mark_used(self, registrant):
        """
        Note that this key has been used to register a new user.
        """
        self.registrant = registrant
        self.save()

    def send_to(self, email):
        """
        Send an invitation email to ``email``.
        """
        current_site = Site.objects.get_current()

        subject = render_to_string('invitation/invitation_email_subject.txt',
                                   { 'site': current_site,
                                     'invitation_key': self })
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('invitation/invitation_email.txt',
                                   { 'invitation_key': self,
                                     'expiration_days': appsettings.INVITATIONS_VALID_DAYS,
                                     'site': current_site })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


class InvitationUser(models.Model):
    inviter = models.ForeignKey(User, unique=True)
    invitations_remaining = models.IntegerField()

    def __unicode__(self):
        return u"InvitationUser for %s" % self.inviter.username


def user_post_save(sender, instance, created, **kwargs):
    """Create InvitationUser for user when User is created."""
    if created:
        invitation_user = InvitationUser()
        invitation_user.inviter = instance
        invitation_user.invitations_remaining = appsettings.INVITATIONS_PER_USER
        invitation_user.save()

models.signals.post_save.connect(user_post_save, sender=User)

def invitation_key_post_save(sender, instance, created, **kwargs):
    """Decrement invitations_remaining when InvitationKey is created."""
    if created and instance.from_user is not None:
        invitation_user = InvitationUser.objects.get(inviter=instance.from_user)
        remaining = invitation_user.invitations_remaining
        invitation_user.invitations_remaining = remaining-1
        invitation_user.save()

models.signals.post_save.connect(invitation_key_post_save, sender=InvitationKey)
