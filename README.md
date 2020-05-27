# vpn-mobileconfig-generator

Generates a macOS VPN .mobileconfig file without needing ProfileManager on macOS Server

example:

```./generator.py -u "USER" -p "Password123" -s "Shared$ecret!" -v "vpn.server.com" -c "Company Name"```
Or
```./generator.py -s "Shared$ecret!" -v "vpn.server.com" -c "Company Name"```

## Important note about security of the file created with script

The configuration profile will contain the user name and passwords in clear text. If VPN configuration profile gets into the wrong hands, this will allow anyone to simply install to their Mac and gain access to the network via VPN.

For this reason, it is strongly recommended only the shared Secret be added, and you omit the user and password while creating profile.

When another App is used such as Apple Configurator 2, it will mask the Shared Secret in file by base64 encoding it.
This generator puts it in as clear text - your Shared Secret, User Name, and Password are all visible in clear text.

This is a quick method to build a profile and distribute it, if you have been unlucky enough to update your Apple Configurator 2 app to Version 2.12.1 (4A20) and found Apple have removed the option to include shared secret. Other means of creating and distributing vpn profiles is highly advised.

## From FoundationPlist.py

<https://github.com/munki/munki/blob/master/code/client/munkilib/FoundationPlist.py>
<https://github.com/mbonne/vpn-mobileconfig-generator/blob/master/munkilib/FoundationPlist.py>

```python
"""
FoundationPlist.py -- a tool to generate and parse OS X .plist files.
This is intended as a drop-in replacement for Python's included plistlib,
with a few caveats:\
    - readPlist() and writePlist() operate only on a filepath,
        not a file object.
    - there is no support for the deprecated functions:
        readPlistFromResource()
        writePlistToResource()
    - there is no support for the deprecated Plist class.
The Property List (.plist) file format is a simple XML pickle supporting
basic object types, like dictionaries, lists, numbers and strings.
Usually the top level object is a dictionary.
To write out a plist file, use the writePlist(rootObject, filepath)
function. 'rootObject' is the top level object, 'filepath' is a
filename.
To parse a plist from a file, use the readPlist(filepath) function,
with a file name. It returns the top level object (again, usually a
dictionary).
To work with plist data in strings, you can use readPlistFromString()
and writePlistToString().
"""
```

No mention of 'data' for your XML. Only basic objects are supported.

## hiding password in base64 encoding insecure obfuscation only

With that said, use your judgement.
<https://stackoverflow.com/questions/157938/hiding-a-password-in-a-python-script-insecure-obfuscation-only>

[Base64](https://docs.python.org/3/library/base64.html) encoding is in the standard library and will only deter casual browsing of code, but not anyone determined:

You can test it out via your python terminal.

```python
>>> import base64
>>>  print(base64.b64encode("password".encode("utf-8")))
cGFzc3dvcmQ=
>>> print(base64.b64decode("cGFzc3dvcmQ=").decode("utf-8"))
password
```
