import nose
import os

nose.run()

# pep8 to ignore
# E501 80 char limit per line
ignore = ['E501']

# run pep8 tests
os.system("pep8 {0} --ignore={1}".format(os.path.dirname(os.path.realpath(__file__)), ",".join(ignore)))
