# Has Triangle (K₃)

Let X = the number of triangles in $G \in G(n, p)$
then $X = \sum_{\{u,v,w\}} A_{u,v,w}$ 
where $A_{u,v,w} = 1$ if vertices $\{u,v,w\}$ form a triangle, 0 otherwise

the number of possible triangles is n choose 3 which is $\frac{n(n-1)(n-2)}{6} \approx \frac{n^3}{6}$
$P(A_{u,v,w} = 1) = p^3$ (need all 3 edges)
so by linearity $E(X) = \binom{n}{3} * p^3 \approx \frac{n^3 p^3}{6}$

## Lower Bound:
if $p \ll \frac{1}{n}$ then P(has triangle) $\to 0$

substitute $p = \frac{c}{n^{1+\epsilon}}$ for some $\epsilon > 0$ then we get
$E(X) = \frac{n^3}{6} * \frac{c^3}{n^{3 + 3\epsilon}} = \frac{c^3}{6n^{3\epsilon}} \to 0$ as $n \to \infty$

Now we apply Markov with t = 1
$P(X \geq 1) \leq E(X) \to 0$

thus P(has triangle) $\to 0$

## Upper Bound:
if $p \gg \frac{1}{n}$ then P(has triangle) $\to 1$

substitute $p = c * n^{-1 + \epsilon}$ for some $\epsilon > 0$
then $E(X) = \frac{n^3}{6} * c^3 * n^{-3 + 3\epsilon} = \frac{c^3 n^{3\epsilon}}{6} \to \infty$

Now we compute Var(X). Two triangles can overlap in:
- 3 vertices (same triangle): contributes $E(X)(1 - p^3)$
- 2 vertices (share 1 edge): $P(A_2 | A_1) = p^2$ since 1 edge is free
  - number of such pairs: $\binom{n}{3} * 3 * (n-3) = O(n^4)$
  - contributes $O(n^4) * p^3 * (p^2 - p^3) = O(n^4 p^5)$
- 1 vertex (share 0 edges): independent, contributes 0
- 0 vertices: independent, contributes 0

so $Var(X) \leq E(X) + O(n^4 p^5)$

now we plug into the Chebyshev ratio:
$\frac{Var(X)}{E(X)^2} \leq \frac{1}{E(X)} + \frac{O(n^4 p^5)}{(n^6 p^6 / 36)}$
$= \frac{1}{E(X)} + O\left(\frac{1}{n^2 p}\right)$

with $p = c * n^{-1 + \epsilon}$:
$\frac{1}{n^2 p} = \frac{1}{c * n^{1 + \epsilon}} \to 0$
$\frac{1}{E(X)} \to 0$ since $E(X) \to \infty$

Finally apply Chebyshev's inequality to get
$P(X = 0) \leq \frac{Var(X)}{E(X)^2} \to 0$

therefore P(has triangle) = P(X >= 1) = 1 - P(X = 0) $\to 1$
