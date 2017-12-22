#!/usr/bin/python3.5


import argparse, time, datetime

from pysnmp.entity.rfc3413.oneliner import cmdgen


mk_oids = {'cpu-load': '1.3.6.1.2.1.25.3.3.1.2.1', 
			'ram': {'total' : '1.3.6.1.2.1.25.2.3.1.5.65536', 'used' : '1.3.6.1.2.1.25.2.3.1.6.65536'}, 
			'port' : {'status' : '1.3.6.1.2.1.2.2.1.8.X', 'name': '1.3.6.1.2.1.2.2.1.2.X', 'bytes-in' : '1.3.6.1.2.1.31.1.1.1.6.X' },
			'uptime' : '1.3.6.1.2.1.1.3.0' }

linux_oids = {'uptime': '1.3.6.1.2.1.25.1.1.0',
		'ram': {'total': '1.3.6.1.4.1.2021.4.5.0', 'free': '1.3.6.1.4.1.2021.4.6.0' },
		'swap': {'total': '1.3.6.1.4.1.2021.4.3.0', 'free': '1.3.6.1.4.1.2021.4.4.0'},
		'cpu-load': '1.3.6.1.2.1.25.3.3.1.2.196608',
		'disk': {'used':'1.3.6.1.2.1.25.2.3.1.6.X', 'total': '1.3.6.1.2.1.25.2.3.1.5.X'},
		'num-users': '1.3.6.1.2.1.25.1.5.0',
		'num-proc': '1.3.6.1.2.1.25.1.6.0'

}

parser = argparse.ArgumentParser(description='Simple Nagios plugin for monitoring Mikrotik and Linux resources written in Python 3. Github page: https://github.com/MatheusRagoso/nagios-plugins-python')


parser.add_argument('IP', action='store',  help="IP Address of SNMP Agent")

parser.add_argument('--port', action='store', default=161, help="Port SNMP of Agent")

parser.add_argument('COMMUNITY', action='store', help="Community SNMP of Agent")


parser.add_argument('--mk-cpu-load', action='store_true',  help="Get CPU Load resource of Mikrotik")

parser.add_argument('--mk-ram', action='store_true', help="Get memory RAM Usage resource of Mikrotik")

parser.add_argument('--mk-uptime', action='store_true', help='Get port traffic of Mikrotik')

parser.add_argument('--mk-port-status', action='store', metavar='OID port suffix', help='Get port status of Mikrotik')

parser.add_argument('--mk-port-traffic', action='store', metavar='OID port suffix', help='Get port traffic of Mikrotik')


parser.add_argument('--linux-cpu-load', action='store_true',  help="Get CPU Load resource of Linux")

parser.add_argument('--linux-ram', action='store_true', help="Get memory RAM free resource of Linux")

parser.add_argument('--linux-disk', action='store', metavar='OID partition suffix', help="Get memory Disk Usage resource of Linux")

parser.add_argument('--linux-uptime', action='store_true', help='Get port traffic of Linux')

parser.add_argument('--linux-swap', action='store_true', help='Get swap usage')

parser.add_argument('--linux-port-status', action='store', type=int, metavar='OID port suffix', help='Get port status of Linux')

parser.add_argument('--linux-port-traffic', action='store', metavar='OID port suffix', help='Get port traffic of Linux')

parser.add_argument('--linux-users', action='store_true', help='Number of users authenticated on system.')

parser.add_argument('--linux-proc', action='store_true', help='Number of process running on system.') 

parser.add_argument('--warning', action='append',  type=int, help='Limit for warning')

parser.add_argument('--critical', action='append' , type=int, help='Limit for critical')

parser.add_argument('--minimum', action='store_true', help='Sets minimum limit for warning and critical')


args = parser.parse_args()

def query_oid(oid):

	try: 
		cmdGen = cmdgen.CommandGenerator()
		errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
		    cmdgen.CommunityData(args.COMMUNITY),
		    cmdgen.UdpTransportTarget((args.IP, 161)),
		    oid
			)

		result = varBinds[0][1]

	except errorIndication:
		print(errorIndication)
		exit(3)
	except errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
		exit(3)
	except errorIndex:
		print(errorIndication)
		exit(3)

	return result


def maximum(result, v):

	if not (args.warning and args.critical):
		print("--warning and --critical is required")
		exit(3)

	exit_code = 3

	if result < args.warning[v]:
		exit_code = 0

	elif result >= args.warning[v] and result < args.critical[v]:
		exit_code = 1

	elif result >= args.critical[v]:
		exit_code = 2

	return exit_code


def minimum(result, v):

	if not (args.warning and args.critical):
		print("--warning and --critical is required")
		exit(3)

	exit_code = 3

	if result > args.warning[v]:
		exit_code = 0

	elif result <= args.warning[v] and result > args.critical[v]:
		exit_code = 1

	elif result <= args.critical[v]:
		exit_code = 2

	return exit_code


def exact(result):

	if result == 1:
		exit_code = 0

	elif result == 2:
		exit_code = 2

	else:
		exit_code = 3

	return exit_code


def limit(result, active=False, v=0):

	if args.minimum or active:
		exit_code = minimum(result, v)
	else:
		exit_code = maximum(result, v)

	return exit_code


def k2m(k):

	if k > 1000:
		return (k / 1000, "Mbps")
	else:
		return (k, "Kbps")



def cpu_load(oid):

	result = query_oid(oid)
	response = "CPU Load is {}%.".format(result)
	exit_code = limit(result)
	return (response, exit_code)


def ram(oid):

	total_result = query_oid(oid['total'])
	used_result = query_oid(oid['used'])
	usage = (used_result * 100) / total_result
	response = "Memory Usage is {:.1f}%.".format(float(usage))
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


def port_traffic(oid, port_suffix):

	if (args.warning and args.critical) and ( len(args.warning) < 2 or len(args.critical) < 2):
		print("--warning and --critical must have two arguments (IN OUT)")
		exit(3)

	oid_in = oid.replace('X', port_suffix)
	oid_out = oid_in.split('.')
	oid_out[10] = '10'
	oid_out = '.'.join(oid_out)

	oid_name = mk_oids['port']['name'].replace('X', port_suffix)
	bytes_in = query_oid(oid_in)
	time_in = time.time()
	time.sleep(1)
	bytes_in_2 = query_oid(oid_in)
	time_in_2 = time.time()
	bytes_in_sec = (bytes_in_2 - bytes_in) / (time_in_2 - time_in)
	kbits_in = (bytes_in_sec / 1024) * 8

	bytes_out = query_oid(oid_out)

	time_out = time.time()
	time.sleep(1)
	bytes_out_2 = query_oid(oid_out)
	time_out_2 = time.time()
	bytes_out_sec = (bytes_out_2 - bytes_out) / (time_out_2 - time_out)
	kbits_out = (bytes_out_sec / 1024) * 8

	port_name = query_oid(oid_name)

	exit_codes = []
	exit_codes.append(limit(kbits_in, True))
	exit_codes.append(limit(kbits_out, True))
	exit_codes.append(limit(kbits_in, True, 1))
	exit_codes.append(limit(kbits_out, True, 1))

	output_out = k2m(kbits_out)
	output_in = k2m(kbits_in)
	response = "{} traffic is: Out {:.2f} {} / In {:.2f} {}.".format(port_name, float(output_out[0]), output_out[1], float(output_in[0]), output_in[1])
	exit_code = max(exit_codes)

	return (response, exit_code)



def uptime(oid):

	ticks = query_oid(oid)
	seconds = int(ticks / 100)
	days = int(ticks / 8640000)
	exit_code = limit(days, True)
	response = "Uptime is {}".format(datetime.timedelta(seconds=seconds))

	return (response, exit_code)


def linux_ram(oid):
	free = query_oid(oid['free'])
	total = query_oid(oid['total'])
	free = (free * 100) / total
	used = float(100 - free)
	exit_code = limit(used)
	response = "Memory usage is {:.2f}%".format(used)
	return (response, exit_code)

def linux_disk(oid, partition_suffix):
	
	used = query_oid(oid['used'].replace('X', partition_suffix))
	total = query_oid(oid['total'].replace('X', partition_suffix))
	free = ((total - used) * 100) / total
	free = float(100 - free)
	exit_code = limit(free)
	response = "Disk usage is  {:.2f}%".format(free)
	return (response, exit_code)

def linux_num_users(oid):
	num = query_oid(oid)
	exit_code = limit(num)
	response = "{} Users currently logged in".format(num)
	return (response, exit_code)

def linux_num_proc(oid):
	num = query_oid(oid)
	exit_code = limit(num)
	response = "{} Running processes currently".format(num)
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

elif args.mk_port_traffic:

	feedback = port_traffic(mk_oids['port']['bytes-in'], args.mk_port_traffic)
	print(feedback[0])
	exit(feedback[1])

elif args.mk_uptime:

	feedback = uptime(mk_oids['uptime'])
	print(feedback[0])
	exit(feedback[1])

elif args.linux_uptime:
	feedback = uptime(linux_oids['uptime'])
	print(feedback[0])
	exit(feedback[1])

elif args.linux_ram:
	feedback = linux_ram(linux_oids['ram'])
	print(feedback[0])
	exit(feedback[1])

elif  args.linux_cpu_load:
	feedback = cpu_load(linux_oids['cpu-load'])
	print(feedback[0])
	exit(feedback[1])

elif  args.linux_disk:
	feedback = linux_disk(linux_oids['disk'], args.linux_disk)
	print(feedback[0])
	exit(feedback[1])

elif args.linux_users:
	feedback = linux_num_users(linux_oids['num-users'])
	print(feedback[0])
	exit(feedback[1])

elif args.linux_proc:
	feedback = linux_num_proc(linux_oids['num-proc'])
	print(feedback[0])
	exit(feedback[1])

elif args.linux_swap:
	feedback = linux_ram(linux_oids['swap'])
	print(feedback[0])
	exit(feedback[1])
