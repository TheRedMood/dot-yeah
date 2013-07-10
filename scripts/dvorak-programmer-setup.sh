#!/bin/bash
wget http://www.kaufmann.no/downloads/linux/kbddvp-1_2_1-src-linux.tgz
DVP_DIR=$(mktemp -t -d kbddvp.XXXXXX)
cat kbddvp-1_2_1-src-linux.tgz | gzip -d | tar xf - -C $DVP_DIR
pushd $DVP_DIR/kbddvp-1.2

chmod +x *.sh
./home.install.sh

popd
rm -fr $DVP_DIR
rm -fr kbddvp-1_2_1-src-linux.tgz
