from django.contrib import admin
from django.utils import timezone
from api.models import Entry


class EntriesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "subject", "message", "create_date_with_seconds")
    ordering = ("-create_date",)
    search_fields = ("user__name",)

    def create_date_with_seconds(self, obj):
        local_time = timezone.localtime(obj.create_date)
        return local_time.strftime("%d-%m-%Y %H:%M:%S")

    create_date_with_seconds.short_description = "Oluşturulma Tarihi"  # Sütun başlığını ayarladık


admin.site.register(Entry, EntriesAdmin)
