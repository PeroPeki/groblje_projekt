from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from pristup.models import NeuspjeliPokusaj


class Command(BaseCommand):
    help = "Briše neuspjele pokušaje starije od 24 sata (pokreće se jednom dnevno, P-27)."

    def handle(self, *args, **options):
        granica = timezone.now() - timedelta(hours=24)
        obrisano, _ = NeuspjeliPokusaj.objects.filter(vrijeme__lt=granica).delete()
        self.stdout.write(f"Obrisano neuspjelih pokušaja: {obrisano}")
