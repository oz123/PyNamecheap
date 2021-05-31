import json
import os
import argparse

from namecheap.client import Api, ApiError

api_key = ''  # You create this on Namecheap site
username = ''
ip_address = ''  # Your IP address that you whitelisted on the site



def get_args():
    parser = argparse.ArgumentParser(description="CLI tool to manage NameCheap.com domain records")

    parser.add_argument("--debug", action="store_true", help="If set, enables debug output")
    parser.add_argument("--sandbox", action="store_true", help="If set, forcing usage of Sandbox API, see README.md for details")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", action="store_true", help="Use to add a record")
    group.add_argument("--delete", action="store_true", help="Use to remove a record")
    group.add_argument("--list", action="store_true", help="List existing records or domains")

    parser.add_argument("--domain", type=str, default=None, help="Domain to manage")

    parser.add_argument("--type", type=str, default="A", help="Record type, default is \"A\"")
    parser.add_argument("--name", type=str, default="test", help="Record name, default is \"test\"")
    parser.add_argument("--address", type=str, default="127.0.0.1", help="Address for record to point to, default is \"127.0.0.1\"")
    parser.add_argument("--ttl", type=int, default=300, help="Time-To-Live, in seconds, default is 300")

    args = parser.parse_args()

    return args


def list_records(api, domain):
    return api.domains_dns_getHosts(domain)


def record_delete(api, domain, hostname, address, record_type="A", ttl=300):
    record = {
        "Type": record_type,
        "Name": hostname,
        "Address": address,
        "TTL": str(ttl)
    }
    api.domains_dns_delHost(domain, record)


def record_add(api, domain, record_type, hostname, address, ttl=300):
    record = {
        "Type": record_type,
        "Name": hostname,
        "Address": address,
        "TTL": str(ttl)
    }
    api.domains_dns_addHost(domain, record)


def main():
    args = get_args()

    with open(os.path.join(os.getenv("HOME"), ".config", "namecheap",
                       "namecheap.json")) as cfg:
        config = json.loads(cfg.read())

    if args.sandbox:
       api_key = config['sandbox_key']
       username = config['sandbox_username']
    else:
       api_key = config['api_key']
       username = config['username']

    ip_address = config['ip_address']
    domain = args.domain
    if domain:
        print("domain: %s" % domain)
    else:
        print("Domains:")

    api = Api(username,
              api_key,
              username,
              ip_address,
              sandbox=args.sandbox,
              debug=args.debug)

    if args.add:
        record_add(
            api,
            domain,
            args.type,
            args.name,
            args.address,
            args.ttl
        )
    elif args.delete:
        record_delete(
            api,
            domain,
            args.name,
            args.address,
            args.type
        )
    elif args.list:
        if not domain:
           [print(f"Name: {i['Name']}") for i in api.domains_getList()]
           exit()
        for line in list_records(api, domain):
            print("\t%s \t%s\t%s -> %s" % (line["Type"], line["TTL"], line["Name"], line["Address"]))
