ds_id = "28-00ff98430ed2"

tfile=open("/sys/bus/w1/devices/{}/w1_slave".format(ds_id))
ttext=tfile.read()
tfile.close()
temp=ttext.split("\n")[1].split(" ")[9]
temperature=float(temp[2:])/1000
print("Temperature:", temperature)
