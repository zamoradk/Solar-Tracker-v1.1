import yaml


class Configuration:
    
    def __init__(self, path_to_config):
        
        self._path = path_to_config
        
        with open(self._path, 'r') as f:
            contents = yaml.load(f, Loader=yaml.SafeLoader)
        
        self.__dict__ = contents
