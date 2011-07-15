# Introduction

collectd-mongodb is a [collectd](http://www.collectd.org/) plugin that collects statistics from a MongoDB server.

This plugin is a direct port of the MongoDB C plugin that will be part of collectd 5.1, it works with Collectd 4.9.x and 4.10.x.

# Requirements

* Collectd 4.9 or later (for the Python plugin)
* Python 2.6 or later (might work on 2.5 but not tested there)
* Python MongoDB driver (https://github.com/mongodb/mongo-python-driver)

# Configuration

The plugin has some configuration options even though none are mandatory. This is done by passing parameters via the <Module> config section in your Collectd config. The following parameters are recognized:

* User - the username for authentication
* Password - the password for authentication
* Host - hostname or IP address of the mongodb server defaults to 127.0.0.1
* Port - the port of the mongodb server defaults to 27017
* Database - the databases you want to monitor defaults to "admin". You can provide more than one database.

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
