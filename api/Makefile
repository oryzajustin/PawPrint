build:
	docker build -t pawprint/api:latest .

run:
	#docker run -d -p 5000:5000 pawprint/api
	docker run -d -p 5000:5000 pawprint/api

kill:
	docker kill $$(docker ps -q)
	docker rm -v $$(docker ps -a -q -f status=exited)

clean:
	docker rmi -f $$(docker images -q -f dangling=true)

run-db:
	docker run --name testdb -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:latest