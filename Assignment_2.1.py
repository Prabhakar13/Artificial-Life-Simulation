import tkinter as tkr
import time

canvas_size=600
init_x=100
init_y=100
final_x=400
final_y=400
obstacle_x=250
obstacle_y=250
robot_radius=10
KATT=5
KREP=100000

motion = [[1, 0],[0, 1],[-1, 0],[0, -1],[-1, -1],[-1, 1],[1, -1],[1, 1]]

tk=tkr.Tk()
tk.title("Assignment 2.1 - IRM2017008")
canvas=tkr.Canvas(tk,width=canvas_size,height=canvas_size)
canvas.grid()

ball=canvas.create_oval(init_x-robot_radius,init_y-robot_radius,init_x+robot_radius,init_y+robot_radius,fill="yellow")
final_ball=canvas.create_oval(final_x-robot_radius,final_y-robot_radius,final_x+robot_radius,final_y+robot_radius,fill="light blue")
obstacle_ball=canvas.create_oval(obstacle_x-robot_radius,obstacle_y-robot_radius,obstacle_x+robot_radius,obstacle_y+robot_radius,fill="red")
path=canvas.create_line(init_x,init_y,final_x,final_y)

def get_att_pot(x,y):
    return 0.5*KATT*pow(pow(x-final_x,2)+pow(y-final_y,2),0.5)

def get_rep_pot(x,y):
    dist=pow(pow(x-obstacle_x,2)+pow(y-obstacle_y,2),0.5)

    if dist<=3*robot_radius:
        if dist<=0.1:
            dist=0.1
        return 0.5*KREP*(1.0/dist-1.0/(3*robot_radius))**2
    else:
        return 0.0

def create_map():
    grid=[[0.0 for i in range(canvas_size)] for i in range(canvas_size)]
    for x in range(canvas_size):
        for y in range(canvas_size):
            att_pot_val=get_att_pot(x,y)
            rep_pot_val=get_rep_pot(x,y)
            total_pot=att_pot_val+rep_pot_val
            grid[x][y]=total_pot
    return grid
            
canvas_grid=create_map()

while True:
    cur_pos=canvas.coords(ball)
    cur_x=int(cur_pos[0]+robot_radius)
    cur_y=int(cur_pos[1]+robot_radius)
    msf=float("inf")
    index=0
    for iter in range(8):
        xx=cur_x+motion[iter][0]
        yy=cur_y+motion[iter][1]
        if(canvas_grid[xx][yy]<msf):
            msf=canvas_grid[xx][yy]
            index=iter
    x=motion[index][0]
    y=motion[index][1]
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