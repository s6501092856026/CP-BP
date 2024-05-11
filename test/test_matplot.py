import matplotlib.pyplot as plt

# Data
x = ["oil", "bio", "gas", "widget", "carbon"]
y = [452.56, 256.29, 348.86, 568.12, 682.22]

# Create a line plot
plt.plot(x, y)

# Customize the plot
plt.title("Line Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# Display the plot
plt.show()