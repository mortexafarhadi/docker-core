import os
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadPathFactory:
    """
    کلاس قابل فراخوانی برای تولید مسیر پویا در FileField و ImageField.
    """

    def __init__(
        self,
        base_path,
        use_parent=False,
        parent_field="parent",
        extra_path=None,
        subfolder=None,
        use_instance_id=True,
        id_field="id",
    ):
        self.base_path = base_path
        self.use_parent = use_parent
        self.parent_field = parent_field
        self.extra_path = extra_path
        self.subfolder = subfolder
        self.use_instance_id = use_instance_id
        self.id_field = id_field

    def __call__(self, instance, filename):
        parts = [self.base_path]

        # تعیین بخش شناسه
        if self.use_parent:
            parent_obj = getattr(instance, self.parent_field)
            if parent_obj:
                id_value = str(parent_obj.id)
            else:
                id_value = "no_parent"
        else:
            if self.use_instance_id:
                id_value = str(getattr(instance, self.id_field))
            else:
                id_value = ""

        if id_value:
            parts.append(id_value)

        if self.extra_path:
            parts.append(self.extra_path)

        if self.subfolder:
            parts.append(self.subfolder)

        return os.path.join(*parts, filename)
