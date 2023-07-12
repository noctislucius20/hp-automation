#!/bin/bash

run_script() {
    /bin/python3 /home/audrey-server/automation.py >> logs_automation.txt
}

> "logs_automation.txt"

while true; do
    run_script

    sleep 60
done