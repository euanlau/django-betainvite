from django.core.management.base import BaseCommand
from optparse import make_option

class Command(BaseCommand):
    help = "Send invitations to people on the waiting list"
    def handle(self, *args, **options):
        try:
            count = args[0]
        except IndexError:
            print u'usage :', __name__.split('.')[-1], 'number_of_invitations'
            return

        from betainvite.models import WaitingListEntry
        entries = WaitingListEntry.objects.filter(invited=False)[:count]
        print "Sending invitations to %d people" % (entries.count())
        for entry in entries:
            print "Sending invitation to %s" % (entry.email)
            entry.send_invitation()
