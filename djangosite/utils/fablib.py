# -*- coding: UTF-8 -*-
"""
The fabric tasks I use to manage my projects.
Use at your own risk.

To be used by creating a `fabfile.py` with the following two line::

  from djangosite.utils.fablib import *
  setup_from_project("foobar")  
  
Where "foobar" is the name of your main package.
  
  
New env keys:

- django_databases : a list of directories where a manage.py exists
  and for which initdb_demo should be executed.

"""
import os
import sys
#~ def clean_sys_path():
    #~ # print sys.path
    #~ if sys.path[0] == '':
        #~ del sys.path[0]
        #~ print "Deleted working directory from PYTHONPATH"


import datetime
import unittest
#~ import subprocess
from unipath import Path
import sphinx
import six
import coverage
#~ from distutils.core import run_setup

#~ import djangosite ; print djangosite.__file__
from djangosite.utils import AttrDict
from djangosite.utils import rstgen
from timtools.tools.synchronizer import Synchronizer


from fabric.api import env, local, task, prompt
from fabric.utils import abort, fastprint, puts, warn
from fabric.contrib.console import confirm


#~ LONG_DATE_FORMAT = 


def setup_from_project(main_package):
  
    #~ env.docs_rsync_dest = 'luc@lino-framework.org'
    #~ env.sdist_dir = '../lino/docs/dl'

    #~ HOME = Path(os.path.expanduser("~"))
    #~ REMOTE = AttrDict(
      #~ lf='lino-framework.org')
    env.ROOTDIR = Path().absolute()

    env.project_name = env.ROOTDIR.absolute().name

    env.setdefault('long_date_format',"%Y%m%d (%A, %d %B %Y)"  )
    #~ env.setdefault('work_root','')
    env.work_root = Path(env.work_root)
    env.sdist_dir = Path(env.sdist_dir)
    env.django_doctests = []
    env.django_admin_tests = []
    env.django_databases = []
    env.simple_doctests = []
    env.main_package = main_package


    #~ print env.project_name

    env.DOCSDIR = Path(env.ROOTDIR,'docs')
    env.BUILDDIR = Path(env.DOCSDIR,'.build')

    if not env.DOCSDIR.exists():
        raise Exception("You must call 'fab' from a project's root directory.")
        
        
    execfile(env.ROOTDIR.child(env.main_package,'setup_info.py'),globals()) # will set SETUP_INFO 
    env.SETUP_INFO = SETUP_INFO
    


#~ def confirm(msg,default='y',others='n',**override_callbacks):
    #~ text = "%s [%s%s]" % (msg,default.upper(),others)
    #~ def y(): return True
    #~ # def n(): abort("Missing user confirmation for:\n%s" % msg)
    #~ def n(): abort("Missing user confirmation")
    #~ callbacks = dict(y=y,n=n)
    #~ callbacks.update(override_callbacks)
    #~ while True:
        #~ answer = prompt(text)
        #~ # answer = raw_input(prompt)
        #~ if not answer: 
            #~ answer = default
        #~ answer = answer.lower()
        #~ if answer: 
            #~ return callbacks.get(answer)()
            
def must_confirm(*args,**kw):
    if not confirm(*args,**kw):
        abort("Dann eben nicht...")
        
def must_exist(p):
    if not p.exists():
        abort("No such file: %s" % p.absolute())
        
def rmtree_after_confirm(p):
    must_confirm("OK to remove %s and everything under it?" % p.absolute())
    p.rmtree()
    

@task(alias='api')
def build_api(*cmdline_args):
    """
    Generate .rst files in `docs/api`.
    """
    #~ if len(env.SETUP_INFO['packages']) != 1:
        #~ abort("env.SETUP_INFO['packages'] is %s" % env.SETUP_INFO['packages'])
        
    api_dir = env.DOCSDIR.child("api").absolute()        
    rmtree_after_confirm(api_dir)
    args = ['sphinx-apidoc']
    #~ args += ['-f'] # force the overwrite of all files that it generates.
    args += ['--no-toc'] # no modules.rst file
    args += ['-o',api_dir]
    args += [env.main_package] # packagedir 
    if False: # doesn't seem to work
        excluded = [env.ROOTDIR.child('lino','sandbox').absolute()]
        args += excluded # pathnames to be ignored
    cmd = ' '.join(args)
    puts("%s> %s" % (os.getcwd(), cmd))
    #~ confirm("yes")
    local(cmd)
    
  
@task(alias='html')
def build_html(): #~ def build_html(*cmdline_args):
    """
    Build sphinx docs.
    """
    write_readme()
    #~ print cmdline_args
    args = ['sphinx-build','-b','html']
    #~ args += cmdline_args
    #~ args += ['-a'] # all files, not only outdated
    #~ args += ['-P'] # no postmortem
    #~ args += ['-Q'] # no output
    #~ args += ['-W'] # consider warnings as errors
    #~ args += ['-w'+Path(env.ROOTDIR,'sphinx_doctest_warnings.txt')]
    args += ['-w',env.DOCSDIR.child('warnings.txt')]
    args += [env.DOCSDIR,env.BUILDDIR]
    #~ sphinx.main(args)
    #~ sphinx.main(args)
    cmd = ' '.join(args)
    local(cmd)
    
    src = env.DOCSDIR.child('dl').absolute()
    if src.isdir():
        #~ from timtools.scripts import sync
        #~ sync.main(*args)
        job = Synchronizer()
        job.toolkit.configure(batch=True)
        target = env.BUILDDIR.child('dl')
        target.mkdir()
        job.addProject(src,target.absolute(),recurse=True)
        #~ job.run(safely=True,noaction=True)
        #~ job.run(safely=True)
        job.run(safely=False)
    else:
        warn("%s is not a directory" % src)
    #~ cp -ru  $(TEMPDIR)\\html    
    return 
    
    
    
@task(alias='clean')
def clean_html(*cmdline_args):
    """
    Delete all built Sphinx files.
    """
    rmtree_after_confirm(env.BUILDDIR)
    
@task(alias='pub')
def publish_docs():
    """
    Upload docs to public web server.
    """
    #~ from fabric.context_managers import cd
    cwd = Path(os.getcwd())
    env.BUILDDIR.chdir()
    #~ with cd(env.BUILDDIR):
    #~ addr = env.user+'@'+REMOTE.lf
    args = ['rsync','-r']
    args += ['--verbose'] 
    args += ['--progress'] # show progress
    args += ['--delete'] # delete files in dest
    args += ['--times'] # preserve timestamps
    args += ['--exclude','.doctrees'] 
    args += ['./'] # source
    args += [env.docs_rsync_dest+':~/public_html/'+env.project_name] # dest
    cmd = ' '.join(args)
    puts("%s> %s" % (os.getcwd(), cmd))
    #~ confirm("yes")
    local(cmd)
    cwd.chdir()
    #~ return subprocess.call(args)

def run_in_django_databases(admin_cmd,*more):
    for db in env.django_databases:
        p = env.ROOTDIR.child(db)
        # cmd = 'python manage.py initdb --noinput'
        args = ["django-admin"] 
        args += [admin_cmd]
        args += more
        #~ args += ["--noinput"]
        args += ["--settings=settings"]
        args += [" --pythonpath=%s" % p.absolute()]
        cmd = " ".join(args)
        local(cmd)
  
@task(alias="initdb")
def initdb_demo():
    """
    Run initdb_demo on each Django database of this project (env.django_databases)
    """
    #~ for db in env.django_databases:
        #~ args = ["django-admin"] 
        #~ args += ["initdb_demo --settings=%s" % prj]
        #~ args += [" --pythonpath=%s" % env.DOCSDIR]
        #~ cmd = " ".join(args)
        #~ local(cmd)
        
    #~ cwd = Path(os.getcwd())
    #~ for db in env.django_databases:
        #~ env.ROOTDIR.child(db).chdir()
        #~ # cmd = 'python manage.py initdb --noinput'
        #~ args = ["django-admin"] 
        #~ args += ["initdb_demo --settings=settings"]
        #~ args += [" --pythonpath=."]
        #~ cmd = " ".join(args)
        
        #~ local(cmd)
    #~ cwd.chdir()
    
    run_in_django_databases('initdb_demo',"--noinput")

@task()
def runserver():
    run_in_django_databases('runserver')
    
        
@task()
def run_sphinx_doctest():
    """
    Run Sphinx doctest tests. 
    Not maintained because i cannot prevent it from also trying to test 
    the documents in `django_doctests` which must be tested separately.
    """
    #~ clean_sys_path()
    #~ if sys.path[0] == '':
        #~ del sys.path[0]
    #~ print sys.path    
    #~ if len(sys.argv) > 1:
        #~ raise Exception("Unexpected command-line arguments %s" % sys.argv)
    onlythis = None
    #~ onlythis = 'docs/tutorials/human/index.rst'
    args = ['sphinx-build','-b','doctest']
    args += ['-a'] # all files, not only outdated
    args += ['-Q'] # no output
    if not onlythis:
        args += ['-W'] # consider warnings as errors
    args += [env.DOCSDIR,env.BUILDDIR]
    if onlythis: # test only this document
        args += [ onlythis ] 
    #~ args = ['sphinx-build','-b','doctest',env.DOCSDIR,env.BUILDDIR]
    #~ raise Exception(' '.join(args))
    #~ env.DOCSDIR.chdir()
    #~ import os
    #~ print os.getcwd()
    exitcode = sphinx.main(args)
    if exitcode != 0:
        output = Path(env.BUILDDIR,'output.txt')
        #~ if not output.exists():
            #~ abort("Oops: no file %s" % output)
        # six.print_("arguments to spxhinx.main() were",args)
        abort("""
=======================================
Sphinx doctest failed with exit code %s
=======================================
%s""" % (exitcode,output.read_file()))
    
@task(alias='sdist')
def setup_sdist():
    """
    Write source districution archive file.
    """
    #~ puts(env.sdist_dir)
    args = ["python", "setup.py"]
    args += [ "sdist", "--formats=gztar" ]
    args += ["--dist-dir", env.sdist_dir.child(env.SETUP_INFO['name'])]
    local(' '.join(args))
    #~ run_setup('setup.py',args)
  
@task(alias='upload')
def setup_sdist_upload():
    args = ["python", "setup.py"]
    args += ["sdist", "--formats=gztar" ]
    args += ["--dist-dir", env.sdist_dir.child(env.SETUP_INFO['name'])]
    args += ["upload"]
    local(' '.join(args))
    #~ run_setup('setup.py',args)
  
@task(alias='reg')
def setup_register():
    args = ["python", "setup.py"]
    args += ["register"]
    #~ run_setup('setup.py',args)
    local(' '.join(args))

class RstFile(object):
    def __init__(self,local_root,url_root,parts):
        self.path = local_root.child(*parts)
        self.url = url_root + "/".join(parts)
        #~ self.parts = parts
        
      
def get_blog_entry(today):
    local_root = env.work_root.child(env.blogger_project)
    parts = ('docs','blog',str(today.year),today.strftime("%m%d.rst"))
    #~ return blogdir.child(*parts)
    return RstFile(local_root,
      "http://code.google.com/p/%s/source/browse/" % env.blogger_project,
      parts)
  

@task(alias='blog')
def edit_blog_entry():
    """
    Edit today's blog entry, create an empty file if it doesn't yet exist.
    """
    today = datetime.date.today()
    entry = get_blog_entry(today)
    if not entry.path.exists():
        if confirm("Create file %s?" % entry.path):
            txt = rstgen.header(1,today.strftime(env.long_date_format))
            entry.path.write_file(txt)
    args = [env.editor]
    args += [entry.path]
    local(' '.join(args))
  
@task(alias='ci')
def checkin():
    """
    Checkin & push to repository, using today's blog entry as commit message.
    """
    write_readme()
    entry = get_blog_entry(datetime.date.today())
    #~ entry = Path(env.ROOTDIR,'..',env.blogger_project,*parts)
    #~ print env.ROOTDIR.parent.absolute()
    if not entry.path.exists():
        abort("%s does not exist!" % entry.path.absolute())
    #~ puts("Commit message refers to %s" % entry.absolute())
    args = ["hg","st"]
    local(' '.join(args))
    must_confirm("OK to checkin %s ?" % env.SETUP_INFO['name'])
    args = ["hg","ci"]
    args += ['-m', entry.url ]
    cmd = ' '.join(args)
    #~ confirm(cmd)
    local(cmd)
    local("hg push %s" % env.project_name)
    
@task()
def write_readme():
    """
    Generate README.txt file from setup_info.
    """
    readme = Path(env.ROOTDIR,'README.txt')
    txt = """\
==========================
%(name)s README
==========================

%(description)s

Description
-----------

%(long_description)s

Read more on %(url)s
""" % env.SETUP_INFO
    if readme.read_file() == txt:
        return 
    if not confirm("Overwrite %s" % readme.absolute()):
        abort
    readme.write_file(txt)
    cmd = "touch " + env.DOCSDIR.child('index.rst')
    local(cmd)
    setup_register()

@task(alias='t2')
def run_django_admin_tests():
    for prj in env.django_admin_tests:
        cmd = "django-admin test --settings=%s --verbosity=0 --traceback" % prj
        local(cmd)
  
@task(alias='t3')
def run_django_doctests():
    """
    run Django's `manage.py tests` in the `docs` 
    dir for each `django_doctests`
    """
    #~ must_exist(env.DOCSDIR.child('manage.py'))
    #~ env.DOCSDIR.chdir()
    for prj in env.django_doctests:
        args = ["django-admin"] 
        args += ["test --settings=%s --failfast" % prj]
        args += [" --verbosity=0"]
        args += [" --pythonpath=%s" % env.DOCSDIR]
        cmd = " ".join(args)
        #~ cmd = "manage.py test --settings=%s --failfast" % prj
        #~ cmd = "python runtest.py %s" % prj
        local(cmd)

@task(alias='t4')
def run_simple_doctests():
    """
    Run a normal doctest for files specified in `simple_doctests`.
    """
    os.environ['DJANGO_SETTINGS_MODULE']='lino.projects.std.settings'
    for prj in env.simple_doctests:
        cmd = "python -m doctest %s" % prj
        #~ print cmd
        local(cmd)

@task(alias='t5')
def run_django_databases_tests():    
    run_in_django_databases('test',"--noinput")


@task(alias='test')
def run_tests():
    """
    Run all tests
    """
    #~ run_sphinx_doctest()
    run_django_admin_tests() # t2
    run_django_doctests() # t3
    run_simple_doctests() # t4
    run_django_databases_tests() # t5
    

#~ @task(alias='listpkg')
#~ def list_subpackages():
    #~ # lst = list(env.ROOTDIR.walk("__init__.py"))
    #~ for fn in env.ROOTDIR.child('lino').walk('*.py'):
        #~ print fn

@task(alias='cov')
def run_tests_coverage():
    """
    Run all tests, creating coverage report
    """
    #~ clean_sys_path()
    puts("Running tests for '%s' within coverage..." % env.project_name)
    #~ env.DOCSDIR.chdir()
    source = []
    for package_name in env.SETUP_INFO['packages']:
        m = __import__(package_name)
        source.append(os.path.dirname(m.__file__))
    #~ cov = coverage.coverage(source=['djangosite'])
    if not confirm("coverage source=%s" % source):
        abort
    cov = coverage.coverage(source=source)
    #~ cov = coverage.coverage()
    cov.start()

    # .. call your code ..
    rv = run_tests()

    cov.stop()
    cov.save()

    cov.html_report()    
    return rv
    



#~ class MainTestCase(unittest.TestCase):
    #~ def test_sphinx_doctest(self):
        #~ exitcode = run_sphinx_doctest()
        #~ if exitcode != 0:
            #~ # six.print_("arguments to spxhinx.main() were",args)
            #~ self.fail("""
#~ =======================================
#~ Sphinx doctest failed with exit code %s
#~ =======================================
#~ %s""" % (exitcode,Path(env.BUILDDIR,'output.txt').read_file()))
          

#~ def suite():
    #~ """
    #~ This is invoked when ``python setup.py test``.
    #~ """
    #~ loader = unittest.TestLoader()
    #~ suite = loader.loadTestsFromTestCase(MainTestCase)
    #~ return suite



