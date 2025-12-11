# Has K₄

Let X = the number of K₄ subgraphs in $G \in G(n, p)$
then $X = \sum_{\{u,v,w,x\}} A_{u,v,w,x}$
where $A_{u,v,w,x} = 1$ if vertices $\{u,v,w,x\}$ form a K₄, 0 otherwise

the number of possible K₄ is n choose 4 which is $\frac{n(n-1)(n-2)(n-3)}{24} \approx \frac{n^4}{24}$
number of edges in K₄ is 4 choose 2 = 6
$P(A_{u,v,w,x} = 1) = p^6$ (need all 6 edges)
so by linearity $E(X) = \binom{n}{4} * p^6 \approx \frac{n^4 p^6}{24}$

## Lower Bound:
if $p \ll n^{-2/3}$ then P(has K₄) $\to 0$

substitute $p = c * n^{-2/3 - \epsilon}$ for some $\epsilon > 0$ then we get
$E(X) = \frac{n^4}{24} * c^6 * n^{-4 - 6\epsilon} = \frac{c^6}{24 n^{6\epsilon}} \to 0$ as $n \to \infty$

Now we apply Markov with t = 1
$P(X \geq 1) \leq E(X) \to 0$

thus P(has K₄) $\to 0$

## Upper Bound:
if $p \gg n^{-2/3}$ then P(has K₄) $\to 1$

substitute $p = c * n^{-2/3 + \epsilon}$ for some $\epsilon > 0$
then $E(X) = \frac{n^4}{24} * c^6 * n^{-4 + 6\epsilon} = \frac{c^6 n^{6\epsilon}}{24} \to \infty$

Now we compute Var(X). Two K₄'s can overlap in (from Example 7.6 in class):

| Overlap | Shared edges | $P(A_2 \| A_1)$ | Count | Contribution |
|---------|--------------|-----------------|-------|--------------|
| 4 vertices (same K₄) | 6 | 1 | $\binom{n}{4}$ | $\binom{n}{4} p^6 (1-p^6)$ |
| 3 vertices | 3 | $p^3$ | $\binom{5}{3}\binom{n}{5}$ | $O(n^5) p^6 (p^3 - p^6)$ |
| 2 vertices | 1 | $p^5$ | $\binom{4}{2}\binom{6}{2}\binom{n}{6}$ | $O(n^6) p^6 (p^5 - p^6)$ |
| 0-1 vertices | 0 | $p^6$ | — | 0 (independent) |

so from class notes:
$Var(X) = \binom{n}{4} p^6(1-p^6) + \binom{5}{3}\binom{n}{5} p^6(p^3 - p^6) + \binom{4}{2}\binom{6}{2}\binom{n}{6} p^6(p^5 - p^6)$

the dominant term is the 3-vertex overlap: $O(n^5 p^9)$

so $Var(X) \leq E(X) + O(n^5 p^9)$

now we plug into the Chebyshev ratio:
$\frac{Var(X)}{E(X)^2} \leq \frac{1}{E(X)} + \frac{O(n^5 p^9)}{(n^8 p^{12} / C)}$
$= \frac{1}{E(X)} + O\left(\frac{1}{n^3 p^3}\right)$

with $p = c * n^{-2/3 + \epsilon}$:
$n^3 p^3 = n^3 * c^3 * n^{-2 + 3\epsilon} = c^3 n^{1 + 3\epsilon} \to \infty$
so $\frac{1}{n^3 p^3} \to 0$
$\frac{1}{E(X)} \to 0$ since $E(X) \to \infty$

Finally apply Chebyshev's inequality to get
$P(X = 0) \leq \frac{Var(X)}{E(X)^2} \to 0$

therefore P(has K₄) = P(X >= 1) = 1 - P(X = 0) $\to 1$
