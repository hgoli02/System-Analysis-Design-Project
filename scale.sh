docker build . -t kalhasti:latest;  docker compose down;  docker compose up --scale queue=1
docker-compose up --force-recreate --no-deps gateway
docker compose up --scale queue=2 --no-recreate