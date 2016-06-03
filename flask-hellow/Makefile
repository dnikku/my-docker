APP_NAME=flask-hellow
dk-build:
	docker rm  $(APP_NAME) || true
	docker rmi $(APP_NAME) || true
	docker build . -t $(APP_NAME)

dk-run:
	docker run -d --name $(APP_NAME) -p 80:80 -p 8001:8001 $(APP_NAME)

dk-shell:
	docker exec -it $(APP_NAME) "/bin/sh"

dk-logs:
	docker logs $(APP_NAME)

dk-stop:
	docker stop -t1 $(APP_NAME)
