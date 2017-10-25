# nagios-plugins-python
Nagios plugin for SNMP query of Mikrotik and Linux resources


Options
-------

`./snmp_mk_linux.py --help` will tell you everything you need. Here is the output to save you a few seconds:


```
usage: snmp_mk_linux.py [-h] [--port PORT] [--mk-cpu-load] [--mk-ram]
                        [--mk-uptime] [--mk-port-status OID port suffix]
                        [--mk-port-traffic OID port suffix] [--linux-cpu-load]
                        [--linux-ram] [--linux-disk] [--linux-uptime]
                        [--linux-port-status OID port suffix]
                        [--linux-port-traffic OID port suffix]
                        [--warning [WARNING [WARNING ...]]]
                        [--critical [CRITICAL [CRITICAL ...]]] [--minimum]
                        IP COMMUNITY

SNMP Mikrotik and Linux Getter.

positional arguments:
  IP                    IP Address of SNMP Agent
  COMMUNITY             Community SNMP of Agent

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           Port SNMP of Agent
  --mk-cpu-load         Get CPU Load resource of Mikrotik
  --mk-ram              Get memory RAM Usage resource of Mikrotik
  --mk-uptime           Get port traffic of Mikrotik
  --mk-port-status OID port suffix
                        Get port status of Mikrotik
  --mk-port-traffic OID port suffix
                        Get port traffic of Mikrotik
  --linux-cpu-load      Get CPU Load resource of Linux
  --linux-ram           Get memory RAM free resource of Linux
  --linux-disk          Get memory Disk Usage resource of Linux
  --linux-uptime        Get port traffic of Linux
  --linux-port-status OID port suffix
                        Get port status of Linux
  --linux-port-traffic OID port suffix
                        Get port traffic of Linux
  --warning [WARNING [WARNING ...]]
                        Limit for warning
  --critical [CRITICAL [CRITICAL ...]]
                        Limit for critical
  --minimum             Sets minimum limit for warning and critical
  ```
