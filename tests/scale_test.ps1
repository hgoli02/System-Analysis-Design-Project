docker build . -t kalhasti:latest;  docker compose down;  docker compose up --scale queue=1
Start-Sleep -Milliseconds 1000
python scale_test1.py
Read-Host -Prompt "Press Enter to continue"
docker-compose up --force-recreate --no-deps gateway
docker compose up --scale queue=4 
Start-Sleep -Milliseconds 1000
python scale_test1.py
