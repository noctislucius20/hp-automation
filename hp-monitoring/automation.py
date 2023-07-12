import psycopg2
import time
import telebot
import os
import ping3
import paramiko
import pytz
from datetime import datetime
from dotenv import load_dotenv


class Regulation:
    connection = psycopg2.connect(user="postgres",
                                password="scipio",
                                host="10.33.102.212",
                                port=54321,
                                database="hp_automation")
    
    cursor = connection.cursor()
    print('Connected to PostgreSQL')

    timezone = pytz.timezone('Asia/Jakarta')

    def check_ping():
        try:
            Regulation.cursor.execute("SELECT ip_address, ip_gateway FROM sensors")
            row = Regulation.cursor.fetchall()

            honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']
            get_id_honeypot_sensor = []
            array_query = []

            for ip in row:
                ip_address = ip[0]
                ip_gateway = ip[1]
                response_address_time = ping3.ping(ip_address, timeout=5)
                response_gateway_time = ping3.ping(ip_gateway, timeout=5)

                #kalau Gateway sukses/gak sukses, IP Address mati berarti sensor/internet mati.
                if response_address_time is None and response_gateway_time is None or response_gateway_time is not None and response_gateway_time is None:
                    print(f"Ping to IP Address {ip_address} timed out.")
                    message = f"[Alerting Raspberry Pi Status] \n\nSensor : {ip_address} \nCode : 500 \nConnection Status : Not Connected \nDescription : Lost Connection to Device \nTimestamp : {datetime.now(Regulation.timezone)} \n\nMessage : Tidak berhasil melakukan update pada perangkat dengan alamat IP {ip_address}. \nCek pada perangkat : \n1. Perangkat aktif atau tidak aktif. \n2. Konfigurasi jaringan pada perangkat atau router."
                    
                    Bot.notifications(message, "Raspberry Pi Status Alert")

                else:
                    print(f"Ping to IP Address {ip_address} and IP Gateway {ip_gateway} successful.")
                    Automation.automation(ip_address)
                    
        except (Exception) as error:
            print(error)


class Automation(Regulation):
    def automation(ip_address):
        # print(ip_address)
        Regulation.cursor.execute("SELECT COUNT(*) FROM history")
        result = Regulation.cursor.fetchone()

        if result[0] > 0:
            honeypot = ['dionaea', 'honeytrap', 'gridpot', 'cowrie', 'elasticpot', 'rdpy']

            for hp in honeypot:
                query = f"SELECT h.honeypot_status FROM history h JOIN honeypot_sensor hs ON h.honeypot_sensor_id = hs.id JOIN honeypots hp ON hs.honeypot_id = hp.id JOIN sensors s ON hs.sensor_id = s.id WHERE hp.name = '{hp}' AND s.ip_address = '{ip_address}' ORDER BY h.created_at DESC LIMIT 1;"
                Regulation.cursor.execute(query)
                row = Regulation.cursor.fetchall()

                if row:
                    status = row[0][0]
                    if status == f'{hp.capitalize()} is Not Running':
                        #cek honeypot apakah sudah ter-deploy
                        Regulation.cursor.execute(f"SELECT * FROM honeypot_sensor hs JOIN honeypots h ON hs.honeypot_id = h.id JOIN sensors s ON hs.sensor_id = s.id WHERE h.name = '{hp}' AND s.ip_address = '{ip_address}'")
                        row_deploy = Regulation.cursor.fetchall()

                        # SSH ke sensor
                        if row_deploy:
                            print(f"Honeypot {hp} deployed on IP Address {ip_address}")

                            client = paramiko.SSHClient()
                            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                            hostname = ip_address
                            port = 22888
                            username = 'ansigent'
                            private_key_path = '/home/audrey-server/ssh_key'
                            private_key = paramiko.Ed25519Key.from_private_key_file(private_key_path)

                            client.connect(hostname, port=port, username=username, pkey=private_key)
                            command = ''

                            if hp == 'dionaea':
                                command = 'sudo -S docker run --rm -it -p 21:21 -p 42:42 -p 69:69/udp -p 80:80 -p 135:135 -p 443:443 -p 445:445 -p 1433:1433 -p 1723:1723 -p 1883:1883 -p 1900:1900/udp -p 3306:3306 -p 5060:5060 -p 5060:5060/udp -p 5061:5061 -p 11211:11211 -v dionaea:/opt/dionaea -d isif/dionaea:dionaea_hp'

                            if hp == 'honeytrap':
                                command = 'sudo -S docker run -it -p 2222:2222 -p 8545:8545 -p 5900:5900 -p 25:25 -p 5037:5037 -p 631:631 -p 389:389 -p 6379:6379 -v honeytrap:/home -d honeytrap_test:latest'

                            if hp == 'gridpot':
                                command = "sudo -S docker run -it -p 102:102 -p 8000:80 -p 161:161 -p 502:502 -d -v gridpot:/gridpot isif/gridpot:gridpot_hp /bin/bash -c 'cd gridpot; gridlabd -D run_realtime=1 --server ./gridpot/gridlabd/3.1/models/IEEE_13_Node_With_Houses.glm; conpot -t gridpot'"

                            if hp == 'cowrie':
                                command = 'sudo -S docker run -p 22:2222/tcp -p 23:2223/tcp -v cowrie-etc:/cowrie/cowrie-git/etc -v cowrie-var:/cowrie/cowrie-git/var -d --cap-drop=ALL --read-only isif/cowrie:cowrie_hp'

                            if hp == 'elasticpot':
                                command = "sudo -S docker run -it -p 9200:9200/tcp -v elasticpot:/elasticpot/log -d isif/elasticpot:elasticpot_hp /bin/sh -c 'cd elasticpot; python3 elasticpot.py'"

                            if hp == 'rdpy':
                                command = "sudo -S docker run -it -p 3389:3389 -v rdpy:/var/log -d isif/rdpy:rdpy_hp /bin/sh -c 'python /rdpy/bin/rdpy-rdphoneypot.py -l 3389 /rdpy/bin/1 >> /var/log/rdpy.log'"

                            stdin, stdout, stderr = client.exec_command(command)
                            # stdin.write(sudo_password + '\n')
                            stdin.flush()

                            stdout_output = stdout.read().decode().strip()
                            stderr_output = stderr.read().decode().strip()

                            # Check if there is any output
                            if stdout_output:
                                print(f"Standard Output: {stdout_output}")
                                print(f"{hp} is successfully running now on sensor {ip_address}")

                            if stderr_output:
                                print(f"Standard Error: {stderr_output}")
                                print(f"{hp} is failed running on sensor {ip_address}")

                            client.close()

                        else:
                            print(f"Honeypot {hp} not deployed on IP Address {ip_address}")


class Bot(Regulation):
    def notifications(message, alerting):
        try:
            API_KEY = os.getenv('API_KEY')
            bot = telebot.TeleBot("6289233331:AAG_l-CfrztpTtYs_9o6ZtKo2adniEi8_Ig")
            chat_id = -963526950

            bot.send_message(chat_id=chat_id, text=message)
            print(f"Message sent to Bot Telegram {alerting} at {datetime.now(Regulation.timezone)}")

        except (Exception) as error:
            print(error)


class Main(Bot):
    def run():
        Regulation.check_ping()

if __name__ == '__main__':
    Main.run()
