#-*-coding:utf-8-*-
import random
import math
from public_transport import Connection

class SimulatedAnnealing: 
    """ A class that implements the heuristic algorithm of simulated displaying."""

    INITIAL_TEMPERATURE = 150000
    INITIAL_TEMPTERATURE_LENGTH = 100
    COOLING_RATIO = 0.99

    INFINITY = float("inf")

    def __init__(self, graph): 
        """ The constructor of the object. """
        self.graph = graph
        # mapping index -> top of the graph
        # self.index_to_node = self.graph.vertices(); 

    def optimal_hamiltonian_cycle(self):
        """ The method finding the optimal (minimal) Hamiltonian cycle in the graph. """

        best_travel_time, edge_cycle = self.search_min_hamiltionian_cycle()

        if best_travel_time is None or best_travel_time < 0: 
            return (None, None) 

        printable_cycle = ""
        # reconstruction of the optimal cycle
        for edge in edge_cycle:
            printable_cycle += str(edge.source()) 
            if type(edge) is Connection: 
                printable_cycle += "(" + str(edge.line_number()) + ")"
            printable_cycle += "->"
        # appending connection from last to first node 
        printable_cycle += str(edge_cycle[-1].target())
        if type(edge_cycle[-1]) is Connection: 
                printable_cycle += "(" + str(edge_cycle[-1].line_number()) + ")"

        return (best_travel_time, printable_cycle)

    def search_min_hamiltionian_cycle(self): 
        """ An auxiliary method executing the cycle search algorithm.
             Implementation of the simulated scoring algorithm. """
        
        # 1. STARTING PERMUTATION
        permutation = [node for node in self.graph.vertices()] # fill with vertices
        random.shuffle(permutation) # shuffle vertex permutation

        # 2. INITIALIZATION OF TEMPERATURE AND INITIAL SOLUTION
        # parameters controlling the algorithm
        T = self.INITIAL_TEMPERATURE
        temperature_length = self.INITIAL_TEMPTERATURE_LENGTH
        # current solution
        curr_solution = permutation
        curr_travel_time = self.hamiltonian_cycle_travel_time(curr_solution)

        # the best solution
        best_solution = curr_solution
        best_travel_time = curr_travel_time

        # 3. LOWERING TEMPERATURE LOOP (REFRIGERATION)
        while True: 

            if len(curr_solution) < 4: break 

            # 4. LOOP ATTEMPT TO TRY THE NEW SOLUTION FOR A TEMPERATURE
            for i in range(temperature_length): 

                # generating a new solution
                new_solution, vi_idx, vj_idx = self.generate_new_solution(curr_solution)
                # calculating the time difference between the old and the new solution
                time_delta = self.travel_time_change(curr_travel_time, new_solution, vi_idx, vj_idx)

                if time_delta <= 0: 
                    # <0 the new solution has a better travel time
                    # =0 both permutations are not a cycle or the same travel time

                    # 5.1 I ACCEPT A NEW PERMUTATION
                    curr_solution = new_solution
                    curr_travel_time += time_delta
                    # the current permutation is the best
                    best_solution = curr_solution
                    best_travel_time = curr_travel_time

                else: 
                    # >0 the new solution has a worse travel time
                    #    or is not a cycle 

                    # 5.2 I ACCEPT A NEW PERMUTATION WITH SURE OF LIKELIHOOD
                    # the worse the travel time, the less likely it is
                    # the higher the temperature, the higher the probability

                    # drawing of values [0,1]
                    rand_num = random.random()

                    # checking if the drawn value is smaller than the one designated
                    # probability of accepting the worse solution
                    if rand_num < self.probability(time_delta, T):
                        # I ACCEPT A BROTHER SOLUTION
                        curr_solution = new_solution
                        curr_travel_time += time_delta

            # 6. COOLING - REDUCING TEMPERATURE
            T *= self.COOLING_RATIO

            # increase in the number of trials for lower temperatures
            length_ratio =  5.0 if self.INITIAL_TEMPERATURE/T > 5.0 else self.INITIAL_TEMPERATURE/T
            temperature_length = int(self.INITIAL_TEMPTERATURE_LENGTH*length_ratio)

            if T <= 1: # condition of the end of the loop
                break

        # 7. END - the best solution is best_travel_time, best_solution
        if best_travel_time == self.INFINITY: 
            return (None, None)

        edge_cycle = []

        # 8. RECONSTRUCTION OF THE HAMILTON CYCLE ON THE BASIS OF PERMUTATION OF DRILLS
        for i in range(len(best_solution)):
            vi = best_solution[i]
            vj = best_solution[(i+1)%len(best_solution)]

            best_edge = None 
            for edge in self.graph.get_edges_from(vi):
                if best_edge == None or best_edge.weight() > edge.weight():
                    best_edge = edge

            if not best_edge: # no connection between the vertex vi - vj
                return (None, None) 

            edge_cycle.append(best_edge)

        return (best_travel_time, edge_cycle)

    def generate_new_solution(self, old_solution):
        """ An auxiliary method that generates a new solution (permutations)
             based on the old one. The algorithm for generating a new permutation:
             1. Random generation of vi_idx indexes, vj_idx from the range [0, len (permutation))
             2. Change the vertex pairs (vi, vi + 1) and (vj, vj + 1) to get
                pairs (vi, vj) and (vi + 1, vj + 1)
             3. Reversal of the order of the permutation elements (vi + 1, ..., vj) -> (vj, ..., vi + 1) """

        new_solution = old_solution[:] # copying permutations
        if len(new_solution) < 4: return new_solution # too few elements to draw 2 pairs

        # 1. sampling of vi_idx <vj_idx indices
        n = len(new_solution)
        vi_idx = random.randrange(0, n-1) %n # 
        while True: 
            vj_idx = (random.randrange(0, n-(vi_idx+1)) + (vi_idx+2) ) % n 
            if vi_idx != vj_idx and vi_idx != ((vj_idx+1)%n):
                break

        print("The index pairs were drawn (vi, vi+1) = (%d, %d) and (vj, vj+1) = (%d,%d)" % 
            (vi_idx, (vi_idx+1)%n, vj_idx, (vj_idx+1)%n))

        # 2. replacement of vertex pairs (vi, vi+1) i (vj, vj+1)
        #    receiving a pair (vi, vj) oraz (vi+1, vj+1)
        #    or swap(vi+1, vj)
        (new_solution[(vi_idx+1)%n], new_solution[vj_idx]) = (new_solution[vj_idx],new_solution[(vi_idx+1)%n])

        # 3. reversing the order of items to the list (vi+1,...vj) -> (vj, ..., vi+1)
        new_solution[((vi_idx+1)%n+1):vj_idx] = new_solution[((vi_idx+1)%n+1):vj_idx][::-1]

        self.print_permutation(old_solution)
        self.print_permutation(new_solution)

        return (new_solution, vi_idx, vj_idx)

    def travel_time_change(self, old_travel_time, new_solution, vi_idx, vj_idx): 
        """ An auxiliary method that calculates the change in travel time between the old and the new solution.
             1. the old solution was not the correct cycle, the new permutation may be it, but it does not have to
                (need to re-determine the cycle length for vertex permutations)
             2. the old solution was the correct cycle, after the change the new permutation can be correct
                cycle, but it does not have to."""

        time_delta = 0 

        # 1. the old permutation was not a cycle
        if old_travel_time == self.INFINITY: 
            # we calculate the transition time of the new permutation
            new_travel_time = self.hamiltonian_cycle_travel_time(new_solution)
            # calculation of time change
            # a) INFINITY - INFINITY == 0, both permutations are not a cycle
            # b) new_time - INFINITY < 0, the new permutation is a cycle
            time_delta = new_travel_time - old_travel_time
        else:
            # 2. the old permutation was a cycle
            #    determining the difference incrementally from the formula: 
            #    time_delta = time(vi, vi+1) + time(vj,vj+1) - time(vi,vj) - time(vi+1,vj+1)
            #    if any of the new edges does not exist then time_delta = INFINITY
            n = len(new_solution)
            time_new_edge_i = self.graph.weight_between(new_solution[vi_idx], new_solution[(vi_idx+1)%n])
            time_new_edge_j = self.graph.weight_between(new_solution[vj_idx], new_solution[(vj_idx+1)%n])

            if time_new_edge_i == self.INFINITY or time_new_edge_j == self.INFINITY:
                time_delta = INFINITY - old_travel_time # należy odjąć czas starego cyklu 
            else: 
                # both correct cycles - let us calculate the difference of times
                time_old_edge_i = self.graph.weight_between(new_solution[vi_idx], new_solution[vj_idx])
                time_old_edge_j = self.graph.weight_between(new_solution[(vi_idx+1)%n], new_solution[(vj_idx+1)%n])

                time_delta = time_new_edge_i + time_new_edge_j - time_old_edge_i - time_old_edge_j

        # possible results: 
        # time_delta == 0, both of these changes are not cycles, or the time has not changed
        # time_delta << 0, the new permutation is a cycle, and the old one is not
        # time_delta < 0, both permutations are cycles, the new one has a shorter time
        # time_delta > 0, both perturbations are cycles, the new one has a longer time
        # time_delta >> 0, the new permutation is not a cycle, the old one was a cycle
        return time_delta

    def hamiltonian_cycle_travel_time(self, permutation): 
        """ An auxiliary method that returns the travel time for a given cycle.
             If for a passed vertex permutation the cycle does not exist
             (none of the edges) is the method returns INFINITY."""
        
        travel_time = 0 

        # a loop after successive pairs of vertices
        for i in range(len(permutation)): 
            vi = permutation[i]
            vj = permutation[(i+1)%len(permutation)]

            # query for travel time between vi - vj
            edge_travel_time = self.graph.weight_between(vi,vj)
            # if INFINITY means no edge
            if edge_travel_time == self.INFINITY:
                return self.INFINITY
            travel_time += edge_travel_time
        
        return travel_time

    def print_permutation(self, permutation): 
        """ Print of permutations."""
        print("-".join(permutation)) 

    def probability(self, time_delta, T): 
        """ The probability of accepting a new cycle permutation. Depends:
             1. difference in travel time between the new and the old cycle
                the longer the lengthening of the time is less likely
             2. temperature - the higher the higher the probability
             The returned value is in the interval (0.1) because exp (negative_x). """

        if time_delta < 0: return 1

        return math.exp(-time_delta/T)

