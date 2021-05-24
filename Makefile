build:
	docker-compose build web

up:
	docker-compose up -d

down:
	docker-compose down

db:
	docker-compose up -d db

reset-db:
	docker-compose stop db && docker-compose rm -f db && docker-compose up -d db

reset-web:
	docker-compose stop web && docker-compose rm -f web && docker-compose up -d web

nginx:
	docker-compose up -d nginx

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

createsu:
	python3 manage.py createsuperuser

collectstatic:
	python3 manage.py collectstatic --noinput

fill-db:
	make migrate
	python3 manage.py createsuperuser
	python3 manage.py load_ingredient
	python manage.py filldb

shell:
	python manage.py shell_plus
