#!/bin/bash


run_script() {
    /bin/python3 /home/ansiadmin/collector-raspi.py >> logs_collector_raspi.txt
}

> "logs_collector_raspi.txt"

while true; do
    run_script

    sleep 3600
done