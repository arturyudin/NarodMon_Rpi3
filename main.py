import socket
import logging
import subprocess

logger = logging.getLogger("NarodMon")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("NarodMon.log")
formatter = logging.Formatter('[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info("logger inited and libraries are connected!")

#paramets
mac_addr = "db:f1:97:38:c2:f5"
ds_id = "28-00ff98430ed2"

# def exec_cmd(cmd):
#     try:
#         cmd1 = cmd.split('___')
#         a = subprocess.run(cmd1)
#         logger.info(str("execution", cmd," result:", a))
#     except Exception as e:
#         logger.error(str("in exec_cmd:", e))
# def analyze_answer(answ):
#     if answ.startswith('#'):
#         logger.info("NarodMon send command:"+answ)
#         try:
#             # if answ.startswith('#cmd'):
#             #     answs = answ.split('___')
#             #     logger.info("Executing command:"+answs[1])
#             #     exec_cmd(answs[1])
#             answs = answ[1:len(answ)].split(";")
#             for i in answs:
#                 if i.startswith('cmd'):
#                     cmd = i.split('=')
#                     logger.info("Executing command:"+cmd[1])
#                     exec_cmd(cmd[1])     
                           
#         except Exception as e:
#             logger.error(str("in analyze_answer:", e))
def get_temp():
    try:
        tfile=open("/sys/bus/w1/devices/{}/w1_slave".format(ds_id))
        logger.info("opened sensor file for reading")
        ttext=tfile.read()
        logger.info("file read")
        tfile.close()
        logger.info("file closed")
        temp=ttext.split("\n")[1].split(" ")[9]
        temperature=float(temp[2:])/1000
        logger.info("returing temperature:"+str(temperature))
        return temperature
    except Exception as e:
        logger.error(e)

sensor1 = "#T1#{}#DS18B20".format(get_temp())
logger.info("Generated sensor1 string for sending:"+sensor1)

try:  
    sock = socket.socket()
    logger.info("socket inited")
    sock.connect(('narodmon.ru', 8283))
    logger.info("socket connected")
    str_send = "#{}\n{}\n##".format(mac_addr, sensor1)
    logger.info("Generated string with sensor(s) for sending:"+str_send)
    sock.send(str_send.encode())
    logger.info("socket sent")
    answ = sock.recv(1024)
    print(answ)
    logger.info("socket answer:"+(answ.decode()))
    sock.close()
    # analyze_answer(str(answ.decode()))
    logger.info("socket close")
except socket.error as e:
    logger.error(e)