# Command to run server: gunicorn --daemon --config gunicorn.conf.py --reload django_app.wsgi:application

import os
os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://circusaidalleservice.openai.azure.com/'
os.environ['AZURE_OPENAI_API_KEY'] = '0bd39cf3951c49b18243e257dd1eda17'

# The number of worker processes for handling requests
workers = 5

# The socket to bind
bind = '0.0.0.0:3000'

# The number of seconds a worker can handle a request before being terminated
timeout = 500

# The logging level
loglevel = 'debug'

# Specify the location for log files
errorlog = '/home/ubuntu/CircusAI/application/backend/django_app/error.log'
accesslog = '/home/ubuntu/CircusAI/application/backend/django_app/access.log'

# If running behind a load balancer, use the forwarded IP
forwarded_allow_ips = '*'

# Static file serving
static_map = {'/static': '/home/ubuntu/CircusAI/application/backend/django_app/staticfiles'}
