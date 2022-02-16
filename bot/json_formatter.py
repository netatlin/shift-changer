import logging
import json


class JSONFormatter(logging.Formatter):
    """Форматер логов Селери"""
    def __init__(self):
        super().__init__()
        try:
            from celery._state import get_current_task
            self.get_current_task = get_current_task
        except ImportError:
            self.get_current_task = lambda: None

    def format(self, record):
        task = self.get_current_task()
        if task and task.request:
            record.__dict__.update(task_id=task.request.id,
                                   task_name=task.name)
        else:
            record.__dict__.setdefault('task_name', None)
            record.__dict__.setdefault('task_id', None)
        if isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg)
        else:
            message = {
                'msg': record.msg,
            }
            for attribute in (
                'asctime',
                'levelname',
                'args',
                'task_name',
                'task_id',
            ):
                if hasattr(record, attribute):
                    message[attribute] = getattr(record, attribute)

            record.msg = json.dumps(message)

        return super().format(record)
