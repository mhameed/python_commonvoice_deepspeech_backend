#!/usr/bin/env python
import requests
import sys
import time
import pexpect as p

key = sys.argv[1]

# check that the key exists:
if not p.run('gpg -k %{k}'.format(k=key), withexitstatus=True)[1]:
    print("gpg unable to locate key: {k}".format(k=key))
    sys.exit(1)

def rephrase(pattern):
    print "Checking: %s" % pattern
    r = p.spawn('rephrase %s' %key)
    r.expect('Enter pattern:.*')
    r.sendline(pattern)
    r.expect(p.EOF, timeout=3600)
    if r.exitstatus == 0:
        # something found:
        lst = r.before.split('\r\n')
        lst.remove('')
        print '\n'.join(lst)
    sys.stdout.flush()
    return r.exitstatus


max_errors = 10
get_errors = 0
patch_errors = 0
patterns_url = 'http://10.0.0.12:5000/patterns/'

while get_errors <= max_errors:
    resp = requests.get(patterns_url)
    if resp.status_code != 200:
        sys.stderr.write('get error code is %d\n' %resp.status_code)
        time.sleep(1)
        get_errors += 1
        continue
    data = resp.json()
    answer = 'n'
    if rephrase(data['pattern']) == 0: answer = 'y'
    payload = {'token': data['token'], 'status': answer}
    while patch_errors <= max_errors:
        resp = requests.patch("%s%d" %(patterns_url, data['id']), json=payload)
        if resp.status_code == 200: break
        patch_errors += 1
        sys.stderr.write('patch error code is %d\n' %resp.status_code)
        time.sleep(1)
    if patch_errors: break
