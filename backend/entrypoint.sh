# /etc/init.d/nginx reload
# /etc/init.d/nginx restart
exec uvicorn main:app --host 0.0.0.0 --port 9527 --reload