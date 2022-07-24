import logging
from datetime import datetime

import pandas as pd
from django.conf import settings

from testservice.celery import app
from web.models import Task

logger = logging.getLogger(__name__)


@app.task
def parse_csv_file(task_id):
    task = Task.objects.get(id=task_id)
    task.status = Task.IN_PROGRESS
    task.started_at = datetime.now()
    task.save()
    logger.debug(f'Start processing task {task_id}')

    result = {}
    with pd.read_csv(f'{settings.CSV_FILES_FOLDER}{task.csv_file_name}', chunksize=50000, quoting=3) as reader:
        logger.debug(f'Successfully opened {task.csv_file_name} for task {task_id}')
        for chunk in reader:
            chunk = chunk.replace('"', '', regex=True)
            chunk.columns = chunk.columns.str.replace('"', '')
            chunk = chunk[chunk.columns[::10][1:]]
            for column in chunk:
                total_value_column = pd.to_numeric(chunk[column]).sum()
                if not result.get(column):
                    result[column] = total_value_column
                else:
                    result[column] += total_value_column

    task.finished_at = datetime.now()
    task.status = Task.DONE
    task.result = result
    task.save()
    logger.debug(f'Task {task_id} complete')
