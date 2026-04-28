import uuid

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from simple_history.models import HistoricalRecords
from translated_fields import TranslatedField

from ___utils.functions.date_and_time_function import now
from ___utils.functions.log_function import insert_query_text_log


class UUIDMixin(models.Model):
    """Mixin for UUID primary key"""

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Mixin for soft delete functionality.
    Sets is_deleted flag instead of actual deletion.
    """

    datetime_delete = models.DateTimeField(null=True, blank=True, editable=False)
    is_deleted = models.BooleanField(default=False, editable=False)

    def get_is_deleted_display(self):
        return "Deleted" if self.is_deleted else "Not Deleted"

    def delete(self, *args, **kwargs):
        """Soft delete implementation"""
        self.is_deleted = True
        self.datetime_delete = now()
        super().save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        """Actual database deletion"""
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    """Mixin for adding slug field with auto-generation"""

    slug = models.SlugField(
        max_length=250, unique=True, allow_unicode=True, editable=False
    )

    def set_slug(self):
        """Generate unique slug for the model"""
        from ___utils.functions.generator import uniq_slugify as tc

        self.slug = tc.uniq_number_slug(self)

    class Meta:
        abstract = True


class DescriptionMixin(models.Model):
    """Mixin for adding description field"""

    description = models.TextField(null=True, blank=True)

    def get_description_display(self):
        """Get description or default placeholder"""
        return self.description or "-----"

    class Meta:
        abstract = True


class DescriptionMultiLanguageMixin(models.Model):
    """Mixin for adding description field"""

    description = TranslatedField(models.TextField(null=True, blank=True))

    def get_description_display(self):
        """Get description or default placeholder"""
        return self.description or "-----"

    class Meta:
        abstract = True


class DescriptionCKEditorMixin(models.Model):
    """Mixin for adding description field"""

    description = CKEditor5Field("Text", null=True, blank=True)

    def get_description_display(self):
        """Get description or default placeholder"""
        return self.description or "-----"

    class Meta:
        abstract = True


class DescriptionCKEditorMultiLanguageMixin(models.Model):
    """Mixin for adding description field"""

    description = TranslatedField(CKEditor5Field("Text", null=True, blank=True))

    def get_description_display(self):
        """Get description or default placeholder"""
        return self.description or "-----"

    class Meta:
        abstract = True


class DatetimeCreateMixin(models.Model):
    """Mixin for tracking creation timestamps"""

    datetime_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-datetime_create"]


class DatetimeUpdateMixin(models.Model):
    """Mixin for tracking update timestamps"""

    datetime_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeStampedMixin(DatetimeCreateMixin, DatetimeUpdateMixin):
    """Mixin for tracking creation and update timestamps"""

    class Meta:
        abstract = True


class ActiveMixin(models.Model):
    """Mixin for On/inactive status"""

    is_active = models.BooleanField(default=True)

    def get_is_active_display(self):
        """Get human-readable active status"""
        return "On" if self.is_active else "Off"

    def delete(self, *args, **kwargs):
        """Deactivate instead of deleting"""
        self.is_active = False
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True


class SortOrderMixin(models.Model):
    """Mixin for controlling display order"""

    sort_order = models.PositiveSmallIntegerField(default=1)

    def delete(self, *args, **kwargs):
        """Set order to 0 when deleted"""
        self.sort_order = 0
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True


class HistoricalMixin(models.Model):
    """Mixin for model history tracking"""

    history = HistoricalRecords(inherit=True)

    def save_without_history(self, *args, **kwargs):
        try:
            self.skip_history_when_saving = True
            return self.save(*args, **kwargs)
        finally:
            # برای اینکه ذخیره‌های بعدی به‌طور ناخواسته بدون تاریخچه نشوند، فلگ را پاک می‌کنیم
            if hasattr(self, "skip_history_when_saving"):
                delattr(self, "skip_history_when_saving")

    @property
    def history_logs(self):
        """Property access to history logs"""
        return self.get_history_logs()

    def get_history_logs(self):
        """Retrieve and format history logs"""
        log_records = self.history.all().order_by("-history_date")
        if not log_records.exists():
            return []

        results = []
        first_record = log_records.first()

        # Get the actual table name instead of model name
        model_name = str(self._meta.model_name).title()

        results.append(
            self._create_history_entry(
                record=1,
                action="Create",
                record_date=first_record.history_date,
                user=first_record.history_user,
                changes=None,
                model_name=model_name,
                obj=(
                    first_record.instance if hasattr(first_record, "instance") else None
                ),
            )
        )

        for i in range(1, len(log_records)):
            new_record = log_records[i - 1]
            old_record = log_records[i]
            delta = new_record.diff_against(old_record)

            action = (
                "Delete"
                if any(c.field == "is_deleted" and c.new for c in delta.changes)
                else "Update"
            )
            changes = [
                f"'{c.field}' changed from '{c.old}' to '{c.new}'"
                for c in delta.changes
            ]

            results.append(
                self._create_history_entry(
                    record=i + 1,
                    action=action,
                    record_date=new_record.history_date,
                    user=new_record.history_user,
                    changes=changes,
                    model_name=model_name,
                    obj=(
                        new_record.instance if hasattr(new_record, "instance") else None
                    ),
                )
            )

        return results

    def _create_history_entry(
        self, record, action, record_date, user, changes, model_name, obj
    ):
        """Helper method to create standardized history entry"""

        if action == "Create":
            query_text = insert_query_text_log(model_name, obj)
        else:
            query_text = (
                f"{action} RECORD with: {', '.join(changes)}"
                if changes
                else f"{action} RECORD"
            )

        return {
            "id": record,
            "query_text": query_text,
            "user": user,
            "status": action,
            "datetime": record_date,
        }

    class Meta:
        abstract = True
