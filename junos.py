from jnpr.junos import Device
from jnpr.junos.exception import (
    ConnectAuthError, ConnectTimeoutError, ConnectRefusedError
    )


class PyEZ(object):
    def __init__(self, host, username, password, timeout=5):
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout

        self.conn = Device(host=self.host, user=self.username, passwd=self.password,
                           timeout=self.timeout)

        try:
            self.conn.open()

        except ConnectAuthError as e:
            raise e

        except ConnectTimeoutError as e:
            raise e

        except ConnectRefusedError as e:
            raise e

    def get_facts(self):
        return self.conn.facts
