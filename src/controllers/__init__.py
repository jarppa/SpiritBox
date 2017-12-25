#!/usr/bin/env python3

import importlib
import os
import traceback
import sys

if not os.environ.get("CONTROLLER_PLUGIN_DIR"):
    CONTROLLERS_DIR = os.path.dirname(__file__)+"/plugins"
else:
    CONTROLLERS_DIR = os.environ["CONTROLLER_PLUGIN_DIR"]

sys.path.append(CONTROLLERS_DIR)


class ControllerFactory:
    def __init__(self):
        self.modules = {}
        self._load_modules()

    def create(self, control_type):
        return self.modules[control_type].instantiate()

    def get_available_types(self):
        return self.modules.keys()

    def _load_modules(self):
        for f in os.listdir(CONTROLLERS_DIR):
            if f.startswith("cntrl_") and f.endswith(".py"):
                try:
                    cls = importlib.import_module(f[:-3], os.path.basename(os.path.normpath(CONTROLLERS_DIR)))
                    self.modules[f[6:-3]] = cls
                except:
                    print("Cannot import module")
                    traceback.print_exc()


class Controller:
    def __init__(self):
        pass

    '''
        Blocking event wait
    '''
    def event(self):
        return None

    '''
        Async event wait
    '''
    def async_event_handler(self, callback):
        pass

