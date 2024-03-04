import sys
import requests
import json
import os.path
import os
import random
import shutil
import re
from pyunpack import Archive
from os import path
from requests.exceptions import HTTPError

def downloadFile(fileName, fileUrl, bearer):
   try:
      response = requests.get(
         fileUrl,
         headers={'User-Agent': 'liftinstall (j-selby)', 'Authorization': 'Bearer ' + bearer},
         allow_redirects=True)

      response.raise_for_status()

   except Exception as err:
      sys.exit()
   else:
      if response.status_code == 200:
         try:
            open(fileName, 'wb').write(response.content)
         except:
            sys.exit()
      else:
         sys.exit()

def getFiles(bearer):
   if not os.path.exists("version.txt"):
    open("version.txt", 'w').close()
   vfile = open('version.txt')
   zipname=str(vfile.read())

   try:
      response = requests.get(
         'https://api.yuzu-emu.org/downloads/earlyaccess/',
         headers={'User-Agent': 'liftinstall (j-selby)'})

      response.raise_for_status()

   except Exception as err:
      sys.exit()
   else:
	   
      if response.status_code == 200:
         try:
            jsonresponse = json.loads(response.text)
         except:
            sys.exit()

         version = jsonresponse["version"]
         files = jsonresponse["files"]
         filename = ""
         for file in files:
            if (".zip" in file["name"] and "debugsymbols" not in file["name"]):
                dir_path = os.listdir(os.getcwd())
                dir_name = os.getcwd()
                for item in dir_path:
                    if (item.endswith(".zip")) and ("YuzuEA-" in item):
                        os.remove(os.path.join(dir_name, item))
                downloadFile(file["name"], file["url"], bearer)
                filename = file["name"]
	       
            if (".AppImage" in file["name"]):
                dir_path = os.listdir(os.getcwd())
                dir_name = os.getcwd()
                for item in dir_path:
                    if (item.endswith(".AppImage")) and ("YuzuEA-" in item):
                        os.remove(os.path.join(dir_name, item))
                downloadFile(file["name"], file["url"], bearer)
         getver(filename)
      else:
          sys.exit()

def getBearer(username, token):
   try:
      response = requests.post(
         'https://api.yuzu-emu.org/jwt/installer/',
         headers={'User-Agent': 'liftinstall (j-selby)', 'X-USERNAME': username, 'X-TOKEN': token})

      response.raise_for_status()

   except Exception as err:
      if not os.path.exists("version.txt"):
         open("tok.txt", 'w').close()
      with open('tok.txt', 'a') as fd:
          fd.write("{" + username + ":" + token + "}\n")
          sys.exit()
   else:
      if response.status_code == 200:
         getFiles(response.text)
      elif ((response.status_code == 401) or (response.status_code == 400)):
         sys.exit()
      else:
         sys.exit()

def decode(inputtoken):
   token_and_user = inputtoken.split(":")
   getBearer(token_and_user[0], token_and_user[1])

def getver(name):
    if os.path.exists("contents"):
        shutil.rmtree("contents")
    os.mkdir("contents")
    Archive(name).extractall("contents")
    with open('contents/yuzu-windows-msvc-early-access/yuzu.exe', 'rb') as docfile:
	    s = docfile.read()
    publicver = re.search(b'0.{3}[0-9]{4}.{8}yuzu Early Access',s)
    publicver=re.search('[0-9]{6}',str(publicver.group(0)))
    publicver=re.search('[0-9]{4}$',str(publicver.group(0)))
    file2 = open('version.txt', 'w+')
    file2.write(name)
    file2.close()
    shutil.rmtree("contents")
    vfile = open('version.txt')
    zipname=str(vfile.read())
    os.rename(zipname,'YuzuEA-' + publicver.group(0) + '.zip')
    os.rename('yuzu-early-access' + re.search('-[0-9].*',zipname).group(0).split('.')[0] + '.AppImage', 'YuzuEA-' + publicver.group(0) + '.AppImage')
    print(('YuzuEA-' + publicver.group(0) + '.zip'))
        
def checkver():
   
   if not os.path.exists("version.txt"):
    open("version.txt", 'w').close()
   vfile = open('version.txt')
   zipname=str(vfile.read())
   response = requests.get(
            'https://api.yuzu-emu.org/downloads/earlyaccess/',
            headers={'User-Agent': 'liftinstall (j-selby)'})
   jsonresponse = json.loads(response.text)         
   files = jsonresponse["files"]
   for file in files:
       if (".zip" in file["name"]):
           if (file["name"]==zipname):
                sys.exit()
        
def main():
   checkver()
   tokenList = ["berkzonked10:REDACTED", "workscurse28:REDACTED", "lombat69284:REDACTED", "pavamiv281:REDACTED", "pekar88688:REDACTED", "Bash1789:REDACTED", "Negligee1993:REDACTED", "Gullible4399:REDACTED", "Tipper5779:REDACTED", "Glider3585:REDACTED", "Gecko9143:REDACTED", "Goofball0001:REDACTED", "Harmonize0076:REDACTED", "Heavily6528:REDACTED"]
   decode(random.choice(tokenList))

if __name__ == '__main__':
    main()
