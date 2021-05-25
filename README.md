# Foodgram
### Описание
Дипломный проект Яндекс.Практикум.\
Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск проекта
- Установить Docker согласно инструкции https://docs.docker.com/engine/install/
- Установить Docker-compose согласно инструкции https://docs.docker.com/compose/install/
- Клонировать репозиторий командой 
```bash
git clone git@github.com:kuzminArtur/foodgram-project.git
```
- В корне проекта выполнить
```bash
docker-compose up
```
- При первом запуске так же следует выполнить
```bash
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```
- Для загрузки ингредиентов выполнить
```bash
python3 manage.py load_ingredient
```
- Для создания тегов выполнить
```bash
python3 manage.py create_tags
```

## Альтернативный вариант с использованием make
- Запуск проекта:
```bash
make up
```
- Выполнение миграций
```bash
make migrate
```
- Создание суперпользователя
```bash
make createsu
```
- Сбор статики
```bash
make collectstatic
```

- Остановка проекта
```bash
make down
```
- Пересборка образа
```bash
make build
```
### Автор
Студент Яндекс.Практикума Кузьмин Артур