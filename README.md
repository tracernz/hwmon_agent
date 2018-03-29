# hwmon_agent

This is a quick hack to fill the lm-sensors MIB with temperature sensors from
hwmon (bit naughty, but I don't want to write something totally new and
upstream patches for network monitoring tools etc.). It was written to get CPU
temps from an Odroid C2 running mainline kernel into librenms. It probably
belongs in a gist but this will be easier for me to find one day when I need it.

## pyagentx dep

This script requires python 3.5+, but there exists no official release of
pyagentx that is compatible with python 3. It works with @ondrejmular's patch
found at https://github.com/rayed/pyagentx/pull/17. If you have some free time
please pick up the maintenance of pyagentx: https://github.com/rayed/pyagentx#looking-for-a-new-maintainer
