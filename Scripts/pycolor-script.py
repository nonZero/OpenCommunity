#!C:\Users\Admin\OpenCommunity\OpenCommunity\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'ipython==1.1.0','console_scripts','pycolor'
__requires__ = 'ipython==1.1.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('ipython==1.1.0', 'console_scripts', 'pycolor')()
    )
