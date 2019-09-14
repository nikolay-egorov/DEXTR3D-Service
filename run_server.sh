clear
cd server/
echo "Loading..."
gunicorn routes:api --access-logfile - --reload  # live-reload (development only!)
