build:
	docker build -t pawprint/web:latest .

run:
	docker run -d -p 5005:80 pawprint/web

kill:
	docker kill $$(docker ps -q)
	docker rm -v $$(docker ps -a -q -f status=exited)

clean:
	docker rmi -f $$(docker images -q -f dangling=true)
