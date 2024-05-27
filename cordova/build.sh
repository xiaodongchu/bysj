cd /
rm /output/*.apk

rm -rf /myApp/www/
cp -r /dist/ /myApp/www/
cp /icon.png /myApp/res/icon.png
cd /myApp
cordova build android
cp /myApp/platforms/android/app/build/outputs/apk/debug/app-debug.apk /output/1.apk

rm -rf /myAdmin/www/
cp -r /dist/ /myAdmin/www/
cp /icon.png /myAdmin/res/icon.png
cd /myAdmin
cordova build android
cp /myAdmin/platforms/android/app/build/outputs/apk/debug/app-debug.apk /output/Admin.apk

rm -rf /myNurse/www/
cp -r /dist/ /myNurse/www/
cp /icon.png /myNurse/res/icon.png
cd /myNurse
cordova build android
cp /myNurse/platforms/android/app/build/outputs/apk/debug/app-debug.apk /output/Nurse.apk

rm -rf /myDoctor/www/
cp -r /dist/ /myDoctor/www/
cp /icon.png /myDoctor/res/icon.png
cd /myDoctor
cordova build android
cp /myDoctor/platforms/android/app/build/outputs/apk/debug/app-debug.apk /output/Doctor.apk
