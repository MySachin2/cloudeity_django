import digitalocean
from digitalocean import SSHKey
from pprint import pprint
from libcloud.compute.types import Provider as ComputeProvider
from libcloud.dns.types import Provider as DNSProvider
from libcloud.compute.providers import get_driver as get_compute_driver
from libcloud.dns.types import RecordType
from libcloud.dns.providers import get_driver as get_dns_driver
import os
from restapi.firebase import *
local_username =  os.popen("whoami").read().replace('\n', '')

def createServerDO(token,uid,server_name):
    if not connectServerDO(token):
        return (None,'Invalid API','ERR')
    addAPISteptoDB(server_name,uid,'0','Droplet Successfully Created')
    user_ssh_key = open('/home/' + local_username +'/.ssh/id_rsa.pub').read()
    if not addSSHKeyDO(user_ssh_key,token):
        return (None,'Error adding SSH Key','ERR')
    addAPISteptoDB(server_name,uid,'1','SSH Key Added to Account')
    server = createDropletDO(token,server_name)
    addAPISteptoDB(server_name,uid,'2','Droplet Created')
    addDroplettoUser(server.ip_address,uid)
    return (server.ip_address,'Success','SUC')

def createServerAWS(api,secret):
    (compute_driver,dns_driver) = connectServerAWS(api,secret)
    node = createDropletAWS(compute_driver)
    addDomainAWS(dns_driver,node,domain)

def createServerGCP(service_account_email,project_id,json_key):
    (compute_driver,dns_driver) = connectServerGCP(service_account_email,project_id,json_key)
    node = createDropletGCP(compute_driver)
    addDomainGCP(dns_driver,node,domain)

def connectServerDO(token):
    try:
        manager = digitalocean.Manager(token=token)
        return True
    except Exception as e:
        print(e)
    return False

def addSSHKeyDO(ssh_key,token):
    try:
        key = SSHKey(token=token,
                     name='StartACloudKey',
                     public_key=ssh_key)
        key.create()
    except Exception as e:
        exception_str = str(e)
        if not exception_str.startswith('SSH Key is already in use'):
            return False
    return True

def createDropletDO(token,server_name):
    manager = digitalocean.Manager(token=token)
    keys = manager.get_all_sshkeys()
    droplet = digitalocean.Droplet(token=token,
                                   name=server_name,
                                   region='blr1',
                                   image='ubuntu-16-04-x64',
                                   size_slug='1gb',
                                   ssh_keys=keys,
                                   backups=False)
    droplet.create()
    actions = droplet.get_actions()
    for action in actions:
        print "Droplet in Progress"
        if action.wait():
            print "Droplet Created"
            my_droplets = manager.get_all_droplets()
            index = len(my_droplets)-1
            return my_droplets[index]
    return None

def addDomainDO(ip_address,token,domain):
    domain = digitalocean.Domain(name=domain, ip_address=ip_address,token=token)
    domain.create()
    domain.create_new_domain_record(type='CNAME',name='www',data='@')

def connectServerAWS(api,secret):
    try:
        cls = get_compute_driver(ComputeProvider.EC2)
        compute_driver = cls(api, secret,region='ap-south-1')
        cls = get_dns_driver(DNSProvider.ROUTE53)
        dns_driver = cls(api, secret)
        return (compute_driver,dns_driver)
    except Exception as e:
        print(e)
    return (None,None)

def createDropletAWS(compute_driver):
    dns_driver = cls(api, secret)
    IMAGE_ID = 'ami-0189d76e'
    SIZE_ID = 't2.micro'
    try:
    	compute_driver.ex_import_keypair('startacloud','~/.ssh/id_rsa.pub')
    	compute_driver.ex_create_security_group('security_group',description='Startacloud Security group')
    except Exception:
    	pass

    compute_driver.ex_authorize_security_group('security_group',from_port='22',to_port='22',cidr_ip='0.0.0.0/0')
    compute_driver.ex_authorize_security_group('security_group',from_port='80',to_port='80',cidr_ip='0.0.0.0/0')
    compute_driver.ex_authorize_security_group('security_group',from_port='443',to_port='443',cidr_ip='0.0.0.0/0')
    compute_driver.ex_authorize_security_group('security_group',from_port='8080',to_port='8080',cidr_ip='0.0.0.0/0')

    sizes = compute_driver.list_sizes()
    images = compute_driver.list_images()
    size = [s for s in sizes if s.id == SIZE_ID][0]
    image = [i for i in images if i.id == IMAGE_ID][0]
    nodes = []

    nodes.append(compute_driver.create_node(ex_keyname='startacloud',name='startacloud-node', image=image, size=size, ex_security_groups = ['security_group']))
    completed_nodes = compute_driver.wait_until_running(nodes)
    for n in completed_nodes:
        node = n
    return node[0]

def addDomainAWS(dns_driver,node,domain):
    try:
    	zone = dns_driver.create_zone(domain=domain)
    except Exception:
    	pass
    name = node.name
    ip = node.public_ips[0] if node.public_ips else None
    record = zone.create_record(name=name, type=RecordType.A, data=ip)
    record = zone.create_record(name='www', type=RecordType.CNAME, data=name)

def connectServerGCP(service_account_email,project_id,json_key):
    try:
        ComputeEngine = get_compute_driver(ComputeProvider.GCE)
        compute_driver = ComputeEngine(service_account_email, json_key,
                               project=project_id)
        GoogleCloudDNS = get_dns_driver(DNSProvider.GOOGLE)
        dns_driver = GoogleCloudDNS(service_account_email, json_key,
                               project=project_id)
        return (compute_driver,dns_driver)
    except Exception as e:
        print(e)
    return (None,None)

def createDropletGCP(compute_driver):
    with open('/home/' + local_username + '/.ssh/id_rsa.pub', 'r') as myfile:
        ssh_key = myfile.read()
    metadata = {'items' : [
    		{
    		'key' : 'ssh-keys',
    		'value' : 'startacloud:' + ssh_key
    		}
    	]}
    nodes = []
    nodes.append(compute_driver.create_node(name='script',size='g1-small',location='asia-south1-a',ex_network='default',image='ubuntu-1604-xenial-v20180424',ex_metadata=metadata))
    completed_nodes = compute_driver.wait_until_running(nodes)
    for n in completed_nodes:
        node = n
    return node[0]

def addDomainGCP(dns_driver,node,domain):
    try:
    	zone = dns_driver.create_zone(domain=domain)
    except Exception:
    	for zones in dns_driver.iterate_zones():
    		zone = zones
    		break
    name = node.name
    ip = node.public_ips[0] if node[0].public_ips else None
    data = {'ttl' : '300','rrdatas' : [ip]}
    record = dns_driver.create_record(name=domain + '.', zone=zone,type=RecordType.A,data=data)
    data = {'ttl' : '300', 'rrdatas' : [domain + "."]}
    record = dns_driver.create_record(name=domain + '.', zone=zone,type=RecordType.CNAME,data=data)
