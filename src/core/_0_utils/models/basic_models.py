from .mixin_models import (
    UUIDMixin,
    TimeStampedMixin,
    DescriptionMixin,
    DescriptionCKEditorMixin,
    SoftDeleteMixin,
    ActiveMixin,
    SortOrderMixin,
    DescriptionMultiLanguageMixin,
    DescriptionCKEditorMultiLanguageMixin,
    HistoricalMixin,
)


class BasicModel(UUIDMixin, TimeStampedMixin, DescriptionMixin, SoftDeleteMixin):
    """Base model with common functionality"""

    def save(self, *args, **kwargs):
        """Custom save logic"""
        if self.is_deleted:
            return

        super().save(*args, **kwargs)

    def __str__(self):
        """String representation using slug or ID"""
        if hasattr(self, "slug") and self.slug:
            return str(self.slug)
        return str(self.id)

    class Meta:
        abstract = True
        ordering = ["-datetime_create"]


class BasicMultiLangModel(
    UUIDMixin,
    TimeStampedMixin,
    DescriptionMultiLanguageMixin,
    SoftDeleteMixin,
):
    """Base model with common functionality"""

    def save(self, *args, **kwargs):
        """Custom save logic"""
        if self.is_deleted:
            return

        super().save(*args, **kwargs)

    def __str__(self):
        """String representation using slug or ID"""
        if hasattr(self, "slug") and self.slug:
            return str(self.slug)
        return str(self.id)

    class Meta:
        abstract = True
        ordering = ["-datetime_create"]


class BasicModelHistorical(BasicModel, HistoricalMixin):
    """Basic model with history tracking"""

    class Meta:
        abstract = True


class BasicMultiLangModelHistorical(BasicMultiLangModel, HistoricalMixin):
    """Basic model with history tracking"""

    class Meta:
        abstract = True


class BaseModelActive(ActiveMixin, BasicModel):
    """Active version of base model"""

    class Meta:
        abstract = True
        ordering = ["is_active", "-datetime_create"]


class BaseMultiLangModelActive(ActiveMixin, BasicMultiLangModel):
    """Active version of base model"""

    class Meta:
        abstract = True
        ordering = ["is_active", "-datetime_create"]


class BaseModelActiveHistorical(BaseModelActive, HistoricalMixin):
    """Active base model with history tracking"""

    class Meta:
        abstract = True


class BaseMultiLangModelActiveHistorical(BaseMultiLangModelActive, HistoricalMixin):
    """Active base model with history tracking"""

    class Meta:
        abstract = True


class BaseModelActiveSortOrder(SortOrderMixin, BaseModelActive):
    """Active base model with display order"""

    class Meta:
        abstract = True
        ordering = ["-sort_order", "is_active", "-datetime_create"]


class BaseMultiLangModelActiveSortOrder(SortOrderMixin, BaseMultiLangModelActive):
    """Active base model with display order"""

    class Meta:
        abstract = True
        ordering = ["-sort_order", "is_active", "-datetime_create"]


class BaseModelActiveSortOrderHistorical(BaseModelActiveSortOrder, HistoricalMixin):
    """Active ordered base model with history tracking"""

    class Meta:
        abstract = True


class BaseMultiLangModelActiveSortOrderHistorical(
    BaseMultiLangModelActiveSortOrder, HistoricalMixin
):
    """Active ordered base model with history tracking"""

    class Meta:
        abstract = True


class BasicCKEditorModel(
    UUIDMixin, TimeStampedMixin, DescriptionCKEditorMixin, SoftDeleteMixin
):
    """Base model with common functionality"""

    def save(self, *args, **kwargs):
        """Custom save logic"""
        if self.is_deleted:
            return

        super().save(*args, **kwargs)

    def __str__(self):
        """String representation using slug or ID"""
        if hasattr(self, "slug") and self.slug:
            return str(self.slug)
        return str(self.id)

    class Meta:
        abstract = True
        ordering = ["-datetime_create"]


class BasicCKEditorMultiLangModel(
    UUIDMixin,
    TimeStampedMixin,
    DescriptionCKEditorMultiLanguageMixin,
    SoftDeleteMixin,
):
    """Base model with common functionality"""

    def save(self, *args, **kwargs):
        """Custom save logic"""
        if self.is_deleted:
            return

        super().save(*args, **kwargs)

    def __str__(self):
        """String representation using slug or ID"""
        if hasattr(self, "slug") and self.slug:
            return str(self.slug)
        return str(self.id)

    class Meta:
        abstract = True
        ordering = ["-datetime_create"]


class BasicCKEditorModelHistorical(BasicCKEditorModel, HistoricalMixin):
    """Basic model with history tracking"""

    class Meta:
        abstract = True


class BasicCKEditorMultiLangModelHistorical(
    BasicCKEditorMultiLangModel, HistoricalMixin
):
    """Basic model with history tracking"""

    class Meta:
        abstract = True


class BaseCKEditorModelActive(ActiveMixin, BasicCKEditorModel):
    """Active version of base model"""

    class Meta:
        abstract = True
        ordering = ["is_active", "-datetime_create"]


class BaseCKEditorMultiLangModelActive(ActiveMixin, BasicCKEditorMultiLangModel):
    """Active version of base model"""

    class Meta:
        abstract = True
        ordering = ["is_active", "-datetime_create"]


class BaseCKEditorModelActiveHistorical(BaseCKEditorModelActive, HistoricalMixin):
    """Active base model with history tracking"""

    class Meta:
        abstract = True


class BaseCKEditorMultiLangModelActiveHistorical(
    BaseCKEditorMultiLangModelActive, HistoricalMixin
):
    """Active base model with history tracking"""

    class Meta:
        abstract = True


class BaseCKEditorModelActiveSortOrder(SortOrderMixin, BaseCKEditorModelActive):
    """Active base model with display order"""

    class Meta:
        abstract = True
        ordering = ["-sort_order", "is_active", "-datetime_create"]


class BaseCKEditorMultiLangModelActiveSortOrder(
    SortOrderMixin, BaseCKEditorMultiLangModelActive
):
    """Active base model with display order"""

    class Meta:
        abstract = True
        ordering = ["-sort_order", "is_active", "-datetime_create"]


class BaseCKEditorModelActiveSortOrderHistorical(
    BaseCKEditorModelActiveSortOrder, HistoricalMixin
):
    """Active ordered base model with history tracking"""

    class Meta:
        abstract = True


class BaseCKEditorMultiLangModelActiveSortOrderHistorical(
    BaseCKEditorMultiLangModelActiveSortOrder, HistoricalMixin
):
    """Active ordered base model with history tracking"""

    class Meta:
        abstract = True
