import tkinter as tkr
import time
import random


# ALL THE PARAMETERS USED
agent_count=16
canvas_size=600
robot_radius=10
KATT=2
KREP=10000
D_REP=2*robot_radius
V_MAX=1
D_ATT=5*robot_radius
dist_threshold=400

first_point=[4*robot_radius,200]
obstacle_point=[600,250]
total_initial_points=[]
total_final_points=[]
for i in range(4):
    line=[]
    for j in range(4):
        line.append([first_point[0]+j*(3*robot_radius),first_point[1]+i*(3*robot_radius)])
    total_initial_points.append(line)
    
for i in range(4):
    total_final_points.append([])
    for j in range(4):
        total_final_points[i].append([])
        total_final_points[i][j].append(0)
        total_final_points[i][j].append(0)
        total_final_points[i][j][0]=total_initial_points[i][j][0]
        total_final_points[i][j][1]=total_initial_points[i][j][1]
        total_final_points[i][j][0]=total_final_points[i][j][0]+1000


tk=tkr.Tk()
tk.title("LAB TEST 4 - IRM2017008")
canvas=tkr.Canvas(tk,width=1200,height=canvas_size)
canvas.grid()

initial_points=total_initial_points

balls=[]

obstacle_ball=canvas.create_oval(obstacle_point[0]-2*robot_radius,obstacle_point[1]-2*robot_radius,obstacle_point[0]+2*robot_radius,obstacle_point[1]+2*robot_radius,fill="yellow")
        
    
for i in range(4):
    for j in range(4):
        init_x=initial_points[i][j][0]
        init_y=initial_points[i][j][1]
        ball=canvas.create_oval(init_x-robot_radius,init_y-robot_radius,init_x+robot_radius,init_y+robot_radius,fill="blue")
        balls.append(ball)

def get_d_soc():
    ret=3*robot_radius
    return ret

def get_k_att():
    ret=100
    return ret

def get_k_rep():
    ret=10000000
    return ret

def get_sigma():
        return [1,4]

diff={}
dist_soc={}
k_att={}
k_rep={}
sigma={}
for i in range(agent_count):
    for j in range(agent_count):
        if(i==j):
            continue
        dsoc=get_d_soc()
        att=get_k_att()
        rep=get_k_rep()
        dist_soc[(i,j)]=dsoc
        k_att[(i,j)]=att
        k_rep[(i,j)]=rep
        dist_soc[(j,i)]=dsoc
        k_att[(j,i)]=att
        k_rep[(j,i)]=rep
        sig=get_sigma()
        sigma[(i,j)]=sig
        sigma[(j,i)]=sig

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
                force_mag=k_att[(i,j)]*(1/pow(temp_dist,sigma[(i,j)][0]))
                F_x=F_x+force_mag*x_dir
                F_y=F_y+force_mag*y_dir
            else:
                #MODEL FOR REPULSION
                force_mag=-1*k_rep[(i,j)]*(1/pow(temp_dist,sigma[(i,j)][1]))
                F_x=F_x+force_mag*x_dir
                F_y=F_y+force_mag*y_dir
                
        ii=int(i/4)
        jj=int(i%4)
        final_x=total_final_points[ii][jj][0]
        final_y=total_final_points[ii][jj][1]
        
        d_from_goal=pow(pow(cur_x-final_x,2)+pow(cur_y-final_y,2),0.5)
        if(d_from_goal<=D_ATT):
            F_Att_x=-KATT*(cur_x-final_x)
            F_Att_y=-KATT*(cur_y-final_y)
        else:
            F_Att_x=(-KATT*D_ATT*(cur_x-final_x))/d_from_goal
            F_Att_y=(-KATT*D_ATT*(cur_y-final_y))/d_from_goal
        
        
        obstacle_x=int((canvas.coords(obstacle_ball))[0]+2*robot_radius)
        obstacle_y=int((canvas.coords(obstacle_ball))[1]+2*robot_radius)
        d_from_rep=pow(pow(cur_x-obstacle_x,2)+pow(cur_y-obstacle_y,2),0.5)-3*robot_radius
        if(d_from_rep<=D_REP):
            #print("Repul Force")
            dist_mul=(1/d_from_rep)-(1/D_REP)
            F_Rep_x=(KREP*dist_mul*(cur_x-obstacle_x))/pow(d_from_rep,3)
            F_Rep_y=(KREP*dist_mul*(cur_y-obstacle_y))/pow(d_from_rep,3)
        else:
            F_Rep_x=0
            F_Rep_y=0
        
        F_x=F_x+F_Att_x+F_Rep_x
        F_y=F_y+F_Att_y+F_Rep_y
        
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