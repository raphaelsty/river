import math

from .. import stats

from . import base


__all__ = ['Gaussian']


class Gaussian(base.ContinuousDistribution):
    """Normal distribution with parameters mu and sigma.

    Example:

        ::

            >>> from creme import proba

            >>> p = proba.Gaussian().update(6)
            >>> p.mode
            6.0

            >>> p.update(7).mode
            6.5

            >>> p
            𝒩(μ=6.500, σ=0.707)

            >>> p.query(6.5)
            0.564189...

    """

    def __init__(self):
        self.variance = stats.Var()

    @property
    def mu(self):
        return self.variance.mean.get()

    @property
    def sigma(self):
        return self.variance.get() ** 0.5

    def __str__(self):
        return f'𝒩(μ={self.mu:.3f}, σ={self.sigma:.3f})'

    def update(self, x):
        self.variance.update(x)
        return self

    def pdf(self, x):
        var = self.variance.get()
        if var:
            return math.exp((x - self.mu) ** 2 / (-2 * var)) / math.sqrt(math.tau * var)
        return 0.

    def cdf(self, x):
        try:
            return 0.5 * (1. + math.erf((x - self.mu) / (self.sigma * math.sqrt(2.))))
        except ZeroDivisionError:
            return 0.
