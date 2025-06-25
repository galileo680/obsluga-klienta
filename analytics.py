"""Testy statystyczne i regresja OLS."""
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf

def ttest(sample1, sample2, equal_var=False):
    stat, p = st.ttest_ind(sample1, sample2, equal_var=equal_var)
    return dict(t=stat, p_value=p)

def mannwhitney(sample1, sample2):
    stat, p = st.mannwhitneyu(sample1, sample2, alternative='two-sided')
    return dict(U=stat, p_value=p)

def regression(formula: str, df: pd.DataFrame):
    model = smf.ols(formula, data=df).fit()
    return model
