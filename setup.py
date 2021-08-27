from setuptools import setup

setup(
    name='ch.kimhauser.python.remacQt5',
    version='0.0.1',
    packages=['apps', 'apps.libs', 'apps.client', 'apps.client.libs', 'apps.client.modules', 'apps.client.modules.libs',
              'apps.server', 'apps.server.libs', 'apps.server.modules', 'apps.server.modules.libs', 'libs'],
    url='http://kimhauser.ch/index.php/projects/remac',
    license='MIT',
    author='dave',
    author_email='kim@kimhauser.ch',
    description='reMac - Remote access and administration for macOS'
)
