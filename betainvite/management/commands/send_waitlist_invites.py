from django.core.management.base import BaseCommand
from optparse import make_option

class Command(BaseCommand):
    help = "Send invitations to people on the waiting list"
    option_list = BaseCommand.option_list + (
        make_option('-c', '--count',
                    type="int",
                    default = 10,
                    dest="count",
                    help='number of new invitations'),
    )

    def handle(self, *args, **options):
        from betainvite.models import WaitingListEntry
        count = options.get('count')
        entries = WaitingListEntry.objects.filter(invited=False)[:count]
        for entry in entries:
            entry.send_invitation()
