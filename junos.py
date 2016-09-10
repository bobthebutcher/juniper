from jnpr.junos import Device
from jnpr.junos.exception import (
    ConnectAuthError, ConnectTimeoutError, ConnectRefusedError
    )


class PyEZ(object):
    def __init__(self, host, username, password, timeout=5, gather_facts=False):
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout
        self.gather_facts = gather_facts

        self.conn = Device(host=self.host, user=self.username, passwd=self.password,
                           timeout=self.timeout, gather_facts=self.gather_facts)

        if self.gather_facts:
            self.facts = self.conn.facts

        try:
            self.conn.open()

        except ConnectAuthError as e:
            raise e

        except ConnectTimeoutError as e:
            raise e

        except ConnectRefusedError as e:
            raise e

    def close_connection(self):
        self.conn.close()
        return "Connection to {0} closed".format(self.host)


    def get_facts(self, refresh=False):
        """
        Get device facts
        :param: refresh: refresh the device facts
        """
        if self.gather_facts and not refresh:
            return self.facts
        else:
            self.conn.facts_refresh()
            self.facts = self.conn.facts
            return self.facts


    def cli_command(self, command, warning=False):
        """ Debugging only, dont use this as part of workflow """
        return self.conn.cli(command=command, warning=warning)
