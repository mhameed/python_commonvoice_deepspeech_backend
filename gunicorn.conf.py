bind = "10.1.2.100:8000"
forwarded_allow_ips = "10.1.95.117"
proxy_protocol = True
proxy_allow_ips = "10.1.95.117"
wsgi_app = 'speech_api:app'
accesslog = "logs/access.log"
errorlog = "logs/error.log"
