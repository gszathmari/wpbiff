# -*- coding: utf-8 -*-

from wpbiff.plugins.ga import GoogleAuthenticator
from wpbiff.plugins.wpga import WPGoogleAuthenticator

class WPLogin:
    def __init__(self, url, username, password, user_agent):
        """
        This factory detects the remote Wordpress two-factor plugin type
        and returns the appropriate class
        """
        self.url = url
        self.username = username
        self.password = password
        self.user_agent = user_agent

    def make(self, plugin):
        """
        This method returns the appropriate module class
        """
        if plugin == "ga":
            return GoogleAuthenticator(self.url, self.username, self.password, self.user_agent)
        elif plugin == "wpga":
            return WPGoogleAuthenticator(self.url, self.username, self.password, self.user_agent)
