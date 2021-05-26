from grabaciones.models import GrabAdit
from datetime import datetime, date
from django.utils.timezone import make_aware


class GrabAditLog(object):

    def __init__(self, task_name):
        self.task_name = task_name

    def update(self, task_by, value, **kargs):

        today = datetime.now()
        today = make_aware(today.replace(hour=0, minute=0, second=0, microsecond=0))

        return GrabAdit.objects.update_or_create(
            task_name=self.task_name, task_by=task_by, value=value, date=today, defaults=kargs
        )
