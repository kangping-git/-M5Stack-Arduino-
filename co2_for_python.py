import subprocess 
import re
import datetime
import tkinter
import json
from io import StringIO
root = tkinter.Tk()
root.geometry("1000x500")
root.title("debug")
co2_label = tkinter.Label()
co2_label.place(x=10,y=10)
data = ""
a = 100000000000
b = 30
data = []
num = 0
c = "["
def function():
    global num,co2_label,c
    output = str(subprocess.check_output(['sudo', 'python', '-m', 'mh_z19']))
    output2 = str(output).split("b")[1]
    output2 = output2.split("\\n")[0]
    output2 = output2.split("'")[1]
    io = StringIO(output2)
    co2 = str(json.load(io)["co2"])
    data.append(datetime.datetime.now().strftime("計測時刻は%Y-%m-%d %H:%M:%Sです。その時の値は" + str(co2) + "です。残り計測回数は" + str(a-num-1) + "です。\r"))
    co2_label["text"] = ""
    for i in range(20):
        if len(data) - i -1 < 0:
            break
        co2_label["text"] += data[len(data) - i-1]
    if num != 0:
        c += '\n\t{"date":"' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '","co2":' + co2 + '}'
    else:
        c += ',\n\t{"date":"' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '","co2":' + co2 + '}'
    print(num+1)
    num += 1
    if num % 10 == 0:
        f2 = open("./data.json","w")
        f2.write(c)
        f2.close()
    if num != a-1:
        root.after(int(b*1000),function)
    else:
        c += "\n]"
        f2 = open("./data.json","w")
        f2.write(c)
        f2.close()
        root.destroy()
function()
root.mainloop()
