#!/bin/bash

run_script() {
    /bin/python3 /home/raspi/monitoring_raspi_oop.py >> logs_monitoring_raspi.txt
    /bin/python3 /home/raspi/monitoring_honeypot_oop.py >> logs_monitoring_honeypot.txt
}

> "logs_monitoring_raspi.txt"
> "logs_monitoring_honeypot.txt"

while true; do
    run_script
    sleep 1
done