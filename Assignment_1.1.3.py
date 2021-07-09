import tkinter as tkr
import time
import random
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

canvas_size=600
ball_diameter=30
ball_radius=ball_diameter/2
dist_threshold=1

tk=tkr.Tk()
tk.title("Assignment 1.1 - IRM2017008")
canvas=tkr.Canvas(tk,width=canvas_size,height=canvas_size)
canvas.grid()

init_x=random.randint(0,canvas_size-ball_diameter)
init_y=random.randint(0,canvas_size-ball_diameter)

final_x=random.randint(0,canvas_size-ball_diameter)
final_y=random.randint(0,canvas_size-ball_diameter)

'''
final_x=init_x
final_y=init_y+100
'''

ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="yellow")

distance_value=pow(pow(final_x-init_x,2)+pow(final_y-init_y,2),0.5)
print("DISTANCE = ",distance_value)
#speed_inc=100/distance_value
speed_inc=1
alpha=0;
k=1/(distance_value)

pi_x=init_x+ball_radius
pi_y=init_y+ball_radius
pf_x=final_x+ball_radius
pf_y=final_y+ball_radius
path=canvas.create_line(pi_x,pi_y,pf_x,pf_y)

"""
initial_ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="light blue")
"""
final_ball=canvas.create_oval(final_x,final_y,final_x+ball_diameter,final_y+ball_diameter,fill="light blue")

x=-k*(init_x-final_x)
y=-k*(init_y-final_y)
print("Velocity = ",x," ",y)
counter=0
while True:
    canvas.move(ball,x,y)
    alpha=alpha+k;
    if(alpha>=1):
        break;
    tk.update()
    time.sleep(0.001)
    pass

tk.mainloop()

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
print("END")