```
https://www.blackhillsinfosec.com/genymotion-proxying-android-app-traffic-through-burp-suite/
https://frida.re/docs/android/
https://www.youtube.com/watch?v=xp8ufidc514
https://www.golinuxcloud.com/how-to-bypass-csrf-protection/
```

genymotion emulator : 127.0.0.1:6555
<br>
burpsuite proxy listener : 127.0.0.1:8082  

```bash
# get burp cert
curl localhost:8082/cert -o cert.der # download cert
openssl x509 -inform DER -in cert.der -out cert.pem # convert to pem format
openssl x509 -inform PEM -subject_hash_old -in cert.pem | head -1 # get hash of file
mv cert.pem 9a5ba575.0 # rename to hash

# push to phone
adb shell && su && mount -o remount,rw / # remount because /system is read-only
adb push 9a5ba575.0 /system/etc/security/cacerts/ # push cert to the certificates folder

# handle phone proxy
adb shell settings put global http_proxy localhost:3333
adb reverse tcp:3333 tcp:8082
```

<img src="https://github.com/NikDzub/brptk/assets/87159434/51f6c8e9-7a52-4095-9071-e7dbecb12f9e" width=100%>
<img src="https://github.com/NikDzub/brptk/assets/87159434/22bc5f62-f4c8-47ce-bd0a-745600437bdc" width=100%>

```bash
# get frida server https://frida.re/docs/android/
adb shell && uname -a # find out which release (Aarch64 or ARM64 in my case)
# https://github.com/frida/frida/releases/download/16.2.1/frida-server-16.2.1-android-arm64.xz
adb push frida-server /data/local/tmp/
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &" # start the server
```

```bash
frida-ps -U # get process list to make sure works

 PID  Name
----  ------------------------------------------------------
2924  Google Play Store                                     
3874  HMA VPN                                               
3088  Phone                                                 
6497  TikTok                                                
1598  adbd                                                  
2269  android.ext.services                                  
1225  android.hardware.atrace@1.0-service                   
1456  android.hardware.audio.service
```


```bash
# download ssl pin script
# https://github.com/Eltion/Tiktok-SSL-Pinning-Bypass/blob/main/tiktok-ssl-pinning-bypass.js
frida -U -l tiktok-ssl-pinning-bypass.js -f com.zhiliaoapp.musically
```
<img src="https://github.com/NikDzub/brptk/assets/87159434/2ac275b8-d968-48df-982b-adcf8a246652" width=100%>
