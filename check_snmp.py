import argparse
from pysnmp.entity.rfc3413.oneliner import cmdgen

mk_oids = {'cpu-load': '1.3.6.1.2.1.25.3.3.1.2.1', 'ram': {'total' : '1.3.6.1.2.1.25.2.3.1.5.65536', 'used' : '1.3.6.1.2.1.25.2.3.1.6.65536'}, 
	'port-status' : '1.3.6.1.2.1.2.2.1.8.X' }

parser = argparse.ArgumentParser(description='SNMP Checker.')

parser.add_argument('IP', action='store',  help="IP Address of SNMP Agent")
parser.add_argument('PORT', action='store', help="Port SNMP of Agent")
parser.add_argument('COMMUNITY', action='store', help="Community SNMP of Agent")

parser.add_argument('--mk-cpu-load', action='store_true',  help="Get CPU Load resource of Mikrotik")
parser.add_argument('--mk-ram', action='store_true', help="Get memory RAM free resource of Mikrotik")
parser.add_argument('--mk-port-uptime', action='store_true', help='Get port traffic of Mikrotik')
parser.add_argument('--mk-port-status', action='store', metavar='OID port suffix', help='Get port status of Mikrotik')
parser.add_argument('--mk-port-traffic', action='store', metavar='OID port suffix', help='Get port traffic of Mikrotik')


parser.add_argument('--warning', nargs='*', default=0,  type=int, required=True, help='Limit for warning')
parser.add_argument('--critical', nargs='*' , default=0, type=int, required=True, help='Limit for critical')
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
	exit_code = 3
	if result < args.warning[0]:
		exit_code = 0
	elif result >= args.warning[0] and result < args.critical[0]:
		exit_code = 1
	elif result >= args.critical[0]:
		exit_code = 2
	return exit_code

def minimum(result):
	exit_code = 3
	if result > args.warning[0]:
		exit_code = 0
	elif result <= args.warning[0] and result > args.critical[0]:
		exit_code = 1
	elif result <= args.critical[0]:
		exit_code = 2
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

print(args)
if args.mk_cpu_load:
	feedback = cpu_load(mk_oids['cpu-load'])
	print(feedback[0])
	exit(feedback[1])
elif args.mk_ram:
	feedback = ram(mk_oids['ram'])
	print(feedback[0])
	exit(feedback[1])


