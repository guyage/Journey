import multiprocessing

bind = "0.0.0.0:9999"
workers = 8
errorlog = '/xs2/logs/Journey/gunicorn.error.log'
accesslog = '/xs2/logs/Journey/gunicorn.access.log'
#loglevel = 'debug'
proc_name = 'Journey'