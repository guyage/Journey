import multiprocessing

bind = "0.0.0.0:8888"
workers = 8
errorlog = '/xs/logs/Journey/gunicorn.error.log'
accesslog = '/xs/logs/Journey/gunicorn.access.log'
#loglevel = 'debug'
proc_name = 'Journey'