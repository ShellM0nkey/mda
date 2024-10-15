#!/usr/bin/env python

import sys, getopt, os, errno, json, subprocess, tempfile

def usage():
    print ("""Usage: %s
    Performs onboarding\offboarding to WDATP locally with tagging support.
""" % sys.argv[0])
    pass

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hc:t:', ['help', 'config=', 'tag='])

    tags = ''
    for k, v in opts:
        if k == '-h' or k == '--help':
            usage()
            sys.exit(0)
        elif k == '-t' or k == '--tag':
            tags = v  # Store the tags from the command line

except getopt.GetoptError as e:
    print (e)
    print ('')
    usage()
    sys.exit(2)

try:
    destfile = '/etc/opt/microsoft/mdatp/mdatp_onboard.json'

    if os.geteuid() != 0:
        print('Re-running as sudo (you may be required to enter sudo''s password)')
        os.execvp('sudo', ['sudo', 'python'] + sys.argv)  # final version

    print('Generating %s ...' % destfile)

    cmd = "sudo mkdir -p '%s'" % (os.path.dirname(destfile))
    subprocess.check_call(cmd, shell=True)

    # Onboarding template with optional tags
    onboarding_info = '''{
      "onboardingInfo": "{\\\"body\\\":\\\"{\\\\\\\"previousOrgIds\\\\\\\":[],\\\\\\\"orgId\\\\\\\":\\\\\\\"79a7a33e-579c-444b-81ed-10ae90e61800\\\\\\\",\\\\\\\"geoLocationUrl\\\\\\\":\\\\\\\"https://edr-neu.eu.endpoint.security.microsoft.com/edr/\\\\\\\",\\\\\\\"datacenter\\\\\\\":\\\\\\\"NorthEurope\\\\\\\",\\\\\\\"vortexGeoLocation\\\\\\\":\\\\\\\"EU\\\\\\\",\\\\\\\"vortexServerUrl\\\\\\\":\\\\\\\"https://eu-v20.events.endpoint.security.microsoft.com/OneCollector/1.0\\\\\\\",\\\\\\\"vortexTicketUrl\\\\\\\":\\\\\\\"https://events.data.microsoft.com\\\\\\\",\\\\\\\"partnerGeoLocation\\\\\\\":\\\\\\\"GW_EU\\\\\\\",\\\\\\\"version\\\\\\\":\\\\\\\"1.7\\\\\\\",\\\\\\\"deviceType\\\\\\\":\\\\\\\"Server\\\\\\\",\\\\\\\"tags\\\\\\\":\\\\\\\"%s\\\\\\\"}\\\"}"
    }''' % tags

    with open(destfile, "w") as json_file:
        json_file.write(onboarding_info)

    print(f"Onboarding completed with tags: {tags}")

except Exception as e:
    print(f"Failed with error: {e}")
    sys.exit(1)
