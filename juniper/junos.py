from lxml import etree

from jnpr.junos import Device, exception


class PyEZ(object):
    """
    Instantiate a connection to a Junos device with the pyez module
    """
    def __init__(self, host, username, password, timeout=5, gather_facts=False):
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout
        self.gather_facts = gather_facts

        self.conn = Device(host=self.host, user=self.username, passwd=self.password,
                           timeout=self.timeout, gather_facts=self.gather_facts)

        try:
            self.conn.open()

        except exception.ConnectAuthError as e:
            raise e

        except exception.ConnectTimeoutError as e:
            raise e

        except exception.ConnectRefusedError as e:
            raise e

        self.facts = self.conn.facts 
        self.rpc = self.conn.rpc

    def open_connection(self):
        """
        Open connection if not already open
        """
        if self.conn.connected:
            return "Connection to {0} already open".format(self.host)
        else:
            self.conn.open()
            return "Connection to {0} opened".format(self.host)

    def close_connection(self):
        """
        Close connection if not already closed
        """
        if not self.conn.connected:
            return "Connection to {0} already closed".format(self.host)
        else:
            self.conn.close()
            return "Connection to {0} closed".format(self.host)

    def get_facts(self, refresh=False):
        """
        Get device facts
        :param refresh: refresh the device facts
        """
        if self.gather_facts and not refresh:
            return self.facts
        else:
            self.conn.facts_refresh()
            self.facts = self.conn.facts
            self.gather_facts = True
            return self.facts

    def cli_command(self, command, warning=True):
        """ 
        Debugging only, don't use this as part of production workflow
        """
        return self.conn.cli(command=command, warning=warning)

    def get_rcp_command(self, command, get_xml=False):
        """
        Converts a junos cli command to its rpc equivalent
        :param command: junos command to convert
        :param get_xml: return command as xml tree
        :return: returns rpc comamnd as a string
        """
        result = self.conn.display_xml_rpc(command)
        if 'invalid command' in result:
            return 'Invalid command: {0}'.format(command)
        else:
            if get_xml:
                return etree.dump(result)
            return result.tag.replace('-', '_')

    def get_config(self):
        """
        Get config as XML
        :return: config as XML
        """
        return self.conn.rpc.get_config()

    def get_interface_information(self, interface_name):
        """
        Get interface info
        :param interface_name: name of interface
        :return: config as XML
        """
        if interface_name:
            return self.conn.rpc.get_interface_information(interface_name=interface_name)
        return self.conn.rpc.get_interface_information()

    def get_zones_information(self):
        """
        Get Zone info
        :return: config as XML
        """
        return self.conn.rpc.get_zones_information()
