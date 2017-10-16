#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

global basepath
basepathswitch = {
    "davidperezmillan-mycrybot-5060192":"/home/ubuntu/workspace/airtrap",
    "alpha_server":"/home/david/script/airtrap"
    }
basepath=basepathswitch[socket.gethostname()]
basepathlog = '{0}/logs/'.format(basepath)
basepathlogplugins = '{0}/logs/plugins/'.format(basepath)




