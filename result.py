import utils
from collections import defaultdict

class Result:

    def __init__(self, conf):
        self.conf = conf

        self._args = []
        self._current_arg = [0] * len(self.conf["variables"])
        self.create_args(0)
        self.data = {}

    def create_args(self, depth):
        if depth == len(self.conf["variables"]):
            self._args.append(self._current_arg[:])
            return

        key, values = self.conf["variables"][depth]

        for value in values:
            self._current_arg[depth] = (key, value)
            self.create_args(depth + 1)

    def args(self):
        return self._args

    # Reload []
    def __setitem__(self, i, y):
        self.data[i] = y

    def __getitem__(self, i):
        return self.data[i]

    def select(self, conditions):
        result = {}
        for key in self.data.keys():
            key_d = {k : v for k, v in key}
            met = True
            for k, v in conditions:
                if key_d[k] != v:
                    met = False

            if met:
                result[key] = self.data[key]

        return result

    def group_by(self, variables):
        result = {}
        svariables = set(variables)
        for key in self.data.keys():
            new_keys = {}
            value = self.data[key]
            for k, v in key:
                if k in variables:
                    new_keys[k] = v

            new_keys = utils.dict2tuple(new_keys)
            if not new_keys in result:
                result[new_keys] = []

            result[new_keys].append(value)
        
        result2 = Result(self.conf)
        result2.data = result
        return result2

    def group_except(self, variables):
        result = {}
        svariables = set(variables)
        for key in self.data.keys():
            new_keys = {}
            value = self.data[key]
            for k, v in key:
                if not k in variables:
                    new_keys[k] = v

            new_keys = utils.dict2tuple(new_keys)
            if not new_keys in result:
                result[new_keys] = []

            result[new_keys].append(value)

        result2 = Result(self.conf)
        result2.data = result
        return result2
        
    def variables(self):
        vars = set()
        for key in self.data.keys():
            for k, v in key:
                vars.add(k)

        return vars

    def map(self, mapper):
        result = Result(self.conf)
        data = defaultdict(list)
        # Map: generate many (k, v)
        for k, v in sorted(self.data.items()):
            output = mapper(k, v)
            for kk, vv in output:
                data[kk].append(vv)

        result.data = dict(data)
        return result

    def reduce(self, reducer):
        result = Result(self.conf)
        result.data = {}
        for k, v in sorted(self.data.items()):
            output = reducer(k, v)
            result.data[output[0]] = output[1]

        return result

    def mapv(self, mapper):
        return self.map(lambda k, v: [(k, mv) for mv in mapper(v)])

    def reducev(self, reducer):
        return self.reduce(lambda k, v: (k, reducer(v)))

    def squeeze(self):
        # delete singleton variables except name
        allvars = self.variables()
        non_singleton = []
        for var in allvars:
            if len(self.group_by([var]).data) > 1:
                non_singleton.append(var)
        
        if not 'name' in non_singleton:
            non_singleton.append('name')

        return self.group_by(non_singleton)

    def items(self, sort=True):
        vars = self.variables()
        if 'name' in vars:
            raise NameError('name cannot be in variables')
        #vars.remove('name')
        lvars = list(vars)
        var2id = { lvars[i] : i for i in xrange(len(lvars)) }

        #result = {}
        result = []
        for key, value in sorted(self.data.items()):
            name = ''
            arg = [0] * len(lvars)
            for k, v in key:
                arg[var2id[k]] = v
                #if k == 'name':
                #    name = v
                #else:
                #    arg[var2id[k]] = v

            #if not name in result:
            #    result[name] = []

            arg.append(value)
            result.append(arg)

        result.sort()
        return result

