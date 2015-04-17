import os
APP_ID = 'dev~alexastocks'
os.environ['SERVER_SOFTWARE'] = 'DevelopmentEnv'
os.environ['APPLICATION_ID'] = APP_ID
HTTP_HOST = 'localhost'
os.environ['HTTP_HOST'] = HTTP_HOST

from google.appengine.ext import testbed
from webapp2_extras import sessions

import unittest
import webtest
from main import app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        # reactivate every run
        self.testbed = _testbed = testbed.Testbed()

        _testbed.setup_env(
            app_id=APP_ID,
            HTTP_HOST=HTTP_HOST,
            SERVER_SOFTWARE='DevelopmentEnv',
            current_version_id='testbed.version',  # needed because endpoints expects a . in this value
            overwrite=True
        )
        _testbed.activate()
        _testbed.init_app_identity_stub()
        _testbed.init_all_stubs()

        self.app = webtest.TestApp(app)


    def assertResponseOK(self, resp, msg=None):
        self.assertEquals(200, resp.status_int)

    def tearDown(self):
        # deactivate every run so we can reactivate
        self.testbed.deactivate()