import tkinter as tkr
import time
import random


# ALL THE PARAMETERS USED
agent_count=14
canvas_size=600
robot_radius=10
KATT=2
KREP=10000
D_REP=2*robot_radius
V_MAX=1
D_ATT=5*robot_radius

tk=tkr.Tk()
tk.title("LAB TEST 1.1 - IRM2017008")
canvas=tkr.Canvas(tk,width=canvas_size,height=canvas_size)
canvas.grid()

initial_points=[]
initial_points_rgb=[]
for i in range(int(agent_count/2)):
    init_x=random.randint(robot_radius,canvas_size-robot_radius)
    init_y=random.randint(robot_radius,canvas_size-robot_radius)
    flag=1
    while(flag==1):
        flag=0
        for j in range(len(initial_points)):
            temp_dist=pow(pow(init_x-initial_points[j][0],2)+pow(init_y-initial_points[j][1],2),0.5)
            if(temp_dist<2*robot_radius):
                flag=1
                break
        if(flag==1):
            init_x=random.randint(robot_radius,canvas_size-robot_radius)
            init_y=random.randint(robot_radius,canvas_size-robot_radius)
    
    initial_points.append([init_x,init_y])
    rgb=[]
    for j in range(3):
        col=random.randint(0,50)
        rgb.append(col)
    initial_points_rgb.append(rgb)
    
    
for i in range(int(agent_count/2)):
    init_x=random.randint(robot_radius,canvas_size-robot_radius)
    init_y=random.randint(robot_radius,canvas_size-robot_radius)
    flag=1
    while(flag==1):
        flag=0
        for j in range(len(initial_points)):
            temp_dist=pow(pow(init_x-initial_points[j][0],2)+pow(init_y-initial_points[j][1],2),0.5)
            if(temp_dist<2*robot_radius):
                flag=1
                break
        if(flag==1):
            init_x=random.randint(robot_radius,canvas_size-robot_radius)
            init_y=random.randint(robot_radius,canvas_size-robot_radius)
    
    initial_points.append([init_x,init_y])
    rgb=[]
    for j in range(3):
        col=random.randint(205,255)
        rgb.append(col)
    initial_points_rgb.append(rgb)


balls=[]
for i in range(agent_count):
    init_x=initial_points[i][0]
    init_y=initial_points[i][1]
    if(i<int(agent_count/2)):
        ball=canvas.create_oval(init_x-robot_radius,init_y-robot_radius,init_x+robot_radius,init_y+robot_radius,fill="yellow")
    else:
        ball=canvas.create_oval(init_x-robot_radius,init_y-robot_radius,init_x+robot_radius,init_y+robot_radius,fill="blue")
    balls.append(ball)

def get_d_soc(dist):
    ret=3*robot_radius+(dist/(255*3))*6*robot_radius
    return ret

def get_k_att(dist):
    ret=100-(dist/(255*3))*90
    return ret/10

def get_k_rep(dist):
    ret=1000+(dist/(255*3))*90000000
    return ret

diff={}
dist_soc={}
k_att={}
k_rep={}
for i in range(agent_count):
    for j in range(agent_count):
        if(i==j):
            continue
        diff_temp=0
        for k in range(3):
            diff_temp=diff_temp+abs(initial_points_rgb[i][k]-initial_points_rgb[j][k])
        diff[(i,j)]=diff_temp
        dsoc=get_d_soc(diff_temp)
        att=get_k_att(diff_temp)
        rep=get_k_rep(diff_temp)
        dist_soc[(i,j)]=dsoc
        k_att[(i,j)]=att
        k_rep[(i,j)]=rep
        dist_soc[(j,i)]=dsoc
        k_att[(j,i)]=att
        k_rep[(j,i)]=rep

visited_point=[]
for i in range(agent_count):
    visited_point.append({})

while True:
    for i in range(agent_count):
        
        ball=balls[i]
        cur_pos=canvas.coords(ball)
        cur_x=int(cur_pos[0]+robot_radius)
        cur_y=int(cur_pos[1]+robot_radius)
        cord=(cur_x,cur_y)
        if(cord in visited_point[i]):
            visited_point[i][cord]=visited_point[i][cord]+1
        else:
            visited_point[i][cord]=1
        
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
        
        F_Mag=pow(pow(F_x,2)+pow(F_y,2),0.5)
        
        if(F_Mag!=0):
            x=V_MAX*(F_x/F_Mag)
            y=V_MAX*(F_y/F_Mag)
        else:
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

    tk.update()
    time.sleep(0.001)
    pass

tk.mainloop()