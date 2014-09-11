class dictobj(dict):

    def __init__(self, _entries=None, **kw):
        if _entries is None:
            _entries = {}
        self.update(_entries)
        self.update(kw)

    def to_json(self):
        return self

    def to_dict(self):
        return dict(self.iteritems())

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError, attr

    def __setattr__(self, attr, val):
        self[attr] = val

    def copy(self):
        return dictobj(self)
