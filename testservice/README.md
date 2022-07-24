## Инструкция по установке
```
Создать .env file

POSTGRES_USER={}
POSTGRES_PASSWORD={}
POSTGRES_DATABASE={}
```
```
sudo docker-compose up -d --build
```
## Создание суперюзера
```
docker exec -it {container_id} python manage.py createsuperuser
```
## Основные методы

### GET /tasks/
    Получение списка задач в работе

### POST /tasks/
    Создание новой задачи
    {
        "csv_file_name": "three_mil_rows.csv"
    }

### GET /tasks/{id}/
    Получение результата работы задачи