import os
import setuptools
#~ execfile(os.path.join(os.path.dirname(__file__),'djangosite','setup_info.py'))
execfile(os.path.join('djangosite','setup_info.py'))
def main(): setuptools.setup(**SETUP_INFO)
if __name__ == "__main__": main()