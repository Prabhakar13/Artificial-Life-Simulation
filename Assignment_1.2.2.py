import tkinter as tkr
import time
import random
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

dist_threshold=1

canvas_size=600
robot_radius=10
KATT=2
KREP=10000000
D_REP=2*robot_radius
V_MAX=1
D_ATT=5*robot_radius

tk=tkr.Tk()
tk.title("Assignment 1.2 - IRM2017008")
canvas=tkr.Canvas(tk,width=canvas_size,height=canvas_size)
canvas.grid()

final_x=random.randint(robot_radius,canvas_size-robot_radius)
final_y=random.randint(robot_radius,canvas_size-robot_radius)

initial_points=[]
for i in range(14):
    init_x=random.randint(robot_radius,canvas_size-robot_radius)
    init_y=random.randint(robot_radius,canvas_size-robot_radius)
    initial_points.append([init_x,init_y])

#print(initial_points)

#ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="yellow")
balls=[]
paths=[]
for i in range(14):
    init_x=initial_points[i][0]
    init_y=initial_points[i][1]
    
    ball=canvas.create_oval(init_x-robot_radius,init_y-robot_radius,init_x+robot_radius,init_y+robot_radius,fill="yellow")
    balls.append(ball)
    
    pi_x=init_x
    pi_y=init_y
    pf_x=final_x
    pf_y=final_y
    path=canvas.create_line(pi_x,pi_y,pf_x,pf_y);
    paths.append(path)
    

"""
initial_ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="light blue")
"""
final_ball=canvas.create_oval(final_x-robot_radius,final_y-robot_radius,final_x+robot_radius,final_y+robot_radius,fill="light blue")

visited_point=[]
for i in range(14):
    visited_point.append({})

counter=0
reached=[]
while True:
    for i in range(14):
        if(i in reached):
            continue
        
        
        #HERE
        ball=balls[i]
        cur_pos=canvas.coords(ball)
        cur_x=int(cur_pos[0]+robot_radius)
        cur_y=int(cur_pos[1]+robot_radius)
        
        obstacle_index=-1
        min_dist=1000
        for j in range(14):
            if(j in reached):
                continue
            xxx=int((canvas.coords(balls[j]))[0]+robot_radius)
            yyy=int((canvas.coords(balls[j]))[1]+robot_radius)
            temp_dist=pow(pow(cur_x-xxx,2)+pow(cur_y-yyy,2),0.5)
            if(temp_dist<min_dist):
                obstacle_index=j;
                min_dist=temp_dist
                
        
        
        cord=(cur_x,cur_y)
        if(cord in visited_point[i]):
            visited_point[i][cord]=visited_point[i][cord]+1
        else:
            visited_point[i][cord]=1
        
        d_from_goal=pow(pow(cur_x-final_x,2)+pow(cur_y-final_y,2),0.5)
        if(d_from_goal<=D_ATT):
            F_Att_x=-KATT*(cur_x-final_x)
            F_Att_y=-KATT*(cur_y-final_y)
        else:
            F_Att_x=(-KATT*D_ATT*(cur_x-final_x))/d_from_goal
            F_Att_y=(-KATT*D_ATT*(cur_y-final_y))/d_from_goal
        
        if(obstacle_index!=-1):
            obstacle_x=int((canvas.coords(balls[obstacle_index]))[0]+robot_radius)
            obstacle_y=int((canvas.coords(balls[obstacle_index]))[1]+robot_radius)
            d_from_rep=pow(pow(cur_x-obstacle_x,2)+pow(cur_y-obstacle_y,2),0.5)-2*robot_radius
            if(d_from_rep<=D_REP):
                #print("Repul Force")
                dist_mul=(1/d_from_rep)-(1/D_REP)
                F_Rep_x=(KREP*dist_mul*(cur_x-obstacle_x))/pow(d_from_rep,3)
                F_Rep_y=(KREP*dist_mul*(cur_y-obstacle_y))/pow(d_from_rep,3)
            else:
                F_Rep_x=0
                F_Rep_y=0
        else:
            F_Rep_x=0
            F_Rep_y=0
        
        print(F_Rep_x," ",F_Rep_x)
        F_Res_x=F_Att_x+F_Rep_x
        F_Res_y=F_Att_y+F_Rep_y
        
        F_Mag=pow(pow(F_Res_x,2)+pow(F_Res_y,2),0.5)
        
        if(F_Mag!=0):
            x=V_MAX*(F_Res_x/F_Mag)
            y=V_MAX*(F_Res_y/F_Mag)
        else:
            #PERBUTATION
            #print("Zero Force")
            x=0
            y=0
        
        if(visited_point[i][cord]>25):
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
            print(i,"th robot reached destination!")
            reached.append(i)
            counter+=1
        
        #HERE
        
        '''
        #Stopping Condition 1 for Ball
        dist1=abs(y_pos-final_y)
        dist2=abs(x_pos-final_x)
        if(dist1<dist_threshold and dist2<dist_threshold):
            print(i," reached Destination !")
            reached.append(i)
            counter+=1
        '''    
            
            
    if(counter>=14):
        print("PROGRAM ENDS HERE!")
        break
    tk.update()
    time.sleep(0.001)
    pass

tk.mainloop()