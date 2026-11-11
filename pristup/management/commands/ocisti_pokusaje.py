from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from pristup.models import NeuspjeliPokusaj
from pristup.ogranicenja import najdulji_prozor


class Command(BaseCommand):
    help = "Briše neuspjele pokušaje starije od 24 sata (pokreće se jednom dnevno, P-27)."

    def handle(self, *args, **options):
        # Nikad ne brišemo zapise koji se još broje u nekom ograničenju.
        starost = max(timedelta(hours=24), najdulji_prozor())
        obrisano, _ = NeuspjeliPokusaj.objects.filter(vrijeme__lt=timezone.now() - starost).delete()
        self.stdout.write(f"Obrisano neuspjelih pokušaja: {obrisano}")
