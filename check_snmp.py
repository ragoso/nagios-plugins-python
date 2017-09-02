#!/usr/bin/python3.5

import argparse
from pysnmp.entity.rfc3413.oneliner import cmdgen

mk_oids = {'cpu-load': '1.3.6.1.2.1.25.3.3.1.2.1', 'ram': {'total' : '1.3.6.1.2.1.25.2.3.1.5.65536', 'used' : '1.3.6.1.2.1.25.2.3.1.6.65536'}, 
			'port' : {'status' : '1.3.6.1.2.1.2.2.1.8.X', 'name': '1.3.6.1.2.1.2.2.1.2.X' } }

	
	


parser = argparse.ArgumentParser(description='SNMP Checker.')

parser.add_argument('IP', action='store',  help="IP Address of SNMP Agent")
parser.add_argument('PORT', action='store', help="Port SNMP of Agent")
parser.add_argument('COMMUNITY', action='store', help="Community SNMP of Agent")

parser.add_argument('--mk-cpu-load', action='store_true',  help="Get CPU Load resource of Mikrotik")
parser.add_argument('--mk-ram', action='store_true', help="Get memory RAM Usage resource of Mikrotik")
parser.add_argument('--mk-uptime', action='store_true', help='Get port traffic of Mikrotik')
parser.add_argument('--mk-port-status', action='store', metavar='OID port suffix', help='Get port status of Mikrotik')
parser.add_argument('--mk-port-traffic', action='store', metavar='OID port suffix', help='Get port traffic of Mikrotik')

parser.add_argument('--linux-cpu-load', action='store_true',  help="Get CPU Load resource of Linux")
parser.add_argument('--linux-ram', action='store_true', help="Get memory RAM free resource of Linux")
parser.add_argument('--linux-disk', action='store_true', help="Get memory Disk Usage resource of Linux")
parser.add_argument('--linux-uptime', action='store_true', help='Get port traffic of Linux')
parser.add_argument('--linux-port-status', action='store', type=int, metavar='OID port suffix', help='Get port status of Linux')
parser.add_argument('--linux-port-traffic', action='store', metavar='OID port suffix', help='Get port traffic of Linux')


parser.add_argument('--warning', nargs='*', default=None,  type=int, help='Limit for warning')
parser.add_argument('--critical', nargs='*' , default=None, type=int, help='Limit for critical')
parser.add_argument('--minimum', action='store_true', help='Sets minimum limit for warning and critical')

args = parser.parse_args()

def query_oid(oid):
	try: 
		cmdGen = cmdgen.CommandGenerator()
		errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
		    cmdgen.CommunityData(args.COMMUNITY),
		    cmdgen.UdpTransportTarget((args.IP, args.PORT)),
		    oid
			)
	except errorIndication:
		print(errorIndication)
		exit(3)
	except errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
		exit(3)
	return varBinds[0][1]

def maximum(result):
	if not (args.warning and args.critical):
		print("--warning and --critical is required")
		exit(3)
	exit_code = 3
	if result < args.warning[0]:
		exit_code = 0
	elif result >= args.warning[0] and result < args.critical[0]:
		exit_code = 1
	elif result >= args.critical[0]:
		exit_code = 2
	return exit_code

def minimum(result):
	if not (args.warning and args.critical):
		print("--warning and --critical is required")
		exit(3)
	exit_code = 3
	if result > args.warning[0]:
		exit_code = 0
	elif result <= args.warning[0] and result > args.critical[0]:
		exit_code = 1
	elif result <= args.critical[0]:
		exit_code = 2
	return exit_code




def exact(result):
	if result == 1:
		exit_code = 0
	elif status == 2:
		exit_code = 2
	else:
		exit_code = 3
	return exit_code

def limit(result, active=False):
	if args.minimum or active:
		exit_code = minimum(result)
	else:
		exit_code = maximum(result)
	return exit_code


def cpu_load(oid):
	result = query_oid(oid)
	response = "CPU Load is {}%.".format(result)
	exit_code = limit(result)
	return (response, exit_code)

def ram(oid):
	total_result = query_oid(oid['total'])
	used_result = query_oid(oid['used'])
	usage = (used_result * 100) / total_result
	response = "RAM Usage is {:.1f}%.".format(float(usage))
	exit_code = limit(usage)
	return (response, exit_code)
 
def port_status(oid, port_suffix):
	oid = oid.replace('X', port_suffix)
	oid_name = oid.split(".")
	oid_name[9] = '2'
	oid_name = ".".join(oid_name)
	result = query_oid(oid)
	result_name = query_oid(oid_name)
	exit_code = exact(result)
	status_name = {0 : 'UP', 2 : 'DOWN', 3: 'UNKNOWN'}
	response = "{} status is {}".format(result_name, status_name[exit_code])
	return (response, exit_code)

if args.mk_cpu_load:
	feedback = cpu_load(mk_oids['cpu-load'])
	print(feedback[0])
	exit(feedback[1])
elif args.mk_ram:
	feedback = ram(mk_oids['ram'])
	print(feedback[0])
	exit(feedback[1])
elif args.mk_port_status:
	feedback = port_status(mk_oids['port']['status'], args.mk_port_status)
	print(feedback[0])
	exit(feedback[1])


