from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import Q
from django.contrib.auth.models import User
from api.models import Entry


@registry.register_document
class EntryDocumet(Document):
    user = fields.ObjectField(
        properties={
            "username": fields.KeywordField(),
        }
    )

    class Index:
        name = "entries"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Entry
        fields = ["subject", "message", "create_date"]
        related_models = [User]

    def get_instances_from_related(self, related_instance):
        return Entry.objects.filter(user=related_instance)
