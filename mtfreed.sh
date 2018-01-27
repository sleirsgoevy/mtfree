#!/bin/bash

export WPA_CLI="wpa_cli"
export MTFREE="xvfb-run python3 mtfree.py"

eval "$WPA_CLI" | while true
do
    read l
    if echo "$l" | grep "SSID=MT_FREE" >/dev/null
    then mt_free_bssid="$(echo "$l" | sed 's/^.*BSSID=//g' | cut -c 1-17)"
    fi
    if echo "$l" | grep "CTRL-EVENT-CONNECTED" >/dev/null
    then
        connected_to_bssid="$(echo "$l" | sed 's/^.*Connection to //g' | cut -c 1-17)"
        if [ "$connected_to_bssid" == "$mt_free_bssid" ]
        then
            eval "$MTFREE"
        fi
    fi
done
