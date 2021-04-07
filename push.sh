#!/bin/sh
currentscript="$0"
function finish {
    echo "Securely deleting ${currentscript}"; shred -u ${currentscript};
}

GIT='git --git-dir='$PWD'/.git'

$GIT init
$GIT checkout -b main
$GIT add .
$GIT commit -m "push boilerplate to main"
$GIT remote add origin git@github.com:licenseware/authenticator.git
$GIT push origin --force main


trap finish EXIT

