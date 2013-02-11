#!/usr/bin/env python

from xml.etree import ElementTree
from PyGtalkRobot import GtalkRobot
import bitly_api

class BitlyBot(GtalkRobot):
    ''' A bot to save links to bitly 
        
    In order to use GtalkRobot functionallity, the following must hold:
    - The commands must follow the pattern command_XXX
    - The method documentation must be a regex to match the text typed in by
        the user (that's why I added the docs as a comment before the methods)
    '''

    # Saves links (starting with http or https) to bitly
    def command_001_saveToBitly(self, user, message, args):
        '''(http[s]*://.+$)'''
        print "{0} entered a link: {1}. I'm saving it to bitly.".format(user, args[0])
	self.usercommands.append([user.getStripped(), "add to bitly"])
        try:
            self.bitly_connection.bundle_link_add(self.bitly_bundle, args[0])
            self.replyMessage(user, "\nYour link just got eaten by the pufferfish!")
        except bitly_api.BitlyError:
            self.replyMessage(user, "\nSorry, the pufferfish is already full!")



    # Default response (help)
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)$'''
	print user, "said: {0}".format(message)
	self.usercommands.append([user.getStripped(), "message"])
	self.replyMessage(user, "\n I save links starting with http " + 
            "or https to bitly ({0}). ".format(self.bitly_bundle) +
            "Try entering a URL, such as http://bit.ly")


def main():
    doc = ElementTree.parse('settings.xml')
    try:
        email = doc.find('email/username').text
        password = doc.find('email/password').text
	super_email = doc.find('email/superuser').text
        bitly_bundle = doc.find('bitly/bundle_link').text
        bitly_access_token = doc.find('bitly/access_token').text

        bot = BitlyBot()
        bot.setState('available', 'I will save your links to bitly')

        bot.bitly_bundle = bitly_bundle
        bot.bitly_connection = bitly_api.Connection(
            access_token=bitly_access_token)
        
        bot.start(email, password)
    except:
        print 'Error in XML file format: settings.xml'
       


if __name__ == "__main__":
    main()
