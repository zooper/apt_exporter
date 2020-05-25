from prometheus_client import start_http_server, Gauge
from time import sleep

APT_UPDATES = Gauge('num_updates', 'Number of updates pending')
APT_SEC_UPDATES = Gauge('num_sec_updates', 'Number of security updates pending')


def apt_update_check(file):
    for row in file:
        if 'packages' in row:
            data = row.split()
            value = data[0]
            APT_UPDATES.set(value)


def apt_sec_update_check(file):
    for row in file:
        if 'security' in row:
            data = row.split()
            value = data[0]
            APT_SEC_UPDATES.set(value)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        f = open('/var/lib/update-notifier/updates-available', 'r')
        apt_update_check(f)
        apt_sec_update_check(f)
        sleep(10)
