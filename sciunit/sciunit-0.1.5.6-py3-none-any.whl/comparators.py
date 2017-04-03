from .scores import BooleanScore,RatioScore,ZScore,FloatScore
from .utils import assert_dimensionless

"""
Each 'compute' function takes and observation and a prediction
and returns a score.
"""

def compute_equality(observation,prediction):
    """
    Computes whether the observation and prediction are equal.
    """
    value = observation==prediction
    return BooleanScore(value)


def compute_ratio(observation, prediction):
    """
    Computes a ratio from an observation and a prediction.
    """
    m_value = prediction['value']
    r_mean = observation['mean']
    
    value = (m_value+0.0)/r_mean
    return RatioScore(value)


def compute_ssd(observation, prediction):
    """
    Computes a sum-squared difference from an observation and a prediction.
    """
    value = sum((observation - prediction)**2) # The sum of the 
                                               # squared differences.
    return FloatScore(value)
        

