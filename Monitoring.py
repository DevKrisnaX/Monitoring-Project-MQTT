from tkinter import *
import random
import queue
import threading
import time
import json
import datetime
import sqlite3
from paho.mqtt import client as mqtt_client

broker 		= '0.tcp.ap.ngrok.io'
port 		= 13761
topic 		= "IOT"
client_id 	= f'python-mqtt-{random.randint(0, 100)}'

from paho.mqtt import client as mqtt_client

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

import json
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        _data = json.loads(msg.payload.decode())
        temp = str(_data[temp][hum][kipas][spray])


    client.subscribe(topic)
    client.on_message = on_message


window = Tk()
window.title("MQTT Dashboard")
window.geometry('700x1000') # Width, Height
window.resizable(False,False) # Width, Height
window.configure(bg="white")

# Banner image
canvas = Canvas(window, width=700,height=200)
canvas.place(x=0,y=0)
img = PhotoImage(file="banner.png")
canvas.create_image(0,0,anchor=NW,image=img)

# Display "Suhu" image
canvas2 = Canvas(window,width=350,height=400)
canvas2.place(x=0,y=201)
img2 = PhotoImage(file="suhu.png")
canvas2.create_image(0,0,anchor=NW,image=img2)

# Label Temperature
temp_label = Label(window,
                 text="",
                 bg="white",
                 fg="black",
                 font=("Horta", 55))

# Display "Hum" image
canvas3 = Canvas(window,width=350,height=400)
canvas3.place(x=351,y=201)
img3 = PhotoImage(file="hum.png")
canvas3.create_image(0,0,anchor=NW,image=img3)

# Label Humadity
moist_label = Label(window,
                 text="",
                 bg="white",
                 fg="black",
                 font=("Horta", 55))

# Label °C dan %
tempC_label = Label(window, text=" °C", bg="white", fg="black", font=("Helvetica", 40))
tempC_label.place(x=200,y=400)
moistP_label = Label(window, text=" %", bg="white", fg="black", font=("Helvetica", 40))
moistP_label.place(x=580,y=400)

# Kipas
canvas = Canvas(window, width=350,height=100)
canvas.place(x=0,y=601)
img4 = PhotoImage(file="Kipas.png")
canvas.create_image(0,0,anchor=NW,image=img4)

# Label kipas
Kipas_label = Label(window,
                 text="",
                 bg="white",
                 fg="black",
                 font=("Horta", 20))

# Spray
canvas = Canvas(window, width=350,height=100)
canvas.place(x=351,y=601)
img5 = PhotoImage(file="Spray.png")
canvas.create_image(0,0,anchor=NW,image=img5)

# Label Spray
Spray_label = Label(window,
                 text="",
                 bg="white",
                 fg="black",
                 font=("Horta", 20))


current_time = datetime.datetime.now()

con = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = con.cursor()

buat_tabel = '''CREATE TABLE IF NOT EXISTS JamurTemp(
                        time TEXT NOT NULL,
                        temp TEXT NOT NULL,
                        moisture TEXT NOT NULL);'''
try:
    cur.execute(buat_tabel)
    con.commit()
    print("Table created successfully")
except Exception as e:
    print("Error creating table:", e)
    con.rollback()

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global temp_label
        global moist_label
        global Kipas_label
        global Spray_label

        try:
            _data = json.loads(msg.payload.decode())
            temp = str(_data["temp"])
            temp_label.place(x=150,y=430, anchor=CENTER)
            temp_label.config(text=temp)

            moist = str(_data["moisture"])
            moist_label.place(x=540,y=430, anchor=CENTER)
            moist_label.config(text=moist)
            
            kipas = str(_data["kipas"])
            Kipas_label.place(x=230,y=650, anchor=CENTER)
            Kipas_label.config(text=kipas)

            spray = str(_data["spray"])
            Spray_label.place(x=470,y=650, anchor=CENTER)
            Spray_label.config(text=spray)

            

            data_sensor_val = (temp, moist)
            cur.execute(
                "INSERT INTO JamurTemp ('time',temp,moisture) VALUES ('{}',?,?);".format(current_time), data_sensor_val)
            con.commit()
            
        except Exception as e:
            print("Data berhasil dimuat !")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    time.sleep(1)  # add delay here
    window.mainloop()
    client.loop_stop()

if __name__ == '__main__':
    run()
