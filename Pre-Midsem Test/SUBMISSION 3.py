import tkinter as tkr
import time
import random


# ALL THE PARAMETERS USED
agent_count=14
goal_count=4
canvas_size=600
initial_agent_canvas=150
robot_radius=10
dist_threshold=3*robot_radius
KATT=2
KREP=10000
D_REP=2*robot_radius
V_MAX=1
D_ATT=5*robot_radius
center_point=canvas_size/2

tk=tkr.Tk()
tk.title("QUESTION 3 - IRM2017008")
canvas=tkr.Canvas(tk,width=canvas_size,height=canvas_size)
canvas.grid()

final_points=[]
final_points.append([5*robot_radius,5*robot_radius])
final_points.append([canvas_size-5*robot_radius,5*robot_radius])
final_points.append([5*robot_radius,canvas_size-5*robot_radius])
final_points.append([canvas_size-5*robot_radius,canvas_size-5*robot_radius])

initial_points=[]
destination_index=[]
agent_goal_list=[]
for i in range(agent_count):
    init_x=(random.randint(0,2*initial_agent_canvas)-initial_agent_canvas)+center_point
    init_y=(random.randint(0,2*initial_agent_canvas)-initial_agent_canvas)+center_point
    flag=1
    while(flag==1):
        flag=0
        for j in range(len(initial_points)):
            temp_dist=pow(pow(init_x-initial_points[j][0],2)+pow(init_y-initial_points[j][1],2),0.5)
            if(temp_dist<2*robot_radius):
                flag=1
                break
        if(flag==1):
            init_x=(random.randint(0,2*initial_agent_canvas)-initial_agent_canvas)+center_point
            init_y=(random.randint(0,2*initial_agent_canvas)-initial_agent_canvas)+center_point
    
    initial_points.append([init_x,init_y])
    
    goal_list=[]
    for j in range(goal_count):
        goal_list.append(j)
        
    random.shuffle(goal_list)
    index1=0
    agent_goal_list.append(goal_list)
    destination_index.append(index1)

#print(initial_points)

#ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="yellow")


balls=[]
paths=[]
for i in range(agent_count):
    init_x=initial_points[i][0]
    init_y=initial_points[i][1]
    
    ball=canvas.create_oval(init_x-robot_radius,init_y-robot_radius,init_x+robot_radius,init_y+robot_radius,fill="yellow")
    balls.append(ball)
    
    final_x=final_points[destination_index[i]][0]
    final_y=final_points[destination_index[i]][1]
    
    pi_x=init_x
    pi_y=init_y
    pf_x=final_x
    pf_y=final_y
    #path=canvas.create_line(pi_x,pi_y,pf_x,pf_y);
    #paths.append(path)
    

final_balls=[]
for i in range(goal_count):
    final_x=final_points[i][0]
    final_y=final_points[i][1]
    final_ball=canvas.create_oval(final_x-robot_radius,final_y-robot_radius,final_x+robot_radius,final_y+robot_radius,fill="light blue")
    final_balls.append(final_ball)
    

"""
initial_ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="light blue")
"""
final_ball=canvas.create_oval(final_x-robot_radius,final_y-robot_radius,final_x+robot_radius,final_y+robot_radius,fill="light blue")

visited_point=[]
for i in range(agent_count):
    visited_point.append({})

counter=0
while True:
    for i in range(agent_count):
        
        ball=balls[i]
        cur_pos=canvas.coords(ball)
        cur_x=int(cur_pos[0]+robot_radius)
        cur_y=int(cur_pos[1]+robot_radius)
        
        
        final_x=final_points[agent_goal_list[i][destination_index[i]]][0]
        final_y=final_points[agent_goal_list[i][destination_index[i]]][1]
        
        #destination_index[i]=(destination_index[i]+1)%goal_count
        
        obstacle_index=-1
        min_dist=1000
        for j in range(agent_count):
            if(i==j):
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
                print(F_Rep_x," ",F_Rep_x)
            else:
                F_Rep_x=0
                F_Rep_y=0
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
        
        '''
        if(x_pos==final_x and y_pos==final_y):
            print(i,"th robot reached destination!")
            reached.append(i)
            counter+=1
        '''
        
        #Stopping Condition 1 for Ball
        dist1=abs(y_pos-final_y)
        dist2=abs(x_pos-final_x)
        if(dist1<dist_threshold and dist2<dist_threshold):
            print(i," reached Destination !")
            destination_index[i]=(destination_index[i]+1)%goal_count 
     
    tk.update()
    time.sleep(0.001)
    pass

tk.mainloop()