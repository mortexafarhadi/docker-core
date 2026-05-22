import random

from django.db import connection


def random_choice_queryset(queryset):
    db_engine = connection.vendor  # 'sqlite', 'postgresql', 'mysql'

    if db_engine == "postgresql":
        # Fastest — PostgreSQL only
        model = queryset.model
        table = model._meta.db_table
        result = model.objects.raw(
            f"SELECT * FROM {table} TABLESAMPLE BERNOULLI(1) LIMIT 1"
        )
        items = list(result)
        return items[0] if items else None

    else:
        # SQLite / MySQL fallback
        count = queryset.count()
        if not count:
            return None
        return queryset[random.randint(0, count - 1)]
