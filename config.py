import os
import sys


class _Wrapper(dict):
    """
    Helper dictionary class, allow direct referencing values
    For example, instead of o["key"] you can use o.key to get the value for "key"
    """

    def __getattr__(self, key):
        try:
            o = self[key]
            if isinstance(o, dict) is True:
                if isinstance(o, _Wrapper) is False:
                    o = _Wrapper.create(o)
                    self[key] = o
            return o
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            pass

    @staticmethod
    def create(*args, **kwargs):
        if args and len(args) > 0:
            return _Wrapper(args[0])
        return _Wrapper(kwargs)


class Configurator(_Wrapper):
    def __init__(self, configs, env_var_pfx=None, auto_cast_env_vars=False):
        """
        Constructor for the Configurator class.
        :param configs: A list of configuration objects
        :param env_var_pfx: (optional) the environment variable prefix for loading the env var config
        :param auto_cast_env_vars: (optional) Flag specifying whether or not to cast the env var values to python types
        """

        if not isinstance(configs, list):
            assert isinstance(configs, dict), "The configs value must be a dictionary instance or list of dictionaries"
            configs = configs[configs]

        if env_var_pfx:
            configs.append(Configurator.get_env_vars(env_var_pfx, auto_cast=auto_cast_env_vars))

        for config in configs:
            self._override(config)

    def _override(self, other):
        """
        Override the current value(s) with the new value(s)
        :param other: The dictionary to override with.
        """
        assert isinstance(other, dict), "The other value must be a dictionary instance."

        def override(a, b):
            keys = b.keys()
            for key in keys:
                o = b[key]
                if isinstance(o, dict) is True:
                    try:
                        override(a[key], o)
                    except KeyError:
                        a[key] = o
                elif o is None:
                    a.pop(key, None)
                else:
                    a[key] = o

        override(self, other)
        return self

    def __repr__(self):
        return "Configurator"

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def get_env_vars(prefix, auto_cast=False):
        """
        Returns a dictionary of environment variables that start with the specified prefix.

        ex:
            # set an environment variable
            export CUSTOM_database__username="admin"

            # call
            get_env_vars("CUSTOM") will return the following:
                {
                  "database": {
                    "username": "admin"
                  }
                }

        :note:  Since periods are not allowed inside environment variables, we use double underscores to denote a period
                For example, database__username would be interpreted as database.username
        :param prefix: The prefix of the environment variables you want to return
        :param auto_cast: Flag specifying whether or not to attempt to cast the string value with the actual python type
        :return: A dictionary object
        """
        def _assign(env_vars, key, val):
            path = key.split(".")
            name = path[-1]
            for k in path[:-1]:
                if not env_vars.get(k):
                    env_vars[k] = {}
                env_vars = env_vars[k]
            env_vars[name] = val

        env_vars = {}
        env_pfx = prefix.lower()
        if not env_pfx.endswith("_"):
            env_pfx = "%s_" % env_pfx

        for key in os.environ:
            if not key.lower().startswith(env_pfx):
                continue

            val = os.environ[key]
            key = "_".join(key.split("_")[1:])
            key = key.replace("__", ".")
            if auto_cast and val:
                if val.isdigit():
                    val = int(val)
                else:
                    val = True if val == "true" else False if val == "false" else val

            _assign(env_vars, key, val)
        return env_vars


if __name__ == "__main__":
    import json
    import codecs

    # create a list of config objects using the settings and settings override file
    configurations = ["settings.json", "settings.override.json"]
    for x, c in enumerate(configurations):
        with codecs.open(c, "r", "utf-8") as f:
            data = f.read()
            cfg = json.loads(data)
            configurations[x] = cfg

    # create a configurator instance, override with environment variables starting with CUSTOM_
    config = Configurator(configurations, env_var_pfx="CUSTOM", auto_cast_env_vars=True)
    print(config.database.username)
    print(config.database.password)
    print(config.database.host)
    print(config.database.port)