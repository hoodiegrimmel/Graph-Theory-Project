# Random Graphs Threshold Experiment

This code generates random graphs G(n,p) and tests various properties to observe the threshold effect.

## What's in here

- `random_graphs.cpp` - C++ program that runs the experiments and outputs data to CSV
- `visualize.py` - Python script that reads the CSV and generates plots

## Requirements

### For the C++ part:
- A C++ compiler with C++17 support (g++, clang++, etc.)

### For the Python part:
- Python 3
- matplotlib
- numpy

You can install the Python dependencies with:
```bash
pip install matplotlib numpy
```

## How to Run

### Step 1: Compile and run the C++ experiment

```bash
g++ -O3 -o random_graphs random_graphs.cpp -std=c++17
./random_graphs
```

This will take a few minutes to run (it's doing 500 trials per data point). When it's done, you'll have a file called `experiment_results.csv` in the same folder.

If you're on Windows:
```bash
g++ -O3 -o random_graphs.exe random_graphs.cpp -std=c++17
random_graphs.exe
```

### Step 2: Generate the plots

Make sure `experiment_results.csv` is in the same folder as `visualize.py`, then run:

```bash
python visualize.py
```

or 

```bash
python3 visualize.py
```

This will generate:
- `plot_has_edge.png` - Edge existence threshold
- `plot_has_k3.png` - Triangle (K₃) threshold
- `plot_connected.png` - Connectivity threshold
- `plot_has_k4.png` - K₄ threshold
- `plot_hamiltonian.png` - Hamilton cycle threshold
- `plot_combined.png` - All five properties in one figure

## What the experiments test

| Property | What it checks | Theoretical Threshold |
|----------|---------------|----------------------|
| Has Edge | Does the graph have at least one edge? | p* = 2/n² |
| Has K₃ | Does the graph contain a triangle? | p* = 1/n |
| Is Connected | Can you reach any vertex from any other vertex? | p* = ln(n)/n |
| Has K₄ | Does the graph contain a complete graph on 4 vertices? | p* = n^(-2/3) |
| Is Hamiltonian | Does the graph have a cycle that visits every vertex exactly once? | p* = ln(n)/n |

## Tweaking the parameters

If you want to change the number of trials or test different values of n, you can edit `random_graphs.cpp`:

- `int trials = 500;` - Change this to run more/fewer trials per data point
- The `for (int n : {10, 50, 100, 500})` lines control which values of n get tested for each property

Fair warning: the Hamilton cycle test is O(n!) so don't go above n = 20
