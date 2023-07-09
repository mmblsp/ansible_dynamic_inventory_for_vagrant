#!/usr/bin/env python

import argparse
import json
import subprocess
import sys
import paramiko


def parse_args():
    parser = argparse.ArgumentParser(description="Vagrant inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()


def list_running_hosts():
    cmd = "vagrant status --machine-readable"
    status = subprocess.check_output(cmd.split(), encoding='utf-8').strip()
    hosts = []
    for line in status.split('\n'):
        (host, key, value) = line.split(',')[1:4]
        if key == 'state' and value == 'running':
            hosts.append(host)
    return hosts


def get_host_details(host):
    cmd = "vagrant ssh-config {}".format(host)
    popen = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    config = paramiko.SSHConfig()
    config.parse(popen.stdout)
    cfg = config.lookup(host)
    print(cfg)
    return {
        'ansible_ssh_host': cfg['hostname'],
        'ansible_ssh_port': cfg['port'],
        'ansible_ssh_user': cfg['user'],
        'ansible_ssh_private_key_file': cfg['identityfile'][0]
    }


def main():
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        json.dump({'vagrant': hosts}, sys.stdout)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)


if __name__ == '__main__':
    main()
