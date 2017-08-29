from __future__ import print_function
import importlib
from distutils.version import LooseVersion

required_packages = {'IPython' : '4.0.0',
                     'numpy' : '1.9.2',
                     'matplotlib' : '1.4.2',
                     'ipywidgets' : '4.0.x' 
                    }

problem_packages = list()
# Iterate over the required packages: If the package is not installed
# ignore the exception. If it is installed check the version and remove
# from dictionary. In the end the dictionary contains the packages
# that are not installed.
for package, required_version in required_packages.items():
    try:
        p = importlib.import_module(package)        
        # Current release of ipywidgets has a bug with the __version__
        # attribute. This was fixed in master, so for now we do not
        # check ipywidgets version.
        if package != 'ipywidgets':
            installed_version = LooseVersion(p.__version__)
            required_version = LooseVersion(required_version)
            if installed_version < required_version:
                print('{0} - required version: {1} installed version: {2}'.format(
                        p.__name__, required_version, installed_version))
                problem_packages.append(package)    
    except ImportError:
        problem_packages.append(package)
    
if len(problem_packages) is 0:
    print('All is well.')
else:
    print('The following packages are required but not installed: ' \
          + ', '.join(problem_packages))