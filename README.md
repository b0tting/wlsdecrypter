# WLSDECRYPTER
Oracle WebLogic has stored all of it's password in AES cryptstrings. As expected, these are reversible if the key is known. And given a Weblogic installation, it is, in the SerializedSystemIni.dat file. 

There are a few blogs that document how to unroll these passwords. This script will do this for you, decrypting every password it can find in the Weblogic configuration files. 
```
wlst.sh wlsdecryptor.py /data/domains/basedomain
Initializing WebLogic Scripting Tool (WLST) ...

Welcome to WebLogic Server Administration Scripting Shell

Type help() for help on available commands

Cryptstring found in: /data/domains/mydomain/./config/config.xml
Encrypted string found at line number 18
Config element: wls:credential-encrypted
{AES}W64IgZrucaEhvfecSYaLW64IgZrucaEhvfecSYaL=
Decrypted to:
welcome123

...

Parsing boot.properties: /data/domains/mydomain/./config/../servers/AdminServer/security/boot.properties
WebLogic Admin username: weblogic
WebLogic Admin password: welcome1
```
Note that this is a WebLogic scripting tool script, not pure python, using the wlst.sh shell script often found in the oracle_common directory of a Weblogic installation directory. 

# Output considerations
With the above output, you should be able to figure out which username matches the cleartext password. I took the quick route by parsing the configuration files using Sax. When asked nicely, I might refactor and use a real parser, matching actual usernames to passwords. 
