"""Formuły analityczne dla M/M/1 i M/M/s (Erlang C)."""
import math

def _fact(n: int) -> int:
    return math.factorial(n)

def mm1(lambda_rate: float, mu: float) -> dict:
    rho = lambda_rate / mu
    if rho >= 1:
        raise ValueError("Układ niestabilny (rho >= 1).")
    Wq = rho / (mu - lambda_rate)
    Ws = 1 / (mu - lambda_rate)
    Lq = lambda_rate * Wq
    Ls = lambda_rate * Ws
    return dict(rho=rho, Wq=Wq, Ws=Ws, Lq=Lq, Ls=Ls)

def mms(lambda_rate: float, mu: float, s: int) -> dict:
    if s < 1:
        raise ValueError("s >= 1")
    rho = lambda_rate / (s * mu)
    if rho >= 1:
        raise ValueError("Układ niestabilny (rho >= 1).")
    a = lambda_rate / mu
    summation = sum(a**k / _fact(k) for k in range(s))
    last_term = a**s / (_fact(s) * (1 - rho))
    P0 = 1 / (summation + last_term)
    Pw = last_term * P0
    Wq = Pw / (s * mu * (1 - rho))
    Ws = Wq + 1/mu
    Lq = lambda_rate * Wq
    Ls = lambda_rate * Ws
    return dict(rho=rho, Pw=Pw, Wq=Wq, Ws=Ws, Lq=Lq, Ls=Ls)
