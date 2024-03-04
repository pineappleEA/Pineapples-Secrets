# How Pineapple Actually Worked  
Contrary to popular belief, we never actually worked for yuzu.  
We did send in a push request once years ago, but that was stolen from us, with no credit.  
We've decided to do a little write-up of how we actually got the files.  
We only actually paid for their patreon for a few weeks.  
  
## Step 1: Getting a Token  
First, we have to get a token. These are easy to get, just make an account on their website.  
You don't even need to connect a Patreon account at all!
We used a bunch of random ones to try hide ourselves a bit, which worked in the long run.  
If you decode the token, you get something in the format of "username:password", with the password being randomly generated (thankfully).  
  
## Step 2: Getting Links  
Send a get request to `https://api.yuzu-emu.org/downloads/earlyaccess/`.  
`curl https://api.yuzu-emu.org/downloads/earlyaccess/`  
This gives us a json file with all of their latest files, as well as download links.  
We couldn't get an example for this step, their APIs were shut down too quickly.  
  
## Step 3: Getting a Bearer Token  
We needed to get a bearer token, which is basically a one-time password to download the file.  
`curl -X POST --user-agent "liftinstall (j-selby)" -H "X-USERNAME: pepepanda" -H "X-TOKEN: [REDACTED]" https://api.yuzu-emu.org/jwt/installer`  
(Yes, this is an account we used)  
In this curl command, we send a POST request to their installer's api.  
We set the useragent to "liftinstall (j-selby)" so that it thinks we are the installer.  
X-USERNAME and X-TOKEN are from step 1, after decoding the token.  
  
This gives you a big base-64 encoded string:  
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2Mzg2NDQwODEuMCwiaWQiOiJjMDVmZmM2My05MzcxLTQ3YzgtOT
lmMy01MTE0M2Y1MzMxZjEiLCJqdGkiOiIxYWJlODQ4Yy00ZWYwLTRlY2UtODk0MS1mYTYyMDdhYmQ0MDgiLCJ1c2VybmFtZSI6I
nBlcGVwYW5kYSIsInN1YiI6InBlcGVwYW5kYSIsImRpc3BsYXlOYW1lIjoicGVwZXBhbmRhIiwiYXZhdGFyVXJsIjoiaHR0cHM6
Ly9hcGkuY2l0cmEtZW11Lm9yZy9wcm9maWxlL3BlcGVwYW5kYS9hdmF0YXIucG5nIiwicm9sZXMiOlsiY29tcGF0aWJpbGl0eSJ
dLCJyZWxlYXNlQ2hhbm5lbHMiOltdLCJpc1BhdHJlb25BY2NvdW50TGlua2VkIjpmYWxzZSwiaXNQYXRyZW9uU3Vic2NyaXB0aW
9uQWN0aXZlIjpmYWxzZSwibmJmIjoxNjM4NjQ0MDc1LCJleHAiOjE2Mzg2NTEyODAsImlzcyI6ImNpdHJhLWNvcmUiLCJhdWQiO
iJpbnN0YWxsZXIifQ.fkbJjzuVfb1_jZjIaDgqOncc_LvU0_Dqytwo9MmsM5WCrOuKgkBLndi3YVfRHhFlMSm6F0Z0c5DeujwQe
4SABDYZZzDB93WSvuD3bV6lB-tr5hrCcOj6hncRgC3RkPY-1oJUaO4XStkeXIH7y2HJJiF71DMwv3ImvJgGxV73FxkT87n2W8H1
BuoW5X9LsWxjnxE27qX24li3UElQOkNDBV87m93DwKjADLH-dS1r7hoarw4Wm2Q_Y_dmWf-Dqwtl6VWJFoZS95qsPSAIXbDpq0W
88q3NnPzAO5GQHBN9ZuNr7e1KPI7A285e16lYLeSdpFRbg0U4Io2FqEYil5OvBw
```  
  
Decoding this gives us something like this:  
```
{"alg":"RS256","typ":"JWT"}{"iat":1638644081.0,"id":"c05ffc63-9371-47c8-99f3-51143f5331f1","jti":"1abe848c-4ef0-4ece-8941-fa6207abd408",  
"username":"pepepanda","sub":"pepepanda","displayName":"pepepanda","avatarUrl":"https://api.citra-emu.org/profile/pepepanda/avatar.png",  
"roles":["compatibility"],"releaseChannels":[],"isPatreonAccountLinked":false,"isPatreonSubscriptionActive":false,"nbf":1638644075,  
"exp":1638651280,"iss":"citra-core","aud":"installer"}  
```  
  
As you can see, this bluntly tells us there isn't a patreon account linked, nor is there a patreon subscription active.  
Liftinstall, which was the emulator's installer and updater, likely just checked this token to see if a Patreon subscription was active.  
  
# Step 4: Actually Downloading the Build  
We grab a download link from Step 2's json file, and the bearer token, which is the still base-64 encoded string from step 3.  
We slap those together in a big http GET request.  
We also make sure that the user agent is still their liftinstall.  
This results in a command along the lines of the following:

```
curl -X GET --user-agent "liftinstall (j-selby)" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5  
cCI6IkpXVCJ9.eyJpYXQiOjE2Mzg2NDAyMTkuMCwiaWQiOiJjMDVmZmM2My05MzcxLTQ3YzgtOTlmMy01MTE0M2Y1MzMxZjEiLC  
JqdGkiOiI1Y2EzNTg4OC0wMGI1LTRiZjAtYThmMy1iOGIxZDg2YzUzNjUiLCJ1c2VybmFtZSI6InBlcGVwYW5kYSIsInN1YiI6I  
nBlcGVwYW5kYSIsImRpc3BsYXlOYW1lIjoicGVwZXBhbmRhIiwiYXZhdGFyVXJsIjoiaHR0cHM6Ly9hcGkuY2l0cmEtZW11Lm9y  
Zy9wcm9maWxlL3BlcGVwYW5kYS9hdmF0YXIucG5nIiwicm9sZXMiOlsiY29tcGF0aWJpbGl0eSJdLCJyZWxlYXNlQ2hhbm5lbHM  
iOltdLCJpc1BhdHJlb25BY2NvdW50TGlua2VkIjpmYWxzZSwiaXNQYXRyZW9uU3Vic2NyaXB0aW9uQWN0aXZlIjpmYWxzZSwibm  
JmIjoxNjM4NjQwMjEzLCJleHAiOjE2Mzg2NDc0MTgsImlzcyI6ImNpdHJhLWNvcmUiLCJhdWQiOiJpbnN0YWxsZXIifQ.UFDGao  
00cvQsaEEuiijMgb0ccf02fXNg2DqSVGhTC9a_nHaRt4MXEYDVn5PCTUSO1f4u1Ubvn_3JlQ6POdhP_vV_b70QEFKf-7MQpmc8L  
Zg5lcKzpeQiJ0PqblR_edzrbmz816pLTVGNFwwhGn4WcmZ68juKmZ7BqudpbxbDqQlbjFq2ZG_65jgyQ_KtLIemLy-WWGDl7Q-Y  
KqCqjA-bPNqT1gXCrlwivyscm_bOwJ4h7YM3_6hWicGBydfWX7UCVZJHYhdjtilXmfebC59pv5caF1CG00vPfhe-6Arrr4-XepO  
zrxopUoNTSvTa97yNDxVE6RtClsMaemtbhgz4HQ"  
https://api.yuzu-emu.org/downloads/earlyaccess/16369/yuzu-windows-msvc-20211204-b9430bace.7z  
-o yuzu-windows-msvc-20211204-b9430bace.7z  
```  
  
This was a real example of a GET request we did, to download a build from their api, without paying for their patreon.  
  
## Footnotes
In step 3, we mentioned that it is likely that the Liftinstall just checked the bearer token for a Patreon subscription.  
This likely would have made it very easy to just circumvent the check.  
The official installer could probably have been "cracked" very easily.  
Since the liftinstaller communicates with the official servers, we decided against that, so we could keep this process secret.  
This meant we could keep using this method for as long as possible, and keep reuploading the builds for everyone to download.  
We originally did this manually, but one of us simply automated the whole process using a Python script, so we had more up-to-date builds.    
Also, by the way, the only reason we made Pineapple was due to Yuzu illegally DMCAing some pastebins of some of our friends.  