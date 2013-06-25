from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from optparse import make_option
import urlparse

class Command(BaseCommand):
    help = "Generate new invitation links"
    option_list = BaseCommand.option_list + (
        make_option('-c', '--count',
                    type="int",
                    default = 10,
                    dest="count",
                    help='number of new invitations'),
        make_option('--view',
                    type="string",
                    default = 'registration.views.register',
                    dest="view",
                    help='sign up view'),
    )

    def handle(self, *args, **options):
        from betainvite.models import InvitationKey
        current_site = Site.objects.get_current()
        count = options.get('count')
        view = options.get('view')
        domain = "http://%s" % Site.objects.get_current().domain

        for i in range(0, count):
            invitation = InvitationKey.objects.create_invitation()
            print urlparse.urljoin(domain, invitation.get_absolute_url(view))
