import tkinter as tkr
import time
import random


# ALL THE PARAMETERS USED
agent_count=20
goal_count=4
group_count=5
canvas_size=600
initial_agent_canvas=150
robot_radius=10
dist_threshold=5*robot_radius
KATT=5
KREP=10000
D_REP=2*robot_radius
V_MAX=1
D_ATT=5*robot_radius
center_point=canvas_size/2
color=["red","blue","black","yellow","orange"]
d_soc_diff=6*robot_radius
d_soc_same=3*robot_radius
k_att_diff=5
k_att_same=20
k_rep_diff=5000000
k_rep_same=1000000

tk=tkr.Tk()
tk.title("QUESTION 3.1 - IRM2017008")
canvas=tkr.Canvas(tk,width=canvas_size,height=canvas_size)
canvas.grid()

final_points=[]
final_points.append([5*robot_radius,5*robot_radius])
final_points.append([canvas_size-5*robot_radius,5*robot_radius])
final_points.append([5*robot_radius,canvas_size-5*robot_radius])
final_points.append([canvas_size-5*robot_radius,canvas_size-5*robot_radius])

initial_points=[]
group_agent_count={}
group_reached_count={}

for i in range(group_count):
    group_agent_count[i]=0
    group_reached_count[i]=[]
    
group_index=[]

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
        
    gp=random.randint(0,group_count-1)
    group_index.append(gp)
    group_agent_count[gp]=group_agent_count[gp]+1
    
group_goal_list=[]
group_destination_index=[]
for i in range(group_count):
    goal_list=[]
    for j in range(goal_count):
        goal_list.append(j)
    random.shuffle(goal_list)
    index1=0
    group_goal_list.append(goal_list)
    group_destination_index.append(index1)

#print(initial_points)

#ball=canvas.create_oval(init_x,init_y,init_x+ball_diameter,init_y+ball_diameter,fill="yellow")


balls=[]
paths=[]
for i in range(agent_count):
    init_x=initial_points[i][0]
    init_y=initial_points[i][1]
    
    ball=canvas.create_oval(init_x-robot_radius,init_y-robot_radius,init_x+robot_radius,init_y+robot_radius,fill=color[group_index[i]])
    balls.append(ball)
    

final_balls=[]
for i in range(goal_count):
    final_x=final_points[i][0]
    final_y=final_points[i][1]
    final_ball=canvas.create_oval(final_x-robot_radius,final_y-robot_radius,final_x+robot_radius,final_y+robot_radius,fill="light blue")
    final_balls.append(final_ball)
    
    
def get_d_soc(a,b):
    if(a==b):
        return d_soc_same
    else:
        return d_soc_diff

def get_k_att(a,b):
    if(a==b):
        return k_att_same
    else:
        return k_att_diff

def get_k_rep(a,b):
    if(a==b):
        return k_rep_same
    else:
        return k_rep_diff

dist_soc={}
k_att={}
k_rep={}
for i in range(agent_count):
    for j in range(agent_count):
        if(i==j):
            continue
        dsoc=get_d_soc(group_index[i],group_index[j])
        att=get_k_att(group_index[i],group_index[j])
        rep=get_k_rep(group_index[i],group_index[j])
        dist_soc[(i,j)]=dsoc
        k_att[(i,j)]=att
        k_rep[(i,j)]=rep
        dist_soc[(j,i)]=dsoc
        k_att[(j,i)]=att
        k_rep[(j,i)]=rep
    
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
        
        final_x=final_points[group_goal_list[group_index[i]][group_destination_index[group_index[i]]]][0]
        final_y=final_points[group_goal_list[group_index[i]][group_destination_index[group_index[i]]]][1]
        
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
        
        F_x=0
        F_y=0
        
        for j in range(agent_count):
            if(i==j):
                continue
            xxx=int((canvas.coords(balls[j]))[0]+robot_radius)
            yyy=int((canvas.coords(balls[j]))[1]+robot_radius)
            temp_dist=pow(pow(cur_x-xxx,2)+pow(cur_y-yyy,2),0.5)
            x_dir=xxx-cur_x
            y_dir=yyy-cur_y
            hypo=pow(pow(y_dir,2)+pow(x_dir,2),0.5)
            x_dir=x_dir/hypo
            y_dir=y_dir/hypo
            if(temp_dist>=dist_soc[(i,j)]):
                #MODEL FOR ATTRACTION
                force_mag=k_att[(i,j)]*(temp_dist-dist_soc[(i,j)])
                F_x=F_x+force_mag*x_dir
                F_y=F_y+force_mag*y_dir
            else:
                #MODEL FOR REPULSION
                force_mag=k_rep[(i,j)]*(dist_soc[(i,j)]-temp_dist)
                F_x=F_x-force_mag*x_dir
                F_y=F_y-force_mag*y_dir
        
        
        F_Res_x=F_Att_x+F_x
        F_Res_y=F_Att_y+F_y
        
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
        
        
        #Stopping Condition 1 for Ball
        dist1=abs(y_pos-final_y)
        dist2=abs(x_pos-final_x)
        if(dist1<dist_threshold and dist2<dist_threshold):
            if(i not in group_reached_count[group_index[i]]):
                group_reached_count[group_index[i]].append(i);
        
        if(len(group_reached_count[group_index[i]])==group_agent_count[group_index[i]]):
            group_reached_count[group_index[i]]=[]
            print("HERE")
            group_destination_index[group_index[i]]=(group_destination_index[group_index[i]]+1)%goal_count
     
    tk.update()
    time.sleep(0.001)
    pass

tk.mainloop()