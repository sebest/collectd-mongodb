# Introduction

collectd-mongodb is a [collectd](http://www.collectd.org/) plugin that collects statistics from a MongoDB server.

This plugin is a direct port of the MongoDB C plugin that will be part of collectd 5.1, it works with Collectd 4.9.x and 4.10.x.

# Requirements

* Collectd 4.9 or later (for the Python plugin)
* Python 2.4 or later
* Python MongoDB driver 2.4 or later (https://github.com/mongodb/mongo-python-driver)

# Configuration

The plugin has some configuration options even though none are mandatory. This is done by passing parameters via the <Module> config section in your Collectd config. The following parameters are recognized:

* User - the username for authentication
* Password - the password for authentication
* Host - hostname or IP address of the mongodb server defaults to 127.0.0.1
* Port - the port of the mongodb server defaults to 27017
* Database - the databases you want to monitor defaults to "admin". You can provide more than one database. Note that the first database _must_ be "admin", as it is used to perform a serverStatus()

The following is an example Collectd configuration for this plugin:

    <LoadPlugin python>
        Globals true
    </LoadPlugin>

    <Plugin python>
        # mongodb.py is at path /opt/collectd-plugins/mongodb.py
        ModulePath "/opt/collectd-plugins/"

        Import "mongodb"
        <Module mongodb>
            Host "127.0.0.1"
            Password "password"
            Database "admin" "db-prod" "db-dev"
        </Module>
    </Plugin>

The data-sets in types.db need to be added to the types.db file given by the collectd.conf TypesDB directive. See the types.db(5) man page for more information.

If you're monitoring a secured MongoDB deployment, declaring a user with minimal read-only roles is a good practice, such as : 


    db.createUser( {
      user: "collectd",
      pwd: "collectd",
      roles: [ { role: "readAnyDatabase", db: "admin" }, { role: "clusterMonitor", db: "admin" } ]
    });
 
