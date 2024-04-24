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
# handle cert
curl localhost:8082/cert -o cert.der # download cert
openssl x509 -inform DER -in cert.der -out cert.pem # convert to pem format
openssl x509 -inform PEM -subject_hash_old -in cert.pem | head -1 # get hash of file
mv cert.pem 9a5ba575.0 # rename to hash
```

```bash
# push to phone
adb shell && su && mount -o remount,rw / # remount because /system is read-only
adb push 9a5ba575.0 /system/etc/security/cacerts/ # push cert to the certificates folder
```

