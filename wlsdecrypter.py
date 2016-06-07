__author__ = 'motting@qualogy'

import os
import sys
import weblogic.security.internal.SerializedSystemIni
import weblogic.security.internal.encryption.ClearOrEncryptedService
import xml.sax
import glob

basepath = "./config/"
domainpath = ""

class wlsHandler(xml.sax.ContentHandler):
    global pws
    lastelement = ""
    filename = ""
    found = False

    def __init__(self, filename):
        xml.sax.ContentHandler.__init__(self)
        self.filename = filename

    def startElement(self, name, attrs):
        self.lastelement = name

    def characters(self, chars = ""):
        if(chars.endswith(".xml")):
            ## Recurse into referenced XML
            decryptXml(chars)
        if chars.startswith("{AES}") or chars.startswith("{3DES}"):
            if not self.found:
                self.found = True
                print("Cryptstrings found in: " + self.filename)
            loc = self._locator
            print ("Encrypted string found at line number "+ str(loc.getLineNumber()))
            print("Config element: " + self.lastelement)
            print(chars)
            pw = decrypt(cleanCryptString(chars))
            print("Decrypted to:\n" + pw + "\n")

def cleanCryptString(crypt):
    return crypt.strip(' \t\n\r').replace("\\", "")

def decrypt(encryptedPassword):
    encryptSrv = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domainpath)
    ces = weblogic.security.internal.encryption.ClearOrEncryptedService(encryptSrv)
    return ces.decrypt(encryptedPassword)

def decryptXml(myxml):
    xmlfile = basepath + myxml
    if os.path.isfile(xmlfile):
        parser = xml.sax.make_parser()
        parser.setContentHandler(wlsHandler(xmlfile))
        parser.parse(xmlfile)

def decryptBootLine(line):
    linetype = False
    if line.startswith("username"):
        linetype = "username"
    elif line.startswith("password"):
        linetype = "password"

    if linetype:
        try:
            print("WebLogic Admin "+linetype+": " + decrypt(cleanCryptString(line[9:])))
        except:
            print("Failed decrypting " + linetype + ", cryptstring was " + cleanCryptString(line[9:]))

def decryptBootProperties():
    list = glob.glob(basepath + "../servers/*/security/boot.properties")
    if len(list):
        print("Parsing boot.properties: "+ list[0])
        props = open(list[0], 'r')
        [decryptBootLine(line) for line in props]
    else:
        print("No boot.properties file was found.")

## init stuff to check all parameters
if len(sys.argv) != 2:
    print("WebLogic password decryptor")
    print("https://github.com/b0tting/wlsdecrypter")
    print("Given a domain directory, this script will attempt to decrypt all AES cryptstrings it")
    print("can find. The result names the WLS configuration and line number where the crypt string")
    print("was found. Please open that in an editor to find the accompanying username")
    print("")
    print("Usage: ")
    print("  wlst.sh " + sys.argv[0] + " <WebLogic domain directory>")
    print("")
    print("If you are unfamiliar with the WebLogic domain setup, that's the directory containing the")
    print("startWebLogic.sh flie and the config and servers directories.")
    exit()

domainpath = sys.argv[1]
basepath = domainpath + basepath
decryptXml("config.xml")
decryptBootProperties()


