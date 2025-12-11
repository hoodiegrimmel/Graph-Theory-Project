# Has Edge

Let X = the number of edges in $G \in G(n, p)$
then $X = \sum_{i < j} A_{i,j}$ 
where $A_{i,j} = 1$ if edge (i,j) exists, 0 otherwise

the number of possible edges is n choose 2 which is $\frac{n(n - 1)}{2}$ 
$P(A_{i,j} = 1) = p$ for each edge
so by linearity $E(X) = \frac{n(n - 1)}{2} *p = \frac{n(n - 1)p}{2}$  

## Lower Bound:
if $p \ll \frac{1}{n^2}$ then P(has edge) $\to 0$

substitute $p = \frac{c}{n^3}$ then we get
$E(X) = \frac{n(n - 1)}{(2n^3)} * c = \frac{c(n - 1)}{(2n^2)} \to 0$  as $n \to \infty$ 

Now we apply Markov with t = 1
$P(X \geq 1) \leq E(X) \to 0$ 

thus P(has edge) $\to 0$ 

## Upper Bound:
if $p \gg \frac{1}{n^2}$ then P(has edge) $\to 1$ 
because edges are independent, the variance is just
n choose 2 * p(1 - p)

Substitute $p = c \cdot \frac{\ln n}{n^2}$ so  
$E(X) \approx \frac{c \cdot \ln n}{2}.$
now we plug this into the Chebyshev ratio.

$\frac{Var(X)}{E(X)^2} = \frac{n(n - 1)p(1-p)/2}{[n(n - 1)p/2]^2}$
$= \frac{(1 - p)}{n(n - 1)p/2}$
$= \frac{2(1 - p)}{n(n-1)p}$
$\approx \frac{2}{n^2 * p}$ for small values of p
$= \frac{2}{c * ln(n)} \to 0$

Finally apply Chebyshev's inequality to get
$P(X = 0) \leq \frac{Var(X)}{E(X)^2} \to 0$ 

therefore P(has edge) = P(X >= 1) = 1 - P(X = 0) $\to 1$
