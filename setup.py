from distutils.core import setup

setup(
    name='ttdclient',
    version='0.1.0',
    author='Emmanuel Job',
    author_email='emmanuel.job@accuenmedia.com',
    packages=['ttdclient'],
    scripts=[],
    url='http://www.accuenmedia.com',
    license='LICENSE.txt',
    description='A simple client for the TTD console.',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests",
    ],
)
