#!/usr/bin/env python3

import pathlib
import re
import subprocess
import sys

import pyagentx

# Updater class that set OID values
class HwMonTable(pyagentx.Updater):
    def __init__(self, *args, **kwargs):
        self.sensors = list()
        p = pathlib.Path('/sys/class/hwmon')
        for x in p.iterdir():
            if x.is_dir() and re.match('^hwmon[0-9]+$', x.name):
                for y in x.iterdir():
                    if y.is_file() and re.match('^temp[0-9]+_input$', y.name):
                        name_path = x.joinpath(y.name[:-5] + 'label')
                        if name_path.exists():
                            with open(name_path, 'r') as fp:
                                name = fp.read().strip()
                        else:
                            name = 'temperature {}'.format(len(self.sensors))
                        self.sensors.append((y, name))
        super().__init__(*args, **kwargs)

    def update(self):
        for i, p in enumerate(self.sensors):
            with open(p[0], 'r') as fp:
                value = fp.read().strip()
            idx = i + 1
            self.set_INTEGER('1.1.{}'.format(idx), idx) # lmTempSensorsIndex
            self.set_OCTETSTRING('1.2.{}'.format(idx), p[1]) # lmTempSensorsDevice
            self.set_GAUGE32('1.3.{}'.format(idx), int(value)) # lmTempSensorsValue

class HwMonAgent(pyagentx.Agent):
    def setup(self):
        self.register('1.3.6.1.4.1.2021.13.16.2', HwMonTable)

if __name__ == '__main__':
    pyagentx.setup_logging()
    try:
        a = HwMonAgent()
        a.start()
    except Exception as e:
        print("Unhandled exception:", e)
        a.stop()
        sys.exit(1)
    except KeyboardInterrupt:
        a.stop()

    sys.exit(0)
