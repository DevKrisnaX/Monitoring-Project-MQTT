# Library yang digunakan
from tkinter import *
import random
import time
import datetime
from paho.mqtt import client as mqtt_client
import json
import sqlite3 

# Setting Server
broker = 'tr3.localto.net'
port = 36733
topic = "Jamur"
client_id = f'python-mqtt-{random.randint(0, 100)}'

# Buat Database, Ubah sesuai kemauan
con = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = con.cursor()

# Buat Tabel pada DB
buat_tabel = '''CREATE TABLE IF NOT EXISTS JamurTemp(
                    time TEXT NOT NULL,
                    rak1_temp TEXT NOT NULL,
                    rak1_hum TEXT NOT NULL
                   
                );'''

# Cek Apakah Tabel Berhasil Dibuat
try:
    cur.execute(buat_tabel)
    con.commit()
    print("Berhasil Membuat Tabel")
except Exception as e:
    print("Gagal Membuat Tabel:", e)
    con.rollback()

# Cek Server Running Atau Tidak
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

# Waktu timestamp
current_time = datetime.datetime.now()

# Ambil Data Dari API ESP
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            _data = json.loads(msg.payload.decode())
            print("Received JSON data:", _data)
            temp1 = str(_data["temp1"])
            moist1 = str(_data["moisture1"])
            kipas1 = str(_data["kipas1"])
            spray1 = str(_data["spray1"])

            temp2 = str(_data["temp2"])
            moist2 = str(_data["moisture2"])
            kipas2 = str(_data["kipas2"])
            spray2 = str(_data["spray2"])

            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            data_sensor_val = (current_time, temp1, moist1)
            cur.execute("INSERT INTO JamurTemp (time,rak1_temp,rak1_hum) VALUES(?, ?, ?)",(data_sensor_val))
            con.commit()

            #RAK1
            temp_label1.place(x=155, y=217, anchor=CENTER)
            temp_label1.config(text=temp1)
            moist_label1.place(x=155, y=327, anchor=CENTER)
            moist_label1.config(text=moist1)
            Kipas_label1.place(x=160, y=447, anchor=CENTER)
            Kipas_label1.config(text=kipas1)
            Spray_label1.place(x=160, y=553, anchor=CENTER)
            Spray_label1.config(text=spray1)
            #RAK2
            temp_label2.place(x=500, y=217, anchor=CENTER)
            temp_label2.config(text=temp2)
            moist_label2.place(x=500, y=327, anchor=CENTER)
            moist_label2.config(text=moist2)
            Kipas_label2.place(x=500, y=447, anchor=CENTER)
            Kipas_label2.config(text=kipas2)
            Spray_label2.place(x=500, y=553, anchor=CENTER)
            Spray_label2.config(text=spray2)

            time.sleep(1)
        except json.decoder.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Raw payload:", msg.payload.decode())
        except Exception as e:
            print("Error processing message:", e)

    client.subscribe(topic)
    client.on_message = on_message

window = Tk()
window.title("MONITORING JAMUR DASHBOARD")
window.geometry('1440x1024')  # Width, Height
window.resizable(False, False)
window.configure(bg="white")

# Banner image
canvas = Canvas(window, width=1440, height=1024)
canvas.place(x=0, y=0)
img = PhotoImage(file="image\Layout.jpg")
canvas.create_image(0, 0, anchor=NW, image=img)

#### RAK 1
# Label °C dan % 1
tempC_label1 = Label(window, text=" °C", bg="white", fg="black", font=("Horta", 20))
tempC_label1.place(x=170,y=200)
moistP_label1 = Label(window, text=" %", bg="white", fg="black", font=("Horta", 20))
moistP_label1.place(x=175,y=310)

temp_label1 = Label(window,text="",bg="white",fg="black",font=("Horta", 20))
moist_label1 = Label(window,text="",bg="white",fg="black",font=("Horta", 20))
Kipas_label1 = Label(window,text="",bg="white",fg="black",font=("Horta", 20))
Spray_label1 = Label(window,text="",bg="white",fg="black",font=("Horta", 20))

#### RAK 2
# Label °C dan % 2
tempC_label2 = Label(window, text=" °C", bg="white", fg="black", font=("Horta", 20))
tempC_label2.place(x=510,y=200)
moistP_label2 = Label(window, text=" %", bg="white", fg="black", font=("Horta", 20))
moistP_label2.place(x=515,y=310)

temp_label2 = Label(window,text="",bg="white",fg="black",font=("Horta", 20))
moist_label2 = Label(window,text="",bg="white",fg="black",font=("Horta", 20))
Kipas_label2 = Label(window,text="",bg="white",fg="black",font=("Horta", 20))
Spray_label2 = Label(window,text="",bg="white",fg="black",font=("Horta", 20))


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    window.mainloop()
    client.loop_stop()

if __name__ == '__main__':
    run()