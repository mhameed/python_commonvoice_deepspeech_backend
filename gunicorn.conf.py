from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

bind = "10.1.2.100:8000"
forwarded_allow_ips = "10.1.95.117"
proxy_protocol = True
proxy_allow_ips = "10.1.95.117"
wsgi_app = 'speech_api:app'
accesslog = "logs/access.log"
errorlog = "logs/error.log"
metrics_port = 9000

def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(metrics_port)


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
