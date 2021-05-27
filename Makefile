build:
	docker-compose build web

up:
	docker-compose up -d

down:
	docker-compose down

db:
	docker-compose up -d db

stop_db:
	docker-compose stop -d db

reset-db:
	docker-compose stop db && docker-compose rm -f db && docker-compose up -d db

reset-web:
	docker-compose stop web && docker-compose rm -f web && docker-compose up -d web

nginx:
	docker-compose up -d nginx

migrate:
	docker-compose exec web python manage.py migrate --noinput

createsu:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

fill-db:
	make migrate
	docker-compose exec web python manage.py createsuperuser
	docker-compose exec web python manage.py load_ingredient
	docker-compose exec web python manage.py create_tags
	docker-compose exec web python manage.py filldb

shell:
	python manage.py shell_plus
