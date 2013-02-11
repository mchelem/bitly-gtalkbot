#!/usr/bin/env python

from xml.etree import ElementTree
from functools import wraps
from PyGtalkRobot import GtalkRobot

import bitly_api


def bot_command(command_pattern):
    """ Decorator to register bot commands

    :param command_pattern: regular expression to match the command
    """
    def bot_command_decorator(function):
        print "Registered command {0}, with pattern {1}".format(
            function.__name__, command_pattern)
        GtalkRobot.commands.append((command_pattern, function))
        
        @wraps(function)
        def wrapper(*args):
            function(*args)
        return wrapper

    return bot_command_decorator


class BitlyBot(GtalkRobot):
    """ A bot to save links to bitly 
    """

    def __init__(self, *args, **kwargs):
        super(BitlyBot, self, *args, **kwargs).__init__()
        self.bitly_bundle = None 
        self.bitly_connection = None


    @bot_command('(http[s]*://.+$)')
    def save_to_bitly(self, user, message, args):
        """ Saves links (starting with http or https) to bitly

        :param user: the email address of the user requesting the command
        :param message: the text as entered by the user
        :param args: the list of parameters as matched on the regex
        """
        print "{0} entered a link: {1}.".format(user, args[0])
        try:
            if self.bitly_connection:

                # Either save it on the declared bundle or not into any bundle
                if self.bitly_bundle:
                    self.bitly_connection.bundle_link_add(self.bitly_bundle, args[0])
                else:
                    self.bitly_connection.user_link_save(args[0])

                self.replyMessage(user, "Your link just got eaten by the pufferfish!")
            else:
                self.replyMessage(user, "The pufferfish is not around!")

        except bitly_api.BitlyError as error:
            print error
            self.replyMessage(user, "Sorry, the pufferfish is already full!")


    @bot_command('.*?(?s)(?m)$')
    def default_command(self, user, message, args):
        """ Default response (help)

        :param user: the email address of the user requesting the command
        :param message: the text as entered by the user
        :param args: the list of parameters as matched on the regex
        """
	print user, "said: {0}".format(message)
	self.replyMessage(user, "I save links starting with http " + 
            "or https to bitly ({0}). ".format(self.bitly_bundle) +
            "Try entering a URL, such as http://bit.ly")


def main():
    doc = ElementTree.parse('settings.xml')

    email = doc.find('email/username').text
    password = doc.find('email/password').text
    super_email = doc.find('email/superuser').text
    bitly_bundle = doc.find('bitly/bundle_link').text
    bitly_access_token = doc.find('bitly/access_token').text

    bot = BitlyBot()
    bot.setState('available', 'I will save your links to bitly')

    bot.bitly_connection = bitly_api.Connection(
        access_token=bitly_access_token)
    bot.bitly_bundle = bitly_bundle

    bot.start(email, password)
       

if __name__ == "__main__":
    main()
