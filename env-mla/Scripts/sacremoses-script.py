#!d:\benutzer\popik\desktop\git\mla\env-mla\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sacremoses==0.0.43','console_scripts','sacremoses'
__requires__ = 'sacremoses==0.0.43'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('sacremoses==0.0.43', 'console_scripts', 'sacremoses')()
    )
