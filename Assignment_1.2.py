import tkinter as tkr
import time
import random

canvas_size=600
ball_diameter=30
ball_radius=ball_diameter/2
dist_threshold=1

tk=tkr.Tk()
tk.title("Assignment 1.2 - IRM2017008")
canvas=tkr.Canvas(tk,width=canvas_size,height=canvas_size)
canvas.grid()

final_x=random.randint(0,canvas_size-ball_diameter)
final_y=random.randint(0,canvas_size-ball_diameter)

initial_points=[]
for i in range(14):
    init_x=random.randint(0,canvas_size-ball_diameter)
    init_y=random.randint(0,canvas_size-ball_diameter)
    if(init_x==final_x):
        i-=1
        continue
    initial_points.append([init_x,init_y])

#print(initial_points)

#ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="yellow")
balls=[]
slopes=[]
velocity=[]
paths=[]
signs=[]
for i in range(14):
    init_x=initial_points[i][0]
    init_y=initial_points[i][1]
    
    ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="yellow")
    balls.append(ball)
    
    slope=(final_y-init_y)/(final_x-init_x)
    slopes.append(slope)
    if init_x<final_x:
        x=1
    else:
        x=-1
    y=slope*x
    velocity.append([x,y])
    
    x_sign=1
    y_sign=1
    if init_x>final_x:
        x_sign=-1
    if init_y>final_y:
        y_sign=-1
    signs.append([x_sign,y_sign])
    
    pi_x=init_x+ball_radius
    pi_y=init_y+ball_radius
    pf_x=final_x+ball_radius
    pf_y=final_y+ball_radius
    path=canvas.create_line(pi_x,pi_y,pf_x,pf_y);
    paths.append(path)
    

"""
initial_ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="light blue")
"""
final_ball=canvas.create_oval(final_x,final_y,final_x+ball_diameter,final_y+ball_diameter,fill="light blue")


counter=0
reached=[]
while True:
    for i in range(14):
        if(i in reached):
            continue
        ball=balls[i]
        x=velocity[i][0]
        y=velocity[i][1]
        canvas.move(ball,x,y)
        pos=canvas.coords(ball)
        
        '''
        #Stopping Condition 1 for Ball
        dist1=abs(pos[1]-final_y)
        dist2=abs(pos[0]-final_x)
        if(dist1<dist_threshold and dist2<dist_threshold):
            print(i," reached Destination !")
            reached.append(i)
            counter+=1
        '''  
            
        ''' 
        #Stopping Condition 2 for Ball
        cur_x_sign=1
        cur_y_sign=1
        x_sign=signs[i][0]
        y_sign=signs[i][1]
        if(pos[0]>final_x):
            cur_x_sign=-1
        if(pos[1]>final_y):
            cur_y_sign=-1
        if(x_sign!=cur_x_sign or y_sign!=cur_y_sign):
            print(i," reached Destination !")
            reached.append(i)
            counter+=1
        '''
        
        final_ball_pos=canvas.coords(final_ball)
        if(pos[0]==final_ball_pos[0] or pos[1]==final_ball_pos[1] or pos[2]==final_ball_pos[2] or pos[3]==final_ball_pos[3]):
            print(i," reached Destination !")
            reached.append(i)
            counter+=1
            
            
    if(counter>=14):
        print("HERE")
        break
    tk.update()
    time.sleep(0.001)
    pass

tk.mainloop()