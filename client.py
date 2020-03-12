#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import optparse
import paramiko

# transaction = 'flow start net.corda.finance.flows.CashIssueAndPaymentFlow amount: "100 CHF", issueRef: 123, recipient: "O=Alice, L=London, C=GB", anonymous: false, notary: "OU=R3 Corda, O=R3 LTD, L=London, C=GB"'
actions = {
    'cash_issue_flow' : 'flow start CashIssueFlow amount: {amount} {currency}, issuerBankPartyRef: {issuer_ref}, notary: "{notary}"',
    'vault_query' : 'run vaultQuery contractStateType: net.corda.finance.contracts.asset.Cash$State',
    'cash_issue_and_payment_flow' : 'flow start net.corda.finance.flows.CashIssueAndPaymentFlow amount: {amount} {currency}, issueRef: {issuer_ref}, recipient: {recipient}, anonymous: false, notary: "{notary}"',
    'cash_payment_flow' : 'flow start CashPaymentFlow amount: {amount} {currency}, recipient: {recipient}',
    'cash_exit_flow' : 'flow start CashExitFlow amount: {amount} {currency}, issuerRef: {issuer_ref}',
    'graceful_shutdown' : 'run gracefulShutdown',
    'shutdown' : 'shutdown',
}

def main():
    options = optparse.OptionParser(usage='%prog [options]', description='injector')
    options.add_option('--hostname', type='str', default='127.0.0.1', help='hostname')
    options.add_option('--port', type='int', default=6789, help='port')
    options.add_option('--username', type='str', default='demou', help='username')
    options.add_option('--password', type='str', default='demop', help='password')
    options.add_option('--repeat_count', type='int', default=1, help='repeat_count')
    options.add_option('--action', type='str', default='cash_issue_flow', help='action')
    options.add_option('--amount', type='float', default=55.00, help='amount')
    options.add_option('--currency', type='str', default='USD', help='currency')
    options.add_option('--recipient', type='str', default='Party2', help='recipient')
    options.add_option('--issuer_ref', type='str', default='1234', help='issuer_ref')
    options.add_option('--notary', type='str', default='Notary', help='notary')

    opts, args = options.parse_args()

    params = {
        'amount': opts.amount,
        'currency': opts.currency,
        'issuer_ref': opts.issuer_ref,
        'notary': opts.notary,
        'recipient': opts.recipient,
    }

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=opts.hostname, username=opts.username,
        password=opts.password, port=opts.port)
    for _ in xrange(opts.repeat_count):
        transaction = actions.get(opts.action, actions['graceful_shutdown']).format(**params)
        stdin, stdout, stderr = client.exec_command(transaction)
        data = stdout.read() + stderr.read()
        print data
    stdin, stdout, stderr = client.exec_command("exit")
    data = stdout.read() + stderr.read()
    client.close()

if __name__ == '__main__':
    sys.exit(main())
