build-dev:
	docker-compose -f docker-compose_dev.yaml build

build-dev-nocache:
	docker-compose -f docker-compose_dev.yaml build --no-cache

clean: stop-dev
	rm -rf data_files/data

fresh: clean build-dev-nocache run-dev

run-dev:
	docker-compose -f docker-compose_dev.yaml pull --quiet --ignore-pull-failures
	docker-compose -f docker-compose_dev.yaml up -d
	sleep 5
	docker-compose -f docker-compose_dev.yaml exec salt-master sh -c "salt \* saltutil.sync_all" > /dev/null 2>&1
	docker-compose -f docker-compose_dev.yaml stop down-minion
	docker-compose -f docker-compose_dev.yaml exec saltui sh -c "wait-for postgres:5432 -t 30 -- python manage.py migrate"
	docker-compose -f docker-compose_dev.yaml exec saltui sh -c "python manage.py createsuperuser --noinput || true"

stop-dev:
	docker-compose -f docker-compose_dev.yaml down

saltui-cmd:
	docker-compose -f docker-compose_dev.yaml exec -it -w /opt/saltui saltui sh

salt-cmd:
	docker-compose -f docker-compose_dev.yaml exec -it -w /srv salt-master sh