#!flask/bin/python
import os
import sys
if sys.platform == 'win32':
    pybabel = 'flask\\Scripts\\pybabel'
else:
    pybabel = 'flask/bin/python flask/bin/pybabel'
os.system(pybabel + ' compile -d app/translations')