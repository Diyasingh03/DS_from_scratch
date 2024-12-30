from typing import Tuple
import math

def normal_approximation_to_binomial(n: int, p: float) -> Tuple[float, float]:
    #returning mu and sigma corr. to Bin(n,p)
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma

from scratch.Probability import normal_cdf, inverse_normal_cdf
# normal_cdf is the prob the var is below the threshold
normal_probability_below = normal_cdf
def normal_probability_above(lo: float, mu: float = 0, sigma: float = 1) -> float:
    return 1 - normal_cdf(lo, mu, sigma)


#it's between if it's less than hi, but not less than lo
#The prob that an N(mu, sigma) is between lo and hi
def normal_probability_between(lo: float, hi: float, mu: float = 0, sigma: float = 1) -> float:
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)

#it's outside if it's not between
def normal_probability_outside(lo: float, hi: float, mu: float = 0, sigma: float = 1) -> float:
    return 1 - normal_probability_between(lo, hi, mu, sigma)

def normal_upper_bound(probability: float, mu: float = 0, sigma: float = 1) -> float:
    #returns the z for which P(Z <= z) = probability
    return inverse_normal_cdf(probability, mu, sigma)
def normal_lower_bound(probability: float, mu: float = 0, sigma: float = 1) -> float:
    #returns the z for which P(Z >= z) = probability
    return inverse_normal_cdf(1 - probability, mu, sigma)
def normal_two_sided_bounds(probability: float, mu: float = 0, sigma: float = 1) -> Tuple[float, float]:
    #returns the symmetric bounds about the mean that contain the specified probability
    tail_probability = (1 - probability) / 2
    #upper bound should have tail_probability above it
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)
    #lower bound should have tail_probability below it
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)
    return lower_bound, upper_bound
mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)

assert mu_0 == 500
assert 15.8 < sigma_0 < 15.9

lower_bound, upper_bound = normal_two_sided_bounds(0.95, mu_0, sigma_0)
# print(lower_bound,",", upper_bound)
#95% bounds based on assumption p is 0.5
lo,hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)

#type 2 error means we fail to reject the null hypothesis happens when X is still in our original interval
type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
power = 1 - type_2_probability

assert 0.886 < power < 0.888

hi = normal_upper_bound(0.95, mu_0, sigma_0) # 526 (< 531, since we need more probability in the upper tail)
type_2_probability = normal_probability_below(hi, mu_1, sigma_1)
power = 1 - type_2_probability # 0.936

assert 526 < hi < 526.1
assert 0.9363 < power < 0.9364
#p-values
def two_sided_p_value(x: float, mu: float = 0, sigma:float=1) -> float:
    if x >= mu:
        #if x is greater than the mean, the tail is everything greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        #if x is less than the mean, the tail is what's less than x
        return 2 * normal_probability_below(x, mu, sigma)
#example 530 heads
tpsv = two_sided_p_value(529.5, mu_0, sigma_0) # 0.062
print(tpsv)
#used 529.5 because of continuity correction

import random
extreme_value_count = 0
for _ in range(1000):
    #count the number of heads in 1000 flips and count how often there are "extreme" results
    num_heads = sum(1 if random.random() < 0.5 else 0 for _ in range(1000))
    if num_heads >= 530 or num_heads <= 470:
        extreme_value_count += 1
# assert 59 < extreme_value_count < 65, f"{extreme_value_count}" #p-value was 0.062 so 62 times out of 1000
tpsv = two_sided_p_value(531.5, mu_0, sigma_0) # 0.0463 which is less than 0.05 so we reject the null hypothesis
assert 0.0463 < tpsv < 0.0464
upper_p_value = normal_probability_above
lower_p_value = normal_probability_below
upper_p_value(524.5, mu_0, sigma_0) # 0.061 not rejecting the null hypothesis
upper_p_value(526.5, mu_0, sigma_0) # 0.047 rejecting the null hypothesis

#Confidence Intervals
p_hat = 525 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)
normal_two_sided_bounds(0.95, mu, sigma) # (0.4940, 0.5560)
#if we were to repeat the experiment many times, 95% of the time the interval would contain the true p
# we do not conclude the coin is unfair because 0.5 is in the interval
# if we had seen 540 heads, the 95% confidence interval would be (0.5091, 0.5709)
p_hat = 540 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)
normal_two_sided_bounds(0.95, mu, sigma) # (0.5091, 0.5709)

#P-hacking
# rejects the null hypothesis 5% of the time
from typing import List
def run_experiment() -> List[bool]:
    #flips a fair coin 1000 times, True = heads, False = tails
    return [random.random() < 0.5 for _ in range(1000)]
def reject_fairness(experiment: List[bool]) -> bool:
    #using the 5% significance levels
    num_heads = len([flip for flip in experiment if flip])
    return num_heads < 469 or num_heads > 531
random.seed(0)
experiments = [run_experiment() for _ in range(1000)]
num_rejections = len([experiment for experiment in experiments if reject_fairness(experiment)])
assert num_rejections == 46

#A/B Testing
def estimated_parameters(N: int, n: int) -> Tuple[float, float]:
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma

def a_b_test_statistic(N_A: int, n_A: int, N_B: int, n_B: int) -> float:
    p_A, sigma_A = estimated_parameters(N_A, n_A)
    p_B, sigma_B = estimated_parameters(N_B, n_B)
    return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigma_B ** 2)
z = a_b_test_statistic(1000, 200, 1000, 180) # -1.14
assert -1.15 < z < -1.13
tpsv = two_sided_p_value(z) # 0.254
assert 0.253 < tpsv < 0.255
z = a_b_test_statistic(1000, 200, 1000, 150) # -2.94
tpsv = two_sided_p_value(z) # 0.003
assert 0.0027 < tpsv < 0.004

#Bayesian Inference
def B(alpha: float, beta: float) -> float:
    #a normalizing constant so the total probability is 1
    return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
def beta_pdf(x: float, alpha: float, beta: float) -> float:
    if x <= 0 or x >= 1: #no weight outside [0, 1]
        return 0
    return x ** (alpha - 1) * (1 - x) ** (beta - 1) / B(alpha, beta)

import matplotlib.pyplot as plt
xs = [x / 100 for x in range(100)]
plt.plot(xs, [beta_pdf(x, 1, 1) for x in xs], '-', label='Beta(1,1)')
plt.plot(xs, [beta_pdf(x, 10, 10) for x in xs], '--', label='Beta(10,10)')
plt.plot(xs, [beta_pdf(x, 4, 16) for x in xs], ':', label='Beta(4,16)')
plt.plot(xs, [beta_pdf(x, 16, 4) for x in xs], '-.', label='Beta(16,4)')
plt.legend()
plt.title("Various Beta pdfs")
plt.show()
# plt.savefig('im/various_beta_pdfs.png')
# plt.gca().clear()
# plt.close()

xs = [x / 100 for x in range(100)]
plt.plot(xs, [beta_pdf(x, 4, 8) for x in xs], '-', label='Beta(4,8)')
plt.plot(xs, [beta_pdf(x, 23, 27) for x in xs], '--', label='Beta(23,27)')
plt.plot(xs, [beta_pdf(x, 33, 17) for x in xs], ':', label='Beta(33,17)')

plt.legend()
plt.title("Various Beta pdfs")
plt.show()
# plt.savefig('im/various_beta_pdfs2.png')