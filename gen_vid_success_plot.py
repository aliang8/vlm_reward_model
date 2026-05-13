import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import matplotlib as mpl

is_robometer = False
max_y_value = 18 # max of this and success_timestamps

# font
mpl.rcParams['font.family'] = 'Palatino'
# set font size to 15
mpl.rcParams['font.size'] = 20

# 1. SETUP DATA
if is_robometer:
    success_timestamps = [6, 7, 8.5, 11, 13, 13.7, 14, 14.5, 16.7, 17.1, 17.5, 20, 21.5, 22, 22.3, 22.7, 23.5, 24]
else:
    success_timestamps = [1.8, 2.2, 4.5, 12.5, 18, 18.5, 24.8]

if is_robometer:
    final_time = 24
else:
    final_time = 25
fps = 15
total_frames = fps * final_time
time_frames = np.linspace(0, final_time, total_frames)



# 2. SETUP PLOT (Dark Mode Styling)
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

fig, ax = plt.subplots(figsize=(6, 7), facecolor='black') 
ax.set_facecolor('black')

# Color palette: Neon Cyan for the line, White for the leading dot
if is_robometer:
    line_color = '#B20000' 
    dot_color = '#B20000'
else:
    line_color = '#9C92C0' 
    dot_color = '#9C92C0'

line, = ax.plot([], [], lw=2.5, color=line_color, drawstyle='steps-post')
head_dot = ax.scatter([], [], color=dot_color, s=40, zorder=5, edgecolors=line_color, facecolors='none')

# Formatting
ax.set_xlim(0, final_time)
ax.set_ylim(0, max(len(success_timestamps) + 1, max_y_value))
# Subtle axis labels
ax.set_xlabel('Time', fontsize=15, fontweight='bold')
ax.set_ylabel('Total Successes', fontsize=15, fontweight='bold')

# Despine (remove top and right border) and set remaining spine colors
sns.despine()
ax.spines['left'].set_color('#444444') # Dark grey spine for subtlety
ax.spines['bottom'].set_color('#444444')

# only int on y axis
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
# disable x tick labels
ax.set_xticklabels([])


plt.tight_layout()

# 3. ANIMATION FUNCTIONS
def update(frame):
    current_time = time_frames[frame]
    past_successes = [t for t in success_timestamps if t <= current_time]
    
    x_data = [0] + past_successes
    y_data = list(range(len(x_data)))
    
    x_data.append(current_time)
    y_data.append(y_data[-1])
    
    line.set_data(x_data, y_data)
    head_dot.set_offsets([[current_time, y_data[-1]]])
    
    return line, head_dot

# 4. RUN / SAVE
ani = FuncAnimation(
    fig, update, frames=total_frames, interval=1000/fps, blit=True
)

# IMPORTANT: Set savefacecolor to black when saving, otherwise it might default to white
ani.save(f'dark_mode_success_{"robometer" if is_robometer else "roboreward"}.mp4', writer='ffmpeg', fps=fps, dpi=200, savefig_kwargs={'facecolor':'black'})

#plt.show()