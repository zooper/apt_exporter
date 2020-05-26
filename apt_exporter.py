from prometheus_client import start_http_server, Gauge
from time import sleep

APT_UPDATES = Gauge('num_updates', 'Number of updates pending')
APT_SEC_UPDATES = Gauge('num_sec_updates', 'Number of security updates pending')


def check_updates(file):
    for row in file:
        if 'packages' in row:
            data = row.split()
            value = data[0]
            APT_UPDATES.set(value)
        if 'security' in row:
            data = row.split()
            value = data[0]
            APT_SEC_UPDATES.set(value)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8090)
    # Generate some requests.
    while True:
        f = open('/var/lib/update-notifier/updates-available', 'r')
        check_updates(f)
        f.close()
        sleep(120)
