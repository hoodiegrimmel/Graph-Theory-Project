# Project 1: Random Graphs and the Threshold Effect

## Introduction

So the whole point of this project is to mess around with random graphs and see if we can observe those "threshold effects" we talked about in class. The idea is pretty simple - generate a bunch of random graphs G(n,p), test some properties, and see if things suddenly start happening at certain values of p. Spoiler alert: they do, and it's actually pretty cool.

I went with this project because I have some coding experience and honestly the probabilistic stuff seemed more interesting than grinding through Ramsey number calculations by hand.

---

## Property 1: Has an Edge

**Theoretical Threshold:** $p^* = \frac{2}{n^2}$

This one's kind of trivial but we gotta start somewhere. The expected number of edges is $\binom{n}{2} \cdot p \approx \frac{n^2 p}{2}$. Setting this equal to 1 gives us $p^* = \frac{2}{n^2}$.

**Naive constant:** $c = 2$

**Experimental Results:**

Looking at the plots, the transition is insanely sharp for large n. For n = 500, the graph almost surely has an edge even at p = 0.02, which is way above the theoretical threshold of p* ≈ 0.000008. Basically once you have enough vertices, you need an absurdly small p to avoid having any edges at all. Makes sense if you think about it - with 500 vertices you have like 125,000 potential edges so even a tiny probability adds up.

---

## Property 2: Has a Triangle (K₃)

**Theoretical Threshold:** $p^* = \frac{c}{n}$ where $c = 6^{1/3} \approx 1.82$

The expected number of triangles is $\binom{n}{3} \cdot p^3 \approx \frac{n^3 p^3}{6}$. Setting this to 1 and solving gives $p = \frac{6^{1/3}}{n}$.

**Naive constant:** $c \approx 1.82$

**Experimental Results:**

The experimental 50% crossing point happens at around p ≈ 2/n, which is pretty close to the theoretical prediction. The curves get steeper as n increases which is exactly what we'd expect from the theory. Triangles are the smallest non-trivial subgraph so they're kind of the "hello world" of subgraph thresholds.

---

## Property 3: Is Connected

**Theoretical Threshold:** $p^* = \frac{\ln(n)}{n}$

This is the famous Erdős-Rényi result. The idea is that connectivity is basically determined by isolated vertices. The expected number of isolated vertices is $n(1-p)^{n-1} \approx n \cdot e^{-pn}$. Setting p = ln(n)/n makes this expectation go to 0 for λ > 1 and go to infinity for λ < 1.

**Naive constant:** $c = 1$

**Experimental Results:**

The experimental data lines up pretty well with theory. For n = 200, the theoretical threshold is p* ≈ 0.0265 and we see the transition happening around p ≈ 0.04. The ratio is about 1.2-1.5x which makes sense because the theoretical threshold is asymptotic (n → ∞) and we're working with finite graphs.

The connectivity threshold is honestly the most satisfying one because the math is so clean. Below the threshold you almost surely have lonely vertices floating around with no friends. Above the threshold everyone's connected. Very wholesome.

---

## Property 4: Has K₄

**Theoretical Threshold:** $p^* = \frac{c}{n^{2/3}}$ where $c = 24^{1/6} \approx 1.70$

The expected number of K₄ subgraphs is $\binom{n}{4} \cdot p^6 \approx \frac{n^4 p^6}{24}$. Setting this to 1 gives $p = \frac{24^{1/6}}{n^{2/3}}$.

**Naive constant:** $c \approx 1.70$

**Experimental Results:**

The transitions happen at around 1.7-1.9 times the theoretical threshold which is consistent with our naive estimate. The curves get steeper for larger n as expected. K₄ detection is O(n⁴) so I could only test up to n = 100 before my laptop started making concerning noises.

---

## Property 5: Has Hamilton Cycle

**Theoretical Threshold:** $p^* = \frac{\ln(n)}{n}$ (same order as connectivity)

This one's interesting because it has the same threshold as connectivity. The intuition is that once a graph is "robustly" connected (no isolated or degree-1 vertices), Hamilton cycles appear almost surely. Komlós and Szemerédi proved this in 1983.

**Naive constant:** $c = 1$

**Experimental Results:**

I could only test small values of n (up to 15) because checking for Hamilton cycles is NP-complete and the backtracking algorithm is O(n!) in the worst case. My computer would probably catch fire if I tried n = 50.

Even at these small sizes, we can see the S-shaped transition curves forming. The experimental thresholds are higher than ln(n)/n but that's expected for small n - the asymptotic behavior kicks in for larger graphs.

---

## Observations

A common observation is that all five properties become increasingly sharp as n grows. This follows the intuition that if we have more vertices, the properties become "forced" even at very low values of p. For example, at n = 500, having an edge is basically guaranteed at p = 0.02 even though the threshold is way lower.

Another interesting observation is the hierarchy of thresholds. As we increase p from 0, a random graph:
1. First gains its first edge (p* ~ 1/n²)
2. Then triangles appear (p* ~ 1/n)
3. Then it becomes connected (p* ~ ln(n)/n)
4. Around the same time, Hamilton cycles become likely
5. Finally K₄ subgraphs appear (p* ~ n^(-2/3)) at moderate n

It's like watching a graph grow up. First it gets its first connection, then it starts forming friend groups (triangles), then the whole social network becomes connected, and eventually you get these tightly-knit cliques forming.

The Hamilton cycle threshold being the same as connectivity is kind of poetic - once everyone's connected, you can visit everyone exactly once and come back home. Very wholesome graph theory content.

---

## Specifics on Methodology

### The Pipeline

The whole experiment works like this:

```
C++ experiment → outputs CSV → Python visualization with matplotlib
```

### C++ Side

I wrote methods to test each property on random graphs:
- `generateRandomGraph(n, p)` - generates G(n,p) using adjacency list
- `generateRandomMatrix(n, p)` - generates G(n,p) using adjacency matrix
- `hasEdge()` - O(n) linear scan
- `hasK3()` - O(n³) brute force over all triplets
- `isConnected()` - O(n+m) DFS
- `hasK4()` - O(n⁴) brute force over all 4-tuples
- `isHamiltonian()` - O(n!) backtracking (pain)

For each (n, p) pair, I ran 500 Monte Carlo trials and recorded what fraction of graphs had each property. The probability p ranged from 0 to 1 in steps of 0.02.

### Python Side

Used matplotlib to generate the plots. Nothing fancy, just plotting probability vs p for different values of n.

### Limitations

- `hasK3`: practical for n ≤ 1000 (billion operations territory)
- `hasK4`: practical for n ≤ 200 (n⁴ gets ugly fast)
- `isHamiltonian`: practical for n ≤ 20 (NP-complete problems hit different)
- `isConnected`: could handle n ≤ 100,000 easily

### Challenges

I don't have much experience with the random library in C++ so I had to do some digging. The mt19937 Mersenne Twister and uniform_real_distribution took some getting used to.

Another challenge was implementing hasK3 and hasK4. With an adjacency matrix you just iterate over triplets/quadruples and look up edges in O(1). The trade-off is O(n²) memory but for the sizes I was testing that was fine. Using adjacency lists would require iterating through neighborhoods which seemed annoying to code and slower anyway.

### All code is provided in the github repository

---

## Summary Table

| Property | Threshold p*(n) | Naive Constant | Algorithm | Max n Tested |
|----------|-----------------|----------------|-----------|--------------|
| Has Edge | 2/n² | c = 2 | O(n) | 500 |
| Has K₃ | 1/n | c ≈ 1.82 | O(n³) | 200 |
| Connected | ln(n)/n | c = 1 | O(n+m) | 200 |
| Has K₄ | n^(-2/3) | c ≈ 1.70 | O(n⁴) | 100 |
| Hamiltonian | ln(n)/n | c = 1 | O(n!) | 15 |

---

## Conclusion

The threshold effect is real and it's spectacular. Random graphs really do exhibit these sharp phase transitions where properties go from "almost never" to "almost always" over a narrow range of p. The experimental results line up pretty well with the theoretical predictions, especially for larger n where the asymptotic behavior kicks in.

The coolest part is how the thresholds form this hierarchy - edges first, then triangles, then connectivity, then bigger cliques. It's like watching order emerge from randomness, which is basically what Erdős and Rényi figured out back in 1959. Pretty cool that we can verify their theorems with some C++ and matplotlib.

If I had more time (and a better computer), I'd test larger values of n for the Hamilton cycle property. But that would require either a smarter algorithm or accepting that my laptop might become a space heater.
