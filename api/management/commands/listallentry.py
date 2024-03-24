from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Entry


class Command(BaseCommand):
    help = "Entry verilerini listeler"

    def create_date_with_seconds(self, obj):
        local_time = timezone.localtime(obj.create_date)
        return local_time.strftime("%d-%m-%Y %H:%M:%S")

    def handle(self, *args, **options):
        for entry in Entry.objects.all().order_by("-create_date"):
            self.stdout.write(self.style.SUCCESS(f"{entry.user.username} - {entry.subject} - {entry.message} - {self.create_date_with_seconds(obj=entry)}"))
