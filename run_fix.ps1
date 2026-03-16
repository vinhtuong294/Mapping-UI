$env:TEMP="D:\temp"
$env:TMP="D:\temp"
$env:PUB_CACHE="D:\.pub-cache"
if (!(Test-Path D:\temp)) { New-Item -ItemType Directory -Path D:\temp }
if (!(Test-Path D:\.pub-cache)) { New-Item -ItemType Directory -Path D:\.pub-cache }
if (!(Test-Path D:\.chrome-profile)) { New-Item -ItemType Directory -Path D:\.chrome-profile }

Write-Host "Redirecting temporary files to D: to bypass disk space errors on C:..."
flutter run -d chrome --web-browser-flag="--disable-web-security --user-data-dir=D:\.chrome-profile"
