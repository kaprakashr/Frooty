#!/bin/bash

#Installing python2.7.3 version
mkdir -p ~/local
wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
tar xvzf Python-2.7.3.tgz
cd Python-2.7.3
./configure
make
make altinstall prefix=~/local 
ln -s ~/local/bin/python2.7 ~/local/bin/python
cd ..

#Install pip for package management
wget http://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9
tar xvzf pip-9.0.1.tar.gz
cd pip-9.0.1
~/local/bin/python setup.py install

#Install scapy
~/local/bin/pip install scapy

#Check python module version info
~/local/bin/pip freeze 
