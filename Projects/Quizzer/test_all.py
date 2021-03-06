#!flask/bin/python
# -*- coding: utf-8 -*-
import os
import unittest
from config import basedir

coverage_enabled = False

if coverage_enabled:
    from coverage import coverage
    cov = coverage(branch=True, omit=['flask/*', 'test_all.py', 'testcases/*'])
    cov.start()

from testcases.test_models import ModelsTestCase

        
if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    if coverage_enabled:
        cov.stop()
        cov.save()
        print("\n\nCoverage Report:\n")
        cov.report()
        print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
        cov.html_report(directory='tmp/coverage')
        cov.erase()