# Is Connected

Let X = the number of isolated vertices in $G \in G(n, p)$
then $X = \sum_{i} A_i$
where $A_i = 1$ if vertex i is isolated (has no edges), 0 otherwise

$P(A_i = 1) = (1 - p)^{n-1}$ (no edge to any of the other n-1 vertices)
so by linearity $E(X) = n * (1 - p)^{n-1}$

We use the threshold $p^* = \frac{ln(n)}{n}$ and write $p = \frac{\lambda * ln(n)}{n}$

## Lower Bound (for connectivity):
if $\lambda > 1$ then P(connected) $\to 1$

this means P(isolated vertex exists) $\to 0$

using the inequality $(1 - p) \leq e^{-p}$ we get
$E(X) = n(1-p)^{n-1} \leq n * e^{-p(n-1)}$

substitute $p = \frac{\lambda * ln(n)}{n}$:
$E(X) \leq n * e^{-\lambda * ln(n) * (n-1)/n}$
$\approx n * e^{-\lambda * ln(n)}$
$= n * n^{-\lambda}$
$= n^{1 - \lambda}$

since $\lambda > 1$, we have $1 - \lambda < 0$
so $E(X) \leq n^{1-\lambda} \to 0$ as $n \to \infty$

Now we apply Markov with t = 1
$P(X \geq 1) \leq E(X) \to 0$

thus P(isolated vertex exists) $\to 0$, so P(connected) $\to 1$

## Upper Bound (for connectivity):
if $\lambda < 1$ then P(connected) $\to 0$

this means P(isolated vertex exists) $\to 1$

we need to show $E(X) \to \infty$ and $\frac{Var(X)}{E(X)^2} \to 0$

using the inequality $(1 - p) \geq e^{-(1+\delta)p}$ for small p and any $\delta > 0$:
$E(X) = n(1-p)^{n-1} \geq \frac{n * e^{-(1+\delta)p(n-1)}}{1-p}$

substitute $p = \frac{\lambda * ln(n)}{n}$:
$E(X) \geq \frac{n * e^{-(1+\delta)\lambda * ln(n)}}{1-p}$
$= \frac{n * n^{-(1+\delta)\lambda}}{1-p}$
$= \frac{n^{1 - (1+\delta)\lambda}}{1-p}$

since $\lambda < 1$, we can pick $\delta$ small enough that $(1+\delta)\lambda < 1$
so $1 - (1+\delta)\lambda > 0$ and $E(X) \to \infty$

Now we compute Var(X). For two different vertices i and j:
- $P(A_i) = (1-p)^{n-1}$
- $P(A_j | A_i) = (1-p)^{n-2}$ (the non-edge between i,j is already known)

so $P(A_j | A_i) - P(A_j) = (1-p)^{n-2} - (1-p)^{n-1} = (1-p)^{n-2} * p$

$Var(X) = \sum_i P(A_i)(1 - P(A_i)) + \sum_{i \neq j} P(A_i)(P(A_j|A_i) - P(A_j))$
$\leq n(1-p)^{n-1} + n(n-1)(1-p)^{n-1}(1-p)^{n-2} * p$
$= E(X) + n^2(1-p)^{2n-3} * p$

this simplifies to (from class notes):
$Var(X) \leq E(X) + E(X)^2 * \frac{p}{1-p}$

now we plug into the Chebyshev ratio:
$\frac{Var(X)}{E(X)^2} \leq \frac{1}{E(X)} + \frac{p}{1-p}$

- first term: $\frac{1}{E(X)} \to 0$ since $E(X) \to \infty$
- second term: $\frac{p}{1-p} = \frac{\lambda ln(n)/n}{1 - \lambda ln(n)/n} \to 0$

Finally apply Chebyshev's inequality to get
$P(X = 0) \leq \frac{Var(X)}{E(X)^2} \to 0$

therefore P(isolated vertex exists) = P(X >= 1) = 1 - P(X = 0) $\to 1$
so P(connected) $\to 0$
