#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import wpbiff

package_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, package_folder)

if __name__ == '__main__':
    sys.exit(wpbiff.main(sys.argv[1:]))
