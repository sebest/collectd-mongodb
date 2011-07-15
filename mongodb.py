import collectd
from pymongo import Connection


class MongoDB(object):

    def __init__(self):
        self.plugin_name = "mongo"
        self.mongo_host = "127.0.0.1"
        self.mongo_port = 27017
        self.mongo_db = "admin"
        self.mongo_user = None
        self.mongo_password = None

    def submit(self, type, instance, value):
        v = collectd.Values()
        v.plugin = self.plugin_name
        v.plugin_instance = str(self.mongo_port)
        v.type = type
        v.type_instance = instance
        v.values = [value, ]
        v.dispatch()

    def do_server_status(self):
        con = Connection(host=self.mongo_host, port=self.mongo_port)
        db = con[self.mongo_db]
        if self.mongo_user and self.mongo_password:
            db.authenticate(self.mongo_user, self.mongo_password)
        server_status = db.command('serverStatus')

        # operations
        for k, v in server_status['opcounters'].items():
            self.submit('total_operations', k, v)

        # memory
        for t in ['resident', 'virtual', 'mapped']:
            self.submit('memory', t, server_status['mem'][t])

        # connections
        self.submit('connections', 'connections', server_status['connections']['current'])

        # locks
        self.submit('percent', 'lock_ratio', server_status['globalLock']['ratio'])

        # indexes
        accesses = server_status['indexCounters']['btree']['accesses']
        misses = server_status['indexCounters']['btree']['misses']
        self.submit('cache_ratio', 'cache_misses', accesses / float(misses) if misses else 0)

        con.disconnect()

    def config(self, obj):
        for node in obj.children:
            if node.key == 'Port':
                self.mongo_port = int(node.values[0])
            elif node.key == 'Host':
                self.mongo_host = node.values[0]
            elif node.key == 'User':
                self.mongo_user = node.values[0]
            elif node.key == 'Password':
                self.mongo_password = node.values[0]
            elif node.key == 'Database':
                self.mongo_db = node.values[0]
            else:
                collectd.warning("mongodb plugin: Unkown configuration key %s" % node.key)

mongodb = MongoDB()
collectd.register_read(mongodb.do_server_status)
collectd.register_config(mongodb.config)
