# -*- coding: utf-8 -*-

import sys
import os
from wpbiff import cli

package_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, package_folder)

if __name__ == '__main__':
    sys.exit(cli.main())
