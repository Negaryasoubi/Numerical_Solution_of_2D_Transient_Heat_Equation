# CFD project
# Negar Yasoubi_99543289 
import numpy as np
import matplotlib.pyplot as plt

# Define parameters
a =  111  #thermal diffusivity for copper [mm**2/s]
length = 30  #length of the square domain [mm]
time = 20   #simulation time [s]
min_T = 25  #initial temperature [°C]
nodes = 70  #number of grid points in each direction

# Initialize temperature field
u = np.zeros((nodes, nodes)) + min_T

# Set boundary conditions
u[0, :] = 100  # Top edge
u[-1, :] = 100  # Bottom edge
u[:,0] =0  # Left edge
u[:, -1] =0  # Right edge

# Define grid spacing and time step
dx = length / nodes
dy = length / nodes
dt = 0.2 * dx **2 / a  # Ensure stability 
t_nodes = int(time / dt)  # Number of time steps

# Create figure and colormap 
fig, axis = plt.subplots()
pcm = axis.pcolormesh(u, cmap = plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)

# Function to save results as plt for Tecplot
def write_results(u, time):
    
    filename = r"C:\Users\FC\Desktop\output/"+str(time)+".plt"
    with open(filename, 'w') as file:
        file.write("VARIABLES=X,Y,u\n")
        file.write("ZONE I=" + str(nodes) + " J=" + str(nodes) + "\n")
        for j in range(nodes ):
           for i in range(nodes ):
               file.write(str(i) + " " + str(j) + " " + str(u[j][i]) +"\n")
    
# Simulation loop
current =0.00000001
Previous = 0
counter = 0

while counter < time:
    w = u.copy()
    if current  - Previous >= 0.00000001:
        Previous = current
        for j in range(1, nodes - 1):
            for i in range(1, nodes - 1):
                dd_ux = (w[j - 1, i] - 2 * w[j, i] + w[j + 1, i]) / dx*2
                dd_uy = (w[j, i - 1] - 2 * w[j, i] + w[j, i + 1]) / dy*2
                u[j, i] = dt * a * (dd_uy + dd_ux) + w[j, i]
                

        current = np.average(u)
            

    else:
          break   # Stop if average temperature stops increasing more than 10**-7
      
    # Print information and update plot  
    print("t: {:.3f} [s], Average temperature: {:.2f} Celcius".format(counter, np.average(u)))
    #write_results(u, counter) it can be in the loop if we want the result in each step
    pcm.set_array(u)
    axis.set_title("Distribution at t: {:.3f} [s].".format(counter))
    plt.pause(0.01)
    
    counter += dt

# Save final results   
write_results(u, counter)
plt.show()