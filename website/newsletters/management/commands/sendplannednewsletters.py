from django.core.management.base import BaseCommand
from django.utils import timezone

from newsletters import emails
from newsletters.models import Newsletter


class Command(BaseCommand):

    def handle(self, *args, **options):
        newsletters = Newsletter.objects.filter(
            send_date__lte=timezone.now(),
            sent=False
        )
        for n in newsletters:
            emails.send_newsletter(n)
