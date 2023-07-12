#!/bin/bash


run_script() {
    /bin/python3 /home/ansiadmin/collector.py >> logs_collector.txt
}

> "logs_collector.txt"

while true; do
    run_script

    sleep 5
done