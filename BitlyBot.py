#!/usr/bin/env python

from xml.etree import ElementTree
from PyGtalkRobot import GtalkRobot

class BitlyBot(GtalkRobot):
    ''' A bot to save links to bitly 
        
    In order to use GtalkRobot functionallity, the following must hold:
    - The commands must follow the pattern command_XXX
    - The method documentation must be a regex to match the text typed in
        by the user
    '''

    def command_001_saveToBitly(self, user, message, args):
        # Saves links (starting with http or https) to bitly
        '''(http[s]*://.+$)'''
        print "{0} entered a link: {1}".format(user, args[0])
        print "I'm saving it to bitly"
	self.usercommands.append([user.getStripped(), "add to bitly"])
	self.replyMessage(user, "\nYour link just got eaten by the pufferfish!")


    def command_002_calculate(self, user, message, args):
        # Simple calculator implementation
	'''(^\d+(\.[0-9]+)?(e[0-9]+|E[0-9]+)?\s*(\+|\*|/|-)+\s*(\d+(\.[0-9]+)?(e[0-9]+|E[0-9]+)?)$)'''
	print user, "executed command: Calculator"
	self.usercommands.append([user.getStripped(), "calculator"])
	try:
		value = eval(message)
	except:
		self.replyMessage(user, "Error in arithmetic expression")
	else:
		self.replyMessage(user, value)


    def command_003_help(self, user, message, args):
	# 
	'''(help)'''
	print user, "executed command: help"
	self.usercommands.append([user.getStripped(), "help"])
	self.replyMessage(user, "\nBesides saving your links " +
            "(starting with http or https) to bitly, " +
            "I can also evaluate arithmetic expressions! " +
            "Try entering http://bit.ly or 40 + 2")


    def command_100_default(self, user, message, args):
        # Default response. Overrides parent method to not act like a parrot, 
        # repeating everything...
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
