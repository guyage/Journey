import multiprocessing

bind = "0.0.0.0:8888" 
workers = 8
errorlog = '/data/logs/Journey/gunicorn.error.log'
accesslog = '/data/logs/Journey/gunicorn.access.log'
#loglevel = 'debug'
proc_name = 'Journey'