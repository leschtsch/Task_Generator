import sys
import subprocess
import pkg_resources

required = {'pygame', 'pygame-gui', 'python-docx', 'lxml', 'easygui', 'latex2mathml'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
