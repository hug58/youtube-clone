workers = 4
max_requests = 1000
timeout = 30
bind = "0.0.0.0:8000"
preload_app = True
# accesslog = "logs/gunicorn_access.log"
# errorlog = "logs/gunicorn_error.log"

accesslog = "-"
errorlog = "-"