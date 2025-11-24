"""
2-Opt Algorithm for TSP
Implements local search heuristic with edge swap optimization
"""

import numpy as np
import time
import random
from src.utilities import calculate_distance


class TwoOptTSP:
    """2-Opt solver for Traveling Salesman Problem"""
    
    def __init__(self, cities):
        """
        Initialize TSP solver with cities
        
        Args:
            cities: List of tuples (name, x, y)
        """
        self.cities = cities
        self.n = len(cities)
        self.distance_matrix = self.create_distance_matrix()
        self.best_tour = None
        self.best_distance = float('inf')
        
        # Statistics tracking
        self.iterations = 0
        self.swaps_made = 0
        self.improvements = 0
        self.start_time = 0
        self.end_time = 0
        self.computation_time = 0
        self.distance_history = []
        
        # Visualization
        self.callback = None
        self.visualization_delay = 0.1
    
    def set_progress_callback(self, callback):
        """Set callback function for progress updates"""
        self.callback = callback
    
    def create_distance_matrix(self):
        """Create distance matrix from city coordinates"""
        n = len(self.cities)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    matrix[i][j] = calculate_distance(
                        self.cities[i][1], self.cities[i][2],
                        self.cities[j][1], self.cities[j][2]
                    )
                else:
                    matrix[i][j] = 0
        
        return matrix
    
    def calculate_tour_distance(self, tour):
        """Calculate total distance of a tour"""
        distance = 0
        for i in range(len(tour)):
            distance += self.distance_matrix[tour[i]][tour[(i + 1) % len(tour)]]
        return distance
    
    def create_initial_tour_nearest_neighbor(self):
        """Create initial tour using nearest neighbor heuristic"""
        unvisited = set(range(1, self.n))
        tour = [0]  # Start at city 0
        
        current = 0
        while unvisited:
            nearest = min(unvisited, key=lambda city: self.distance_matrix[current][city])
            tour.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        return tour
    
    def create_initial_tour_random(self):
        """Create random initial tour"""
        tour = list(range(self.n))
        random.shuffle(tour[1:])  # Keep first city fixed
        return tour
    
    def two_opt_swap(self, tour, i, k):
        """
        Perform 2-opt swap: reverse tour segment between i and k
        
        Args:
            tour: Current tour
            i, k: Indices for swap
            
        Returns:
            New tour after swap
        """
        new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
        return new_tour
    
    def calculate_swap_delta(self, tour, i, k):
        """
        Calculate change in distance if swap is performed
        Faster than recalculating entire tour
        """
        n = len(tour)
        
        # Current edges
        a, b = tour[i-1], tour[i]
        c, d = tour[k], tour[(k+1) % n]
        
        # Current distance
        current = self.distance_matrix[a][b] + self.distance_matrix[c][d]
        
        # New distance after swap
        new = self.distance_matrix[a][c] + self.distance_matrix[b][d]
        
        return new - current
    
    def solve(self, initial_method='nearest_neighbor'):
        """
        Solve TSP using 2-Opt algorithm
        
        Args:
            initial_method: 'nearest_neighbor' or 'random'
            
        Returns:
            Tuple of (best_tour, best_distance)
        """
        self.start_time = time.time()
        
        # Create initial tour
        if initial_method == 'nearest_neighbor':
            tour = self.create_initial_tour_nearest_neighbor()
        else:
            tour = self.create_initial_tour_random()
        
        current_distance = self.calculate_tour_distance(tour)
        self.best_tour = tour.copy()
        self.best_distance = current_distance
        self.distance_history.append(current_distance)
        
        # Notify initial state
        if self.callback:
            self.callback({
                'iteration': 0,
                'tour': tour,
                'distance': current_distance,
                'swaps_made': 0,
                'improvements': 0,
                'phase': 'initial'
            })
            time.sleep(self.visualization_delay)
        
        # 2-Opt improvement loop
        improved = True
        self.iterations = 0
        
        while improved:
            improved = False
            self.iterations += 1
            
            # Try all possible edge swaps
            for i in range(1, self.n - 1):
                for k in range(i + 1, self.n):
                    # Visualize considering this swap
                    if self.callback:
                        self.callback({
                            'iteration': self.iterations,
                            'tour': tour,
                            'distance': current_distance,
                            'swaps_made': self.swaps_made,
                            'improvements': self.improvements,
                            'considering_swap': (i, k),
                            'phase': 'searching'
                        })
                        time.sleep(self.visualization_delay * 0.5)
                    
                    # Calculate improvement
                    delta = self.calculate_swap_delta(tour, i, k)
                    
                    if delta < -0.001:  # Improvement found (with small epsilon)
                        # Perform swap
                        tour = self.two_opt_swap(tour, i, k)
                        current_distance += delta
                        self.swaps_made += 1
                        self.improvements += 1
                        improved = True
                        
                        # Update best if needed
                        if current_distance < self.best_distance:
                            self.best_tour = tour.copy()
                            self.best_distance = current_distance
                            self.distance_history.append(current_distance)
                        
                        # Visualize swap
                        if self.callback:
                            self.callback({
                                'iteration': self.iterations,
                                'tour': tour,
                                'distance': current_distance,
                                'swaps_made': self.swaps_made,
                                'improvements': self.improvements,
                                'swap_performed': (i, k),
                                'improvement': -delta,
                                'phase': 'swap'
                            })
                            time.sleep(self.visualization_delay)
                        
                        break  # Restart with new tour
                
                if improved:
                    break
        
        # Final result
        self.end_time = time.time()
        self.computation_time = self.end_time - self.start_time
        
        if self.callback:
            self.callback({
                'iteration': self.iterations,
                'tour': self.best_tour,
                'distance': self.best_distance,
                'swaps_made': self.swaps_made,
                'improvements': self.improvements,
                'phase': 'complete'
            })
        
        return self.best_tour, self.best_distance
    
    def get_statistics(self):
        """Get solving statistics"""
        return {
            'iterations': self.iterations,
            'swaps_made': self.swaps_made,
            'improvements': self.improvements,
            'computation_time': self.computation_time,
            'best_distance': self.best_distance,
            'initial_distance': self.distance_history[0] if self.distance_history else 0,
            'improvement_percent': ((self.distance_history[0] - self.best_distance) / 
                                   self.distance_history[0] * 100) if self.distance_history else 0,
            'distance_history': self.distance_history
        }