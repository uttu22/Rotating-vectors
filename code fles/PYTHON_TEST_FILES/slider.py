import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Step 1: Create the figure and the plot
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)  # Adjust plot to make space for sliders

# Initial values for amplitude and frequency
amp_init = 1
freq_init = 1

# Generate x values
x = np.linspace(0, 10, 1000)

# Generate initial y values for sine wave
y = amp_init * np.sin(2 * np.pi * freq_init * x)

# Plot the sine wave
line, = ax.plot(x, y, lw=2)

# Set labels and title
ax.set_xlabel('x')
ax.set_ylabel('Amplitude')
ax.set_title('Sine Wave with Adjustable Amplitude and Frequency')

# Step 2: Add sliders for amplitude and frequency
# Slider for amplitude
axamp = plt.axes([0.1, 0.2, 0.8, 0.05], facecolor='lightgoldenrodyellow')
amp_slider = Slider(axamp, 'Amplitude', 0.1, 10.0, valinit=amp_init)

# Slider for frequency
axfreq = plt.axes([0.1, 0.1, 0.8, 0.05], facecolor='lightgoldenrodyellow')
freq_slider = Slider(axfreq, 'Frequency', 0.1, 5.0, valinit=freq_init)

# Step 3: Update the plot when slider value changes
def update(val):
    amplitude = amp_slider.val
    frequency = freq_slider.val
    line.set_ydata(amplitude * np.sin(2 * np.pi * frequency * x))  # Update y values
    fig.canvas.draw_idle()  # Redraw the plot

# Link sliders to the update function
amp_slider.on_changed(update)
freq_slider.on_changed(update)

# Step 4: Display the plot
plt.grid(True)
plt.show()
