from collections import defaultdict

salaries_and_tenures = [(83000, 8.7), (88000, 8.1), (48000, 0.7), 
                        (76000, 6), (69000, 6.5), (76000, 7.5), 
                        (60000, 2.5), (83000, 10), (48000, 1.9), (63000, 4.2)]

#Key: years, Value: list of the salaries for each tenure
salary_by_tenure = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)
#Key: years, Value: average salary for that tenure
average_salary_by_tenure = {
    tenure : sum(salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}
print(average_salary_by_tenure)
def tenure_bucket(tenure):
    if tenure < 2:
        return "less than two"
    elif tenure < 5:
        return "between two and five"
    else:
        return "more than five"
#Key: tenure bucket, Value: list of salaries for that bucket
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)
#Key: tenure bucket, Value: average salary for that bucket
average_salary_by_bucket = {
    tenure_bucket : sum(salaries) / len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.items()
}
print(average_salary_by_bucket)
#Output is: {'more than five': 79166.66666666667, 'between two and five': 61500.0, 'less than two': 48000.0}
def predict_paid_or_unpaid(years_experience):
    if years_experience < 3.0:
        return "paid"
    elif years_experience < 8.5:
        return "unpaid"
    else:
        return "paid"