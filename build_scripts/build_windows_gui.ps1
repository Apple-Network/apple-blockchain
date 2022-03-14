# $env:path should contain a path to editbin.exe and signtool.exe

$ErrorActionPreference = "Stop"
Write-Output "   ---"
Write-Output "Get APPLE_INSTALLER_VERSION"
# The environment variable APPLE_INSTALLER_VERSION needs to be defined
$env:APPLE_INSTALLER_VERSION = python .\build_scripts\installer-version.py -win

if (-not (Test-Path env:APPLE_INSTALLER_VERSION)) {
  $env:APPLE_INSTALLER_VERSION = '0.0.0'
  Write-Output "WARNING: No environment variable APPLE_INSTALLER_VERSION set. Using 0.0.0"
}
Set-Location -Path ".\build_scripts" -PassThru
Write-Output "Apple Version is: $env:APPLE_INSTALLER_VERSION"
Write-Output "   ---"
Write-Output "Setup npm packager"
Write-Output "   ---"
Set-Location -Path ".\npm_windows" -PassThru
#npm ci
$Env:Path = $(npm bin) + ";" + $Env:Path
Set-Location -Path "..\" -PassThru

Set-Location -Path "..\apple-blockchain-gui" -PassThru
Write-Output "Prepare Electron packager"
Write-Output "   ---"
$Env:NODE_OPTIONS = "--max-old-space-size=3000"
#lerna clean -y
#npm ci
Write-Output "   ---"
Write-Output "Electron package Windows Installer"
Write-Output "   ---"
npm run build
If ($LastExitCode -gt 0){
    Throw "npm run build failed!"
}

# Change to the GUI directory
Set-Location -Path "packages\gui" -PassThru

Write-Output "   ---"
Write-Output "Increase the stack for apple command for (apple plots create) chiapos limitations"
# editbin.exe needs to be in the path
editbin.exe /STACK:8000000 daemon\apple.exe
Write-Output "   ---"

$packageVersion = "$env:APPLE_INSTALLER_VERSION"
$packageName = "Apple-$packageVersion"

Write-Output "packageName is $packageName"

#Write-Output "   ---"
#Write-Output "fix version in package.json"
#choco install jq
#cp package.json package.json.orig
#jq --arg VER "$env:APPLE_INSTALLER_VERSION" '.version=$VER' package.json > temp.json
#rm package.json
#mv temp.json package.json
#Write-Output "   ---"

Write-Output "   ---"
Write-Output "electron-packager"
electron-packager . Apple --asar.unpack="**\daemon\**" --overwrite --icon=.\src\assets\img\apple.ico --app-version=$packageVersion
Write-Output "   ---"

Write-Output "   ---"
Write-Output "node winstaller.js"
node winstaller.js
Write-Output "   ---"

git status

If ($env:HAS_SECRET) {
   Write-Output "   ---"
   Write-Output "Add timestamp and verify signature"
   Write-Output "   ---"
   signtool.exe timestamp /v /t http://timestamp.comodoca.com/ .\release-builds\windows-installer\AppleSetup-$packageVersion.exe
   signtool.exe verify /v /pa .\release-builds\windows-installer\AppleSetup-$packageVersion.exe
   }   Else    {
   Write-Output "Skipping timestamp and verify signatures - no authorization to install certificates"
}

git status

Write-Output "   ---"
Write-Output "Moving final installers to expected location"
Write-Output "   ---"
Copy-Item ".\Apple-win32-x64" -Destination "$env:GITHUB_WORKSPACE\apple-blockchain-gui\" -Recurse
Copy-Item ".\release-builds" -Destination "$env:GITHUB_WORKSPACE\apple-blockchain-gui\" -Recurse

Write-Output "   ---"
Write-Output "Windows Installer complete"
Write-Output "   ---"
