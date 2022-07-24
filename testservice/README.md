## Инструкция по установке
```
Создать .env file

POSTGRES_USER={}
POSTGRTES_PASSWORD={}
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

### GET tasks/
    Получение списка тасок в работе

### POST tasks/
    Создание новой таски
    {
        "csv_file_name": "three_mil_rows.csv"
    }

### GET tasks/{id}/
    Получение результата работы таски