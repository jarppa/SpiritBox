#!/usr/bin/env python3

import os
import traceback
import importlib


class PluginLoadError(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return "Cannot load plugin: " + self.msg


class PluginError(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return "Plugin init error: " + self.msg


class PluginFactory:
    def __init__(self, module_prefix):
        self.modules = {}
        self._load_modules(module_prefix)

    def create(self, plugin_type, args):
        mod = self.modules.get(plugin_type)
        if mod:
            return mod.instantiate(args)
        else:
            raise PluginError(plugin_type)

    def get_available_types(self):
        return self.modules.keys()

    def _load_modules(self, prefix):
        for f in os.listdir(os.environ["SPIRITBOX_PLUGIN_DIR"]):
            if f.startswith(prefix) and f.endswith(".py"):
                try:
                    cls = importlib.import_module(f[:-3],
                                                  os.path.basename(
                                                      os.path.normpath(
                                                          os.environ["SPIRITBOX_PLUGIN_DIR"])))
                    self.modules[f[len(prefix):-3]] = cls
                except:
                    print("Cannot import module")
                    traceback.print_exc()
                    raise PluginLoadError
