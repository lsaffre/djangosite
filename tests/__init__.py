from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('djangosite', 'project_info.py'), globals())

from djangosite.utils.pythontest import TestCase


class BaseTestCase(TestCase):
    project_root = ROOTDIR

   
class BasicTests(BaseTestCase):

    def test_01(self):
        self.assertEqual(1+1, 2)

    def test_float2decimal(self):
        self.run_docs_django_tests('tested.float2decimal.settings')

    def test_integer_pk(self):
        self.run_docs_django_tests('tested.integer_pk.settings')


class PackagesTests(BaseTestCase):
    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])

