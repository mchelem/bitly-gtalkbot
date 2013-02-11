#!/usr/bin/env python

from xml.etree import ElementTree
from PyGtalkRobot import GtalkRobot

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
	self.replyMessage(user, "\nYour link just got eaten by the pufferfish!")


    # Shows help text
    def command_003_help(self, user, message, args):
	'''(help)'''
	print user, "executed a command: help"
	self.usercommands.append([user.getStripped(), "help"])
	self.replyMessage(user, "\n I save links starting with http " + 
            "or https to bitly. Try entering a URL, such as http://bit.ly")


    # Default response. Overrides parent method to not behave like a parrot... 
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
	print user, "executed unknown command and will be ignored", args
	self.usercommands.append([user.getStripped(), "unknown command ", message])


def main():
    doc = ElementTree.parse('resources/auth.xml')
    try:
        email = doc.find('Username').text
        password = doc.find('Password').text
	super_email = doc.find('Superuser').text
    except:
        print "Error in XML file format: auth.xml"

    bot = BitlyBot()
    bot.setState('available', "I will save your links to bitly")
    bot.start(email, password)


if __name__ == "__main__":
    main()
