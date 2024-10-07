### Mathematical Explanation of Optimizing Delivery Routes using a Genetic Algorithm (GA)

We are solving a variant of the **Vehicle Routing Problem (VRP)** using a Genetic Algorithm. Here’s the mathematical formulation behind the problem:

### 1. **Problem Setup**

Given:
- **V**: Set of vehicles, where each vehicle $$ v_i \in V $$ has a capacity $$ C_i $$.
- **N**: Set of customers, where each customer $$ n_j \in N $$ has a demand $$ d_j $$ and a time window $$ [t_j^{start}, t_j^{end}] $$.
- **W**: The central warehouse (depot), where all vehicles start and end their routes.
- **D(i, j)**: The distance between locations $$ i $$ and $$ j $$ (can also be time or cost).

### 2. **Decision Variables**

- **$$ x_{ij} $$**: A binary decision variable, which is:
  $$
  x_{ij} = 
  \begin{cases} 
  1 & \text{if vehicle travels directly from customer } i \text{ to customer } j \\
  0 & \text{otherwise}
  \end{cases}
  $$
  
- **$$ t_i $$**: The time vehicle arrives at customer $$ i $$.

### 3. **Objective Function**

The goal is to **minimize the total distance (or time)** traveled by all vehicles, which is mathematically represented as:
$$
\min \sum_{v_i \in V} \sum_{n_j \in N} \sum_{n_k \in N} D(j, k) \cdot x_{jk}
$$
Where:
- $$ x_{jk} $$ indicates whether vehicle $$ i $$ travels from customer $$ j $$ to customer $$ k $$.
- $$ D(j, k) $$ is the distance (or cost) of traveling from customer $$ j $$ to customer $$ k $$.

### 4. **Constraints**

#### Capacity Constraints:
Each vehicle cannot exceed its capacity $$ C_i $$, meaning the total demand served by a vehicle must be less than or equal to its capacity:
$$
\sum_{n_j \in route(v_i)} d_j \leq C_i \quad \forall v_i \in V
$$
Where $$ d_j $$ is the demand of customer $$ j $$.

#### Time Window Constraints:
Each vehicle must arrive at customer $$ j $$ within the customer's time window:
$$
t_j^{start} \leq t_j \leq t_j^{end} \quad \forall j \in N
$$
Where $$ t_j $$ is the time the vehicle arrives at customer $$ j $$.

#### Route Constraints:
Each vehicle must visit every customer exactly once and return to the depot, which implies:
$$
\sum_{i \in N} x_{ij} = 1 \quad \forall j \in N \quad (\text{each customer is visited once})
$$
$$
\sum_{j \in N} x_{ij} = 1 \quad \forall i \in N \quad (\text{each vehicle departs from and returns to the depot once})
$$

### 5. **Genetic Algorithm Components**

The **Genetic Algorithm** tries to solve this by evolving solutions over several generations:

#### Chromosome Representation:
A **chromosome** represents a route taken by the vehicles. Mathematically, this is an ordered list of customer indices, e.g., a permutation of $$ N $$ like $$ [1, 4, 3, 2, 5] $$.

#### Fitness Function:
The **fitness function** evaluates how good a chromosome (route configuration) is, by calculating the total distance traveled while ensuring that capacity and time window constraints are satisfied:
$$
f(\text{chromosome}) = \sum_{i=1}^{n-1} D(i, i+1)
$$
Where $$ D(i, i+1) $$ is the distance between two consecutive customers in the route.

To include penalties for constraint violations, the fitness function can be augmented:
$$
f(\text{chromosome}) = \sum_{i=1}^{n-1} D(i, i+1) + \lambda_1 \cdot P_{\text{capacity}} + \lambda_2 \cdot P_{\text{time}}
$$
Where:
- $$ P_{\text{capacity}} $$ is the penalty for violating vehicle capacity.
- $$ P_{\text{time}} $$ is the penalty for arriving outside a customer’s time window.
- $$ \lambda_1 $$ and $$ \lambda_2 $$ are penalty coefficients.

#### Selection:
Based on their fitness scores, the best chromosomes are selected to form the next generation. This is mathematically done by **probability proportional to fitness**:
$$
P(\text{selection of chromosome } i) = \frac{f(\text{chromosome } i)}{\sum_{j=1}^{N} f(\text{chromosome } j)}
$$
Where $$ f $$ is the fitness value and $$ N $$ is the population size.

#### Crossover:
Two selected parent chromosomes $$ P_1 $$ and $$ P_2 $$ are combined to produce an offspring. A typical crossover method is **Ordered Crossover (OX)**:
$$
\text{Child} = \text{Crossover}(P_1, P_2)
$$
For example, take a sub-sequence from $$ P_1 $$ and fill the remaining positions from $$ P_2 $$ without repeating customers.

#### Mutation:
Mutation introduces randomness to explore new solutions by, for example, swapping two customers in a route or reversing a subsequence:
$$
\text{Mutate}(chromosome) = \text{Swap}(i, j)
$$
Where customers at positions $$ i $$ and $$ j $$ in the route are swapped.

#### Termination:
The algorithm terminates after a fixed number of generations or when there’s no significant improvement in fitness.

### 6. **Conclusion**
Mathematically, the genetic algorithm evolves towards an optimal or near-optimal solution for the vehicle routing problem by exploring different configurations of delivery routes, using a combination of genetic operators like crossover and mutation. The solution minimizes the total distance, subject to capacity and time window constraints.

This GA approach provides an approximate solution to a complex combinatorial optimization problem like VRP, making it computationally feasible for real-world logistics.