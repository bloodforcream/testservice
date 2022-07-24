import logging
from datetime import datetime

import pandas as pd
from django.conf import settings

from testservice.celery import app
from web.models import Task

logger = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 50 * 1024  # MegaBytes


@app.task
def parse_csv_file(task_id):
    task = Task.objects.get(id=task_id)
    task.status = Task.IN_PROGRESS
    task.started_at = datetime.now()
    task.save(update_fields=['status', 'started_at'])
    logger.info(f'Start processing task {task_id}')

    result = {}
    path = f'{settings.CSV_FILES_FOLDER}{task.csv_file_name}'
    with pd.read_csv(path, chunksize=DEFAULT_CHUNK_SIZE, quoting=3) as reader:
        logger.info(f'Successfully opened {task.csv_file_name} for task {task_id}')
        for chunk in reader:
            chunk = chunk.replace('"', '', regex=True)
            chunk.columns = chunk.columns.str.replace('"', '')
            chunk = chunk[chunk.columns[::10][1:]]
            for column in chunk:
                total_value_column = pd.to_numeric(chunk[column]).sum()

                existing_value = result.get(column, 0)
                result[column] = existing_value + total_value_column

    task.finished_at = datetime.now()
    task.status = Task.DONE
    task.result = result
    task.save(update_fields=['status', 'finished_at', 'result'])
    logger.info(f'Task {task_id} complete')
