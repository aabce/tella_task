from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry
from .models import Product

custom_analyzer = analyzer(
    'custom_analyzer',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@registry.register_document
class ProductDocument(Document):
    title = fields.TextField(
        analyzer=custom_analyzer,
        fields={ 'raw' :fields.KeywordField() }
    )
    description = fields.TextField(
        analyzer=custom_analyzer,
        fields={'raw': fields.KeywordField()}
    )
    features = fields.TextField(
        analyzer=custom_analyzer,
        fields={'raw': fields.KeywordField()}
    )

    class Index:
        name = 'products'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product

        fields = [
            'id',
        ]
