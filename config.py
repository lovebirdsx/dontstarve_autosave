import json

class Config:

    def __init__(self, path) -> None:
        self.path = path
        try:
            with open(path) as f:
                self.values = json.load(f)
        except:
            self.values = {}

    def get(self, key:str, default='') -> object:
        if key in self.values:
            return self.values[key] 
        else:
            self.set(key, default)
            return default

    def set(self, key:str, value:object) -> None:
        self.values[key] = value
        self._save()

    def _save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.values, f, sort_keys=True, indent=2)

if __name__ == "__main__":
    config = Config('test.json')
    print(config.get('hello'))
    config.set('hello', 'world')
    print(config.get('hello'))