from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Reset the number of remaining number of invitations"

    def handle_noargs(self, **options):
        from betainvite.models import InvitationUser
        from betainvite.conf import settings
        users = InvitationUser.objects.all()
        for user in users:
            user.invitations_remaining = settings.INVITATIONS_PER_USER
            user.save()
