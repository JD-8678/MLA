#!d:\benutzer\popik\desktop\git\mla\env-mla\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'chromedriver-binary==86.0.4240.22.0','console_scripts','chromedriver-path'
__requires__ = 'chromedriver-binary==86.0.4240.22.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('chromedriver-binary==86.0.4240.22.0', 'console_scripts', 'chromedriver-path')()
    )
