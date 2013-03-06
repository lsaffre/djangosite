import sys
import unittest
from unipath import Path
from sphinx import main
import six

ROOTDIR = Path(__file__).ancestor(2)
#~ raise Exception(ROOTDIR)

SOURCEDIR = Path(ROOTDIR,'docs').absolute()
BUILDDIR = Path(SOURCEDIR,'.build')

def run_sphinx_doctest():
    #~ if sys.path[0] == '':
        #~ del sys.path[0]
    #~ print sys.path    
    #~ if len(sys.argv) > 1:
        #~ raise Exception("Unexpected command-line arguments %s" % sys.argv)
    args = ['sphinx-build','-b','doctest']
    args += ['-a'] # all files, not only outdated
    args += ['-Q'] # no output
    args += ['-W'] # consider warnings as errors
    #~ args += ['-w'+Path(ROOTDIR,'sphinx_doctest_warnings.txt')]
    args += [SOURCEDIR,BUILDDIR]
    #~ args = ['sphinx-build','-b','doctest',SOURCEDIR,BUILDDIR]
    #~ raise Exception(' '.join(args))
    #~ SOURCEDIR.chdir()
    #~ import os
    #~ print os.getcwd()
    return main(args)
    

class MainTestCase(unittest.TestCase):
    def test_sphinx_doctest(self):
        exitcode = run_sphinx_doctest()
        if exitcode != 0:
            #~ six.print_("arguments to spxhinx.main() were",args)
            self.fail("""
=======================================
Sphinx doctest failed with exit code %s
=======================================
%s""" % (exitcode,Path(util.BUILDDIR,'output.txt').read_file()))
          

def suite():
    """
    This is invoked when ``python setup.py test``.
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(MainTestCase)
    return suite





