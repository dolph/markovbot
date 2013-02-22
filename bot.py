"""A natural language IRC bot.

This is an example bot that uses the SingleServerIRCBot class from irc.bot. The
bot enters a channel and listens for commands in private messages and channel
traffic.  Commands in channel messages are given by prefixing the text by the
bot name followed by a colon.

The known commands are:

    disconnect: Disconnect the bot. The bot will try to reconnect after 60
                seconds.

    die: Let the bot cease to exist.

"""

import argparse
import logging

import irc.bot
import irc.strings

import markov


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler())


class MarkovBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        super(MarkovBot, self).__init__([(server, port)], nickname, nickname)
        print 'Starting'
        self.channel = channel

    def _dispatcher(self, connection, event):
        super(MarkovBot, self)._dispatcher(connection, event)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        for x in e.arguments:
            print x
        c.join(self.channel)

    def on_join(self, c, e):
        print 'Joined', self.channel

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        conn = irc.strings.lower(self.connection.get_nickname())
        if len(a) > 1 and irc.strings.lower(a[0]) == conn:
            s = markov.produce()
            c.notice(self.channel, '%s: %s' % (e.source.nick, s))
        else:
            for s in e.arguments:
                markov.consume(s)
                print s

    def do_command(self, e, cmd):
        c = self.connection
        c.notice(e.source.nick, 'shh')


def main():
    parser = argparse.ArgumentParser(description='Natural language IRC bot.')
    parser.add_argument('server')
    parser.add_argument('port', type=int, default=6667)
    parser.add_argument('channel')
    parser.add_argument('nickname')

    args = parser.parse_args()

    while True:
        try:
            bot = MarkovBot(
                args.channel, args.nickname,args.server, args.port)
            bot.start()
        except Exception as e:
            LOG.exception(e)


if __name__ == "__main__":
    main()
