#!/bin/sh

releaseVersion=$1
releasePackageName="apache-yunikorn-${releaseVersion}-incubating"
currentDir=$(pwd)
workDir=$(dirname "$currentDir")
rm -rf ${workDir}/staging
mkdir -p ${workDir}/staging/${releasePackageName}
cd ${workDir}/staging/${releasePackageName}

git clone "https://github.com/apache/incubator-yunikorn-core.git"
git clone "https://github.com/apache/incubator-yunikorn-k8shim.git"
git clone "https://github.com/apache/incubator-yunikorn-scheduler-interface.git"
git clone "https://github.com/apache/incubator-yunikorn-web.git"

mv incubator-yunikorn-core core
mv incubator-yunikorn-k8shim k8shim
mv incubator-yunikorn-scheduler-interface scheduler-interface
mv incubator-yunikorn-web web

mv ${workDir}/release-top-level-artifacts/*  ${workDir}/staging/${releasePackageName}
