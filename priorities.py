import numpy as np
import matplotlib.pyplot as plt
import random
# Function to simulate a priority queue with given classes and simulation time
def simulate_priority_queue(classes, sim_time):
    # Initialize a list to store total response times for each class
    response_times = [0] * len(classes)
    # Initialize a list of empty queues for each class
    queue = [[] for _ in classes]

    for _ in range(sim_time):
        # Choose a random class according to its arrival rate
        
        arrival_rates = [cls["arrival_rate"] for cls in classes]
        class_idx = np.random.choice(len(classes), p=arrival_rates/np.sum(arrival_rates))

        # Calculate service time for the chosen class
        service_time = np.random.exponential(1/classes[class_idx]["service_rate"])

        # Calculate response time for the chosen class
        if not queue[class_idx]:
            response_time = service_time
        else:
            response_time = max(queue[class_idx][-1], service_time)

        # Update the queue and response times
        queue[class_idx].append(response_time)
        response_times[class_idx] += response_time

    # Calculate the mean response time for each class
    mean_response_times = [rt / sim_time for rt in response_times]

    return mean_response_times

# Scenario 1: ρ=0.69, 20 classes
classes_1 = [{"arrival_rate": random.uniform(0.01, 0.1), "service_rate": random.uniform(0.05, 0.5)} for _ in range(20)]
mean_response_times_1 = simulate_priority_queue(classes_1, 1000)

# Scenario 2: ρ=0.89, 9 classes
classes_2 = [{"arrival_rate": random.uniform(0.01, 0.1), "service_rate": random.uniform(0.05, 0.5)} for _ in range(9)]
mean_response_times_2 = simulate_priority_queue(classes_2, 1000)

# Plot the results
plt.plot(range(1, len(classes_1) + 1), mean_response_times_1, 'o-', label='Scenario 1: ρ=0.69, 20 classes')
plt.plot(range(1, len(classes_2) + 1), mean_response_times_2, 'x-', label='Scenario 2: ρ=0.89, 9 classes')

plt.xlabel('Class Priority')
plt.ylabel('Mean Response Time (s)')
plt.title('Response Time vs Class Priority')
plt.legend()
plt.grid()
plt.show()
