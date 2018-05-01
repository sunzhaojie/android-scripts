#!/bin/bash

ipRe="((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))"

sifconfig=`ifconfig`

echo ${sifconfig} |grep -o -E "en0.*inet $ipRe "|awk -F'inet ' '{print $2}'
