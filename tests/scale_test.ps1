docker build . -t kalhasti:latest;  docker compose down;  docker compose up --scale queue=1
python scale_test1.py
docker compose up --scale queue=2 --no-recreate
python scale_test2.py