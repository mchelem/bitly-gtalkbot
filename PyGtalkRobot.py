#!usr/bin/python
# -*- coding: utf-8 -*-

# PyGtalkRobot: A simple jabber/xmpp bot framework using Regular Expression 
# Pattern as command controller
# Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Homepage: http://code.google.com/p/pygtalkrobot/
#

"""A simple jabber/xmpp bot framework
"""

import sys, traceback
import xmpp
import re



class GtalkRobot(object):

    conn = None
    show = "available"
    status = "PyGtalkRobot"
    commands = []


    #show : xa,away---away   dnd---busy   available--online
    def setState(self, show, status_text):
        if show:
            show = show.lower()
        if show == "online" or show == "on" or show == "available":
            show = "available"
        elif show == "busy" or show == "dnd":
            show = "dnd"
        elif show == "away" or show == "idle" or show == "off" or show == "out" or show == "xa":
            show = "xa"
        else:
            show = "available"
        
        self.show = show

        if status_text:
            self.status = status_text
        
        if self.conn:
            pres=xmpp.Presence(priority=5, show=self.show, status=self.status)
            self.conn.send(pres)


    def getState(self):
        return self.show, self.status


    def replyMessage(self, user, message):
        self.conn.send(xmpp.Message(user, message))


    def getRoster(self):
        return self.conn.getRoster()


    def getResources(self, jid):
        roster = self.getRoster()
        if roster:
            return roster.getResources(jid)


    def getShow(self, jid):
        roster = self.getRoster()
        if roster:
            return roster.getShow(jid)


    def getStatus(self, jid):
        roster = self.getRoster()
        if roster:
            return roster.getStatus(jid)


    def authorize(self, jid):
        """ Authorise JID 'jid'. Works only if these JID requested auth previously. """
        self.getRoster().Authorize(jid)
    

    def controller(self, conn, message):
        matched = False
        text = message.getBody()
        user = message.getFrom()
        
        if text:
            text = text.encode('utf-8', 'ignore')
            for (pattern, function) in self.commands:
                match_obj = re.match(pattern, text)
                if(match_obj):
                    try:
                        return_value = function(self, user, text, match_obj.groups())
                        break
                    except Exception as e:
                        print traceback.format_exc()
                        self.replyMessage(user, 'I committed a grave error!')


    def presenceHandler(self, conn, presence):
        if presence:
            print "-"*100
            print presence.getFrom(), ",", presence.getFrom().getResource(), ",", presence.getType(), ",", presence.getShow()
            if presence.getType() == 'subscribe':
                jid = presence.getFrom().getStripped()
                self.authorize(jid)


    def StepOn(self):
        try:
            self.conn.Process(1)
        except KeyboardInterrupt: 
            print 'Bye!'
            return 0
        return 1


    def GoOn(self):
        while self.StepOn(): pass


    def __init__(self, server_host="talk.google.com", server_port=5223, debug=[]):
        """
            :param debug: specifies the debug IDs that will go into debug output
            :type debug: list
            
            You can either specifiy an "include" or "exclude" list. 
            The latter is done via adding "always" pseudo-ID to the list.
            
            Full list: [
                'nodebuilder', 'dispatcher', 'gen_auth', 'SASL_auth', 'bind', 
                'socket', 'CONNECTproxy', 'TLS', 'roster', 'browser', 'ibb',
            ]
        """
        self.debug = debug
        self.server_host = server_host
        self.server_port = server_port
	self.usercommands = []


    def start(self, gmail_account, password):
        """ Connect to the server and starts handling incoming messages.
        """
        jid = xmpp.JID(gmail_account)
        user, server, password = jid.getNode(), jid.getDomain(), password
        
        self.conn = xmpp.Client(server, debug=self.debug)
        conres = self.conn.connect()
        if not conres:
            print "Unable to connect to server {0}!".format(server)
            sys.exit(1)
        
        authres = self.conn.auth(user, password)
        if not authres:
            print "Unable to authorize on {0} -".format(server),\
                "Please check your name/password."
            sys.exit(1)
        
        self.conn.RegisterHandler("message", self.controller)
        self.conn.RegisterHandler('presence',self.presenceHandler)
        self.conn.sendInitPresence()
        self.setState(self.show, self.status)
        
        print "Bot started."
        self.GoOn()
