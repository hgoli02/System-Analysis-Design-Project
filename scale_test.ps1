docker build . -t kalhasti:latest;  docker compose down;  docker compose up --scale queue=1 -d
Start-Sleep -Milliseconds 1000
python test.py
Read-Host -Prompt "Press Enter to continue"
docker-compose up --force-recreate --no-deps gateway -d
docker compose up --scale queue=4 -d
Start-Sleep -Milliseconds 1000
python test.py
