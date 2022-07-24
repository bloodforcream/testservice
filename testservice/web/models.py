from django.core.validators import RegexValidator
from django.db import models


class Task(models.Model):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания задачи')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала обработки задачи')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения обработки задачи')
    result = models.JSONField(null=True, blank=True, verbose_name='Результат обработки задачи')
    csv_file_name = models.CharField(
        max_length=512,
        validators=[RegexValidator('.+\.csv$', message='Must be csv extension')],
        verbose_name='Название CSV файла'
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=20, default=PENDING, verbose_name='Статус задачи'
    )

    class Meta:
        verbose_name = 'Задача обработки CSV файла'
        verbose_name_plural = 'Задачи обработки CSV файлов'

    def __str__(self):
        return f'{self.id} - {self.csv_file_name} - {self.get_status_display()}'
