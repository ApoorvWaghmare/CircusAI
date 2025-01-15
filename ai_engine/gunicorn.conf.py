# Command to run server: gunicorn --daemon --config gunicorn.conf.py --reload wsgi:app

# The number of worker processes for handling requests
workers = 1

# The socket to bind
bind = '127.0.0.1:5000'

# The number of seconds a worker can handle a request before being terminated
timeout = 500

# The logging level
loglevel = 'debug'

# Specify the location for log files
errorlog = '/home/ubuntu/CircusAI/application/backend/ai_engine/error.log'
accesslog = '/home/ubuntu/CircusAI/application/backend/ai_engine/access.log'

# If running behind a load balancer, use the forwarded IP
forwarded_allow_ips = '*'

