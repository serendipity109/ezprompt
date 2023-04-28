# /etc/init.d/nginx reload
# /etc/init.d/nginx restart
exec uvicorn main:app --host 0.0.0.0 --port 8877 --reload