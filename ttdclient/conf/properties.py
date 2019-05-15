import os
import yaml


class Properties():

    props = None

    def __init__(self, env):
        conf_dir = os.path.dirname(os.path.realpath(__file__))
        stream = open("{0}/{1}.yaml".format(conf_dir, env))
        self.props = yaml.load(stream)

    def __getattr__(self, name):
        return self.props.get(name, None)
