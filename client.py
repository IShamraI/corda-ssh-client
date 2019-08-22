#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import optparse
import paramiko

transaction = 'flow start net.corda.finance.flows.CashIssueAndPaymentFlow amount: "100 CHF", issueRef: 123, recipient: "O=Alice, L=London, C=GB", anonymous: false, notary: "OU=R3 Corda, O=R3 LTD, L=London, C=GB"'

def main():
    options = optparse.OptionParser(usage='%prog [options]', description='injector')
    options.add_option('--hostname', type='str', default='127.0.0.1', help='hostname')
    options.add_option('--port', type='int', default=6789, help='port')
    options.add_option('--username', type='str', default='demou', help='username')
    options.add_option('--password', type='str', default='demop', help='password')
    options.add_option('--issue_count', type='int', default=100, help='issue_count')

    opts, args = options.parse_args()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=opts.hostname, username=opts.username,
        password=opts.password, port=opts.port)
    for _ in xrange(opts.issue_count):
        stdin, stdout, stderr = client.exec_command(transaction)
        data = stdout.read() + stderr.read()
        print data
    stdin, stdout, stderr = client.exec_command("exit")
    data = stdout.read() + stderr.read()
    client.close()

if __name__ == '__main__':
    sys.exit(main())
