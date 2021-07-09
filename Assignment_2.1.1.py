import tkinter as tkr
import time
import random

canvas_size=600
init_x=100
init_y=100
final_x=500
final_y=500
obstacle_x=250
obstacle_y=250
robot_radius=10
KATT=2
KREP=100000
D_REP=2*robot_radius
V_MAX=2
D_ATT=5*robot_radius

tk=tkr.Tk()
tk.title("Assignment 2.1.1 - IRM2017008")
canvas=tkr.Canvas(tk,width=canvas_size,height=canvas_size)
canvas.grid()

ball=canvas.create_oval(init_x-robot_radius,init_y-robot_radius,init_x+robot_radius,init_y+robot_radius,fill="yellow")
final_ball=canvas.create_oval(final_x-robot_radius,final_y-robot_radius,final_x+robot_radius,final_y+robot_radius,fill="light blue")
obstacle_ball=canvas.create_oval(obstacle_x-robot_radius,obstacle_y-robot_radius,obstacle_x+robot_radius,obstacle_y+robot_radius,fill="red")
path=canvas.create_line(init_x,init_y,final_x,final_y)

visited_point={}

while True:
    cur_pos=canvas.coords(ball)
    cur_x=int(cur_pos[0]+robot_radius)
    cur_y=int(cur_pos[1]+robot_radius)
    
    cord=(cur_x,cur_y)
    if(cord in visited_point):
        visited_point[cord]=visited_point[cord]+1
    else:
        visited_point[cord]=1
    
    d_from_goal=pow(pow(cur_x-final_x,2)+pow(cur_y-final_y,2),0.5)
    if(d_from_goal<=D_ATT):
        F_Att_x=-KATT*(cur_x-final_x)
        F_Att_y=-KATT*(cur_y-final_y)
    else:
        F_Att_x=(-KATT*D_ATT*(cur_x-final_x))/d_from_goal
        F_Att_y=(-KATT*D_ATT*(cur_y-final_y))/d_from_goal
    
    d_from_rep=pow(pow(cur_x-obstacle_x,2)+pow(cur_y-obstacle_y,2),0.5)-2*robot_radius
    if(d_from_rep<=D_REP):
        dist_mul=(1/d_from_rep)-(1/D_REP)
        F_Rep_x=(KREP*dist_mul*(cur_x-obstacle_x))/pow(d_from_rep,3)
        F_Rep_y=(KREP*dist_mul*(cur_y-obstacle_y))/pow(d_from_rep,3)
    else:
        F_Rep_x=0
        F_Rep_y=0
    
    F_Res_x=F_Att_x+F_Rep_x
    F_Res_y=F_Att_y+F_Rep_y
    
    F_Mag=pow(pow(F_Res_x,2)+pow(F_Res_y,2),0.5)
    
    if(F_Mag!=0):
        x=V_MAX*(F_Res_x/F_Mag)
        y=V_MAX*(F_Res_y/F_Mag)
    else:
        #PERBUTATION
        print("Zero Force")
        break
    
    if(visited_point[cord]>25):
        rand_x=random.random()
        rand_y=random.random()
        magnitude=pow(pow(rand_x,2)+pow(rand_y,2),0.5)
        rand_x=rand_x/magnitude
        rand_y=rand_y/magnitude
        x=rand_x*V_MAX
        y=rand_y*V_MAX
    
    canvas.move(ball,x,y)
    pos=canvas.coords(ball)
    x_pos=pos[0]+robot_radius
    y_pos=pos[1]+robot_radius
    if(x_pos==final_x and y_pos==final_y):
        break
    tk.update()
    time.sleep(0.001)
    pass

tk.mainloop()