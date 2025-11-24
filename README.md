# TSP 2-Opt Solver

A Python-based GUI application that solves the Traveling Salesman Problem (TSP) using the 2-Opt local search algorithm.

## Project Information

**Course:** BSC - CS & IT Department  
**Module:** Comprehension (351 CP 81)  
**Algorithm:** 2-Opt (Local Search Heuristic)  
**Language:** Python with PyQt5  
**Author:** Francis Mitawa  
**Date:** November 2025

## Description

This application implements the 2-Opt algorithm to find high-quality solutions for the Traveling Salesman Problem. The GUI allows users to:
- Add cities with coordinates
- Choose initial tour method (Nearest Neighbor or Random)
- Visualize edge swaps in real-time
- See tour improvements step-by-step
- Compare initial vs optimized tour

## Features

- ✅ Interactive PyQt5 GUI
- ✅ Add/remove cities dynamically
- ✅ Real-time edge swap visualization
- ✅ Two initial tour methods
- ✅ Live statistics tracking
- ✅ Visual feedback for swaps

## Algorithm: 2-Opt

2-Opt is a local search heuristic that:
1. **Starts** with an initial tour (nearest neighbor or random)
2. **Iterates** through all pairs of edges
3. **Tests** if swapping edges reduces tour length
4. **Swaps** edges that improve the tour
5. **Repeats** until no improvements found

### Why 2-Opt?
- ✅ **Fast**: Much faster than exact algorithms for large problems
- ✅ **Good quality**: Typically within 5-10% of optimal
- ✅ **Simple**: Easy to understand and implement
- ✅ **Scalable**: Works well for 50+ cities
- ❌ **Not optimal**: Cannot guarantee finding the best solution

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone/download the project:
```bash
cd TSP-2-Opt
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### How to Use:
1. **Add Cities:** Enter city name and coordinates (x, y) and click "Add City"
2. **Load Sample:** Click "Load Sample Cities" for quick testing
3. **Choose Method:** Select initial tour method (Nearest Neighbor recommended)
4. **Start:** Click "Start 2-Opt" to begin optimization
5. **Watch:** Observe edge swaps in real-time
   - 🔴 Red dashed = edges being removed
   - 🟢 Green dashed = new edges being added
   - ✨ Bright green = swap just performed
6. **View Results:** See final tour and improvement statistics

## Project Structure

```
TSP-2-Opt/
│
├── src/
│   ├── __init__.py
│   ├── algorithm.py          # 2-Opt implementation
│   ├── gui.py                # PyQt5 GUI
│   ├── canvas_widget.py      # Visualization canvas
│   └── utilities.py          # Helper functions
│
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
├── README.md                 # This file
└── .gitignore
```

## Algorithm Explanation

### Edge Swap Process:

**Before Swap:**
```
A ------- B
          |
          |
C ------- D
```

**After Swap (if improvement found):**
```
A ------- C
          |
          |
B ------- D
```

The algorithm tries all possible edge pairs and keeps swaps that reduce total distance.

### Time Complexity:
- **Per iteration**: O(n²) - try all edge pairs
- **Total**: O(n² × k) where k = number of iterations
- Typically k is small (10-50 iterations)

### Space Complexity:
- O(n²) for distance matrix
- O(n) for tour storage

## Comparison with Branch & Bound

| Feature | 2-Opt | Branch & Bound |
|---------|-------|----------------|
| **Solution Quality** | Near-optimal (~95%) | Optimal (100%) |
| **Speed** | Very fast | Slower |
| **Scalability** | Excellent (100+ cities) | Limited (~20 cities) |
| **Guarantee** | No | Yes |
| **Best For** | Large problems | Small problems |

## Dependencies

```
PyQt5==5.15.9
numpy==1.24.3
```

## Testing

Sample test with 8 cities:
1. Click "Load Sample Cities"
2. Keep "Nearest Neighbor" selected
3. Click "Start 2-Opt"
4. Expected: 10-20 iterations, 5-15 swaps, ~10-20% improvement

## Known Limitations

- Visual updates may be too fast for very small problems (< 6 cities)
- Not guaranteed to find global optimum (can get stuck in local optimum)
- Multiple runs with different initial tours may yield different results

## Future Enhancements

- [ ] Add 3-Opt variant for better solutions
- [ ] Multiple restart option to avoid local optima
- [ ] Export tour to file
- [ ] Comparison mode with other algorithms

## License

Educational project for university coursework.

## Author

[Francis Mitawa]  
[francismitawa406@gmail.com]  
[Your GitHub]

## Acknowledgments

- 2-Opt algorithm by Croes (1958)
- PyQt5 for GUI framework
- Course instructors and supervisors