#!/usr/bin/python
# coding: utf-8

import sys
import ldap

Server = "ldap://ldapserver.fqdn.com:389"

# note the inputs should be:
# samAccountName: testuser
# put them in exactly as shown
DN, Secret, un = ["testuser@fqdn.com","password","testuser"]

# get them from cli
# DN, Secret, un = sys.argv[1:4]

print ("usage: run_filter('" + Server + "','" + DN + "','" + Secret + "','" + un + "')")


def run_filter(Server, DN, Secret, un):

    Base = "dc=amd,dc=com"
    Scope = ldap.SCOPE_SUBTREE
    Filter = "(&(objectClass=user)(sAMAccountName="+un+"))"
    Attrs = ["displayName","samAccountName"]

    result = 'unset'

    try:
        l = ldap.initialize(Server)
        l.set_option(ldap.OPT_REFERRALS, 0)
        l.protocol_version = 3
        print l.simple_bind_s(DN, Secret)
        # l.simple_bind_s(DN, Secret)
        r = l.search(Base, Scope, Filter, Attrs)
        Type,user = l.result(r,60)
        # ipdb.set_trace()
        Name,Attrs = user[0]
        if hasattr(Attrs, 'has_key') and Attrs.has_key('displayName'):
            displayName = Attrs['displayName'][0]
            print displayName
    except ldap.INVALID_CREDENTIALS:
        result = 'fail: Wrong username ili password'
    except ldap.SERVER_DOWN:
        result = 'fail: AD server not awailable'
    l.unbind()
    result = 'success: all is well'
    print result

for x in range(0, 1000):
        run_filter(Server, DN, Secret, un)

# sys.exit()
