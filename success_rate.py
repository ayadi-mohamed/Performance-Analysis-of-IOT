import numpy as np
import matplotlib.pyplot as plt
# Function to simulate the queue and compute the success rate with given parameters
def simulate_queue_success_rate(arrival_rate, service_rate, sim_time, t_on, t_off, lifetime, zeta, K):
    # Generate an array of inter-arrival times using an exponential distribution
    arrival_times = np.random.exponential(1/arrival_rate, int(sim_time * arrival_rate))
    # Generate an array of service times using an exponential distribution
    service_times = np.random.exponential(service_rate, int(sim_time * arrival_rate))
    # Initialize an empty queue
    queue = []
    # Initialize a counter for successful messages
    nbr_successful_messages = 0
    total_messages = 0
    # Server's initial state (ON)
    server_on = True
    # Time when the server switches its state
    server_switch_time = 0
    # Current simulation time
    time = 0
    # Iterate through all arrival times
    for i in range(len(arrival_times)):
        # Update the current simulation time

        time += arrival_times[i]
        # Increment the total messages counter
        total_messages += 1
        # Check if the server switches its state
        while server_switch_time < time:
            # If the server is ON, add an ON time period
            if server_on:
                server_switch_time += np.random.exponential(t_on)
            # If the server is OFF, add an OFF time period
            else:
                server_switch_time += np.random.exponential(t_off)
            # Switch the server's state
            server_on = not server_on
        
        if server_on:
            # Calculate the start and end times of the service
            if queue:
                service_start = max(queue[-1], time)
            else:
                service_start = time
            
            service_end = service_start + service_times[i]
            # Apply buffer capacity constraints
            if K != np.inf:
                queue = [t for t in queue if t >= (time - K/zeta)]
            # Apply message lifetime constraints
            if lifetime != np.inf and (service_end - time) > lifetime:
                continue
            
            if len(queue) < K * zeta:
                queue.append(service_end)
                nbr_successful_messages += 1
    # Calculate and return the success rate
    return nbr_successful_messages / total_messages

# Parameters
D = 0.125
TON_TOFF = 20
arrival_rates = np.linspace(0.05, 3.9, 100)
# Define experiments with different QoS features
experiments = [
    {"zeta": 1, "lifetime": np.inf, "K": np.inf},
    {"zeta": 1, "lifetime": 30, "K": np.inf},
    {"zeta": 0.75, "lifetime": np.inf, "K": np.inf},
    {"zeta": 1, "lifetime": np.inf, "K": 100},
]

# Simulate success rates for different experiments
# Simulate success rates for different experiments
for idx, exp in enumerate(experiments, 1):
    success_rates = []
    for arrival_rate in arrival_rates:
        success_rate = simulate_queue_success_rate(
            arrival_rate, D, 1000, TON_TOFF, TON_TOFF, exp["lifetime"], exp["zeta"], exp["K"]
        )
        success_rates.append(success_rate)
    
    plt.plot(arrival_rates, success_rates, label=f'Experiment {idx}')

plt.xlabel('Arrival Rate (messages/s)')
plt.ylabel('Success Rate')
plt.title('Success Rate vs Arrival Rate for Various ON/OFF Model Parameters')
plt.legend()
plt.grid()
plt.show()
