#!/usr/bin/python

## Forked from https://github.com/kai-h/vpn-mobileconfig-generator
## Original Author: kai-h

import os
import sys
import uuid
import optparse
# import base64 ##If I can work out how to make an encoded data object, this might be needed.
from munkilib import FoundationPlist


def build_plist(sharedSecret, username, password, company, server):

	uuidOne = str(uuid.uuid4())
	uuidTwo = str(uuid.uuid4())

	plist = dict(
		ConsentText = dict(
			default = "Installing VPN profile for "+ company +" ",
		),
		PayloadContent = [ dict(
				#DisconnectOnIdle = 0, -Haven't needed to implement this before. Leaving out.
				IPSec = dict(
					AuthenticationMethod = "SharedSecret",
					#OnDemandEnabled = 0,
					#PromptForVPNPIN = False,
					#LocalIdentifierType = "KeyID"
					# This would usually be where <data> is placed under the SharedSecret <key>, But instead <string> is used to store the secret.
					SharedSecret = sharedSecret,
					),
				IPv4 = dict(
					OverridePrimary = 1,
					),
				PPP = dict(
					AuthName = username,
					AuthPassword = password,
					AuthenticationMethod = "Password",
					CommRemoteAddress = server,
					OnDemandEnabled = 0,
					),
				PayloadDisplayName = "VPN (" + company +")",
				PayloadEnabled = True,
				PayloadIdentifier = "com.apple.mdm." + company.lower() + ".private." + uuidOne + ".alacarte.vpn." + uuidTwo,
				PayloadType = "com.apple.vpn.managed",
				PayloadUUID = uuidTwo,
				PayloadVersion = 1,
				Proxies = dict(
					),
				UserDefinedName = company,
				VPNType = "L2TP",
				)
		],
		PayloadDisplayName = company + " VPN",
		PayloadIdentifier = "com.apple.mdm." + company.lower().replace(" ", "") + ".private." + uuidOne + ".alacarte",
		PayloadOrganization = company,
		PayloadRemovalDisallowed = False,
		PayloadScope = "User",
		PayloadType = "Configuration",
		PayloadUUID = uuidOne,
		PayloadVersion = 1,
		)

	return plist

def write_plist(plist,filename):
	FoundationPlist.writePlist(plist, filename)

def main():
	"""Main routine"""

	usage = """usage: ./%prog [options] [/path/to/profile.mobileconfig]
	   Creates a configuration profile to install your VPN.
		 Example: ./mkvpn.py -u user -p pa$$word! -s SuperS3cr3tC0de -c "Contoso" -v vpn.server.com test.mobileconfig
		 TIP: To create profile with no user or password. Use ./mkvpn.py -s SuperS3cr3tC0de -c "Contoso" -v vpn.server.com
		 The script will name the profile for you, placing it in current working directory.
	   """

	parser = optparse.OptionParser(usage=usage)

	parser.add_option('--username', '-u',
	                  help='The username for the L2TP VPN Server.')
	parser.add_option('--password', '-p',
	                  help='The password for the L2TP VPN Server.')
	parser.add_option('--secret', '-s',
	                  help='The shared secret for the L2TP VPN Server.')
	parser.add_option('--company', '-c',
	                  help='The company name for the generated Configuration Profile.')
	parser.add_option('--vpn', '-v',
	                  help='The IP Address or hostname of the VPN Endpoint.')

	if len(sys.argv) == 1:
		parser.print_usage()
		exit(0)

	options, arguments = parser.parse_args()

	if not options.secret or not options.company or not options.vpn:
		parser.print_help()
		exit(0)

## The below is returning an error: munkilib.FoundationPlist.NSPropertyListSerializationException:
## Property list invalid for format: 100 (property lists cannot contain objects of type 'CFNull')
	if not options.username and not options.password:
		username = ""
		password = ""
	else:
		username = options.username
		password = options.password

	sharedSecret = options.secret
	# Would like to be able to use this base64.b64encode(options.secret.encode("utf-8")) - but only adds the encoded text as a string object not data object in XML.
	company = options.company
	server = options.vpn

	mobileConfig = None
	if arguments:
		mobileConfig = arguments[0]
	else:
		mobileConfig = os.getcwd() +"/" + company + " VPN for " + username + ".mobileconfig"

	print ("Created Configuration Profile: " + mobileConfig)

	plist = build_plist(sharedSecret, username, password, company, server)
	write_plist(plist,mobileConfig)

if __name__ == '__main__':
    main()
