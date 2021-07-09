import tkinter as tkr
import time
import random

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
#final_y=init_y

ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="yellow")

slope=(final_y-init_y)/(final_x-init_x);
if init_x<final_x:
    x=1
else:
    x=-1
y=slope*x


x_sign=1
y_sign=1
if init_x>final_x:
    x_sign=-1
if init_y>final_y:
    y_sign=-1


pi_x=init_x+ball_radius
pi_y=init_y+ball_radius
pf_x=final_x+ball_radius
pf_y=final_y+ball_radius
path=canvas.create_line(pi_x,pi_y,pf_x,pf_y);

"""
initial_ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="light blue")
"""
final_ball=canvas.create_oval(final_x,final_y,final_x+ball_diameter,final_y+ball_diameter,fill="light blue")


counter=0
while True:
    canvas.move(ball,x,y)
    pos=canvas.coords(ball)
    center_y=(pos[1]+pos[3])/2
    center_x=(pos[0]+pos[2])/2
    cur_x_sign=1
    cur_y_sign=1
    if(pos[0]>final_x):
        cur_x_sign=-1
    if(pos[1]>final_y):
        cur_y_sign=-1    
    dist=pow((center_x-final_x),2)+pow((center_y-final_y),2)
    dist=pow(dist,0.5)
    dist=abs(pos[1]-final_y)
    print(center_x," ",center_y," ",final_x," ",final_y," ",pos[1])
    
    '''
    if(dist<dist_threshold):
        print(pos[1],"-",final_y,"-",dist,"-",dist_threshold)
        break
    '''
    
    
    if(x_sign!=cur_x_sign or y_sign!=cur_y_sign):
        break
    
    
    '''
    final_ball_pos=canvas.coords(final_ball)
    if(pos[0]==final_ball_pos[0] or pos[1]==final_ball_pos[1] or pos[2]==final_ball_pos[2] or pos[3]==final_ball_pos[3]):
        break
    '''
        

    tk.update()
    time.sleep(0.001)
    pass

tk.mainloop()