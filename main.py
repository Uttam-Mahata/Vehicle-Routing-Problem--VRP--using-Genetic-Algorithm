import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from deap import base, creator, tools, algorithms

# Set random seed for reproducibility
random.seed(42)

# Define the number of customers, vehicles, and the depot (warehouse)
NUM_CUSTOMERS = 100
DEPOT = (50, 50)  # Location of depot
VEHICLE_CAPACITY = 20
DEMAND = [random.randint(1, 5) for _ in range(NUM_CUSTOMERS)]  # Random customer demands

# Generate random customer locations
CUSTOMER_LOCATIONS = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(NUM_CUSTOMERS)]

# Fitness function: minimize total distance
def calculate_total_distance(individual):
    total_distance = 0
    current_location = DEPOT
    vehicle_load = 0
    for customer_index in individual:
        next_location = CUSTOMER_LOCATIONS[customer_index]
        vehicle_load += DEMAND[customer_index]
        if vehicle_load > VEHICLE_CAPACITY:  # If vehicle exceeds capacity, go back to depot
            total_distance += np.linalg.norm(np.array(current_location) - np.array(DEPOT))
            current_location = DEPOT
            vehicle_load = DEMAND[customer_index]  # Load vehicle with next customer's demand
        
        total_distance += np.linalg.norm(np.array(current_location) - np.array(next_location))
        current_location = next_location

    # Return to depot after serving all customers
    total_distance += np.linalg.norm(np.array(current_location) - np.array(DEPOT))
    return total_distance,

# Set up Genetic Algorithm with DEAP
def setup_ga():
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimization problem
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    toolbox = base.Toolbox()
    
    # Define the individual (a permutation of customer indices)
    toolbox.register("indices", random.sample, range(NUM_CUSTOMERS), NUM_CUSTOMERS)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    # Genetic operators
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", calculate_total_distance)
    
    return toolbox

# Initialize plot
fig, ax = plt.subplots(figsize=(8, 8))
line, = ax.plot([], [], 'b-', linewidth=2)
depot_point = ax.scatter(*DEPOT, label="Depot", color="red", marker='s', s=100)
customer_points = ax.scatter([], [], label="Customers", color="blue")
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.legend()
plt.title("Vehicle Routing Problem Solution")

# Animation function to update the plot
def update_plot(best_individual):
    # Clear the current plot
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.scatter(*DEPOT, label="Depot", color="red", marker='s', s=100)

    # Plot the customer locations
    for loc in CUSTOMER_LOCATIONS:
        ax.scatter(*loc, color="blue")

    # Plot the route
    current_location = DEPOT
    vehicle_load = 0
    x_data, y_data = [DEPOT[0]], [DEPOT[1]]

    for customer_index in best_individual:
        next_location = CUSTOMER_LOCATIONS[customer_index]
        vehicle_load += DEMAND[customer_index]
        if vehicle_load > VEHICLE_CAPACITY:  # Go back to depot if vehicle is full
            x_data.append(DEPOT[0])
            y_data.append(DEPOT[1])
            vehicle_load = DEMAND[customer_index]

        # Plot the route to the next customer
        x_data.append(next_location[0])
        y_data.append(next_location[1])

    # Return to depot after all deliveries
    x_data.append(DEPOT[0])
    y_data.append(DEPOT[1])
    
    # Update line data
    line.set_data(x_data, y_data)
    ax.plot(x_data, y_data, 'b-', linewidth=2)

    # Add customer annotations
    for i, loc in enumerate(CUSTOMER_LOCATIONS):
        ax.annotate(f"{i+1}", (loc[0]+1, loc[1]+1), fontsize=12)

    ax.legend()
    ax.set_title("Vehicle Route")
    plt.draw()

# Genetic Algorithm execution
def run_ga():
    toolbox = setup_ga()
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)  # Save the best solution
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)
    
    generations_data = []

    # Run the genetic algorithm
    for gen in range(30):  # 30 generations
        pop = algorithms.varAnd(pop, toolbox, cxpb=0.7, mutpb=0.2)
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop = toolbox.select(pop, len(pop))
        record = stats.compile(pop)
        hof.update(pop)

        # Store best individual for animation
        best_individual = hof[0]
        generations_data.append(best_individual)
        print(f"Generation {gen}: Best Fitness = {best_individual.fitness.values[0]}")

    return generations_data

if __name__ == "__main__":
    # Initial customer plot
    for loc in CUSTOMER_LOCATIONS:
        plt.scatter(*loc, color="blue")
    plt.scatter(*DEPOT, label="Depot", color="red", marker='s', s=100)

    # Run GA
    generations_data = run_ga()

    # Animate the best solutions over generations
    ani = FuncAnimation(fig, update_plot, frames=generations_data, repeat=False)
    plt.show()
