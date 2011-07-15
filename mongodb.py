import collectd
from pymongo import Connection

class MongoStatus(object):

    def __init__(self):
        self.con = Connection()
        self.port = 27017

    def do_server_status(self):
        server_status = self.con['admin'].command('serverStatus')

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

    def submit(self, type, instance, value):
        v = collectd.Values()
        v.plugin = 'mongo'
        v.plugin_instance = str(self.port)
        v.type = type
        v.type_instance = instance
        v.values = [value, ]
        v.dispatch()

def config(obj):
    collectd.debug('config %s' % obj)

def read(data=None):
    ms = MongoStatus()
    ms.do_server_status()

collectd.register_read(read)
collectd.register_config(config)
