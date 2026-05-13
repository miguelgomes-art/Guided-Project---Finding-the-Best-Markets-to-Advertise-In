"""
Guided Project: Finding the Best Markets to Advertise In

The purpose of this project is to identify the two most suitable markets that will advertise our services in the future.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

survey = pd.read_csv('2017-fCC-New-Coders-Survey-Data.csv', low_memory = False)
survey.head()
survey.shape

"""
In this project we will use an existing data filled by new coders that matches with our analyses.

## Checking for Sample Representativity
Most of the courses we offer are on web and mobile development, but we also cover many other domains, like data science, game development, etc. For the purpose of our analysis, we want to answer questions about a population of new coders that are interested in the subjects we teach. We'd like to know:

Where are these new coders located.

What are the locations with the greatest number of new coders.

How much money new coders are willing to spend on learning."""

survey['JobRoleInterest'].value_counts(normalize = True) * 100

job_role = survey['JobRoleInterest'].dropna()
job_role.head()

splitted_job_role = job_role.str.split(',')
splitted_job_role

n_of_options = splitted_job_role.apply(lambda x: len(x))
n_of_options.value_counts(normalize = True).sort_index() * 100

"""
Most students know exactly what they want to learn, but about 68 percent have ambiguous ideas or plans."""
job_role_dict = {}
def job_role(array):
    
    for roles in array:
        for role in roles:
            role = role.strip().upper()
            if role in job_role_dict:
                job_role_dict[role] += 1
            else:
                job_role_dict[role] = 1
    return job_role_dict
job_role(splitted_job_role)

def filter_and_sort_dict(input_dict, x):
    # Filter values greater than x
    filtered = {k: v for k, v in input_dict.items() if v >= x}
    
    # Sort by values (ascending)
    sorted_dict = dict(sorted(filtered.items(), key=lambda item: item[1]))
    
    return sorted_dict

top_roles = filter_and_sort_dict(job_role_dict, 1000)

plt.barh(list(top_roles.keys()), list(top_roles.values()))
plt.show()

plt.pie(top_roles.values(), labels = top_roles.keys(), autopct = '%1.1f%%', startangle = 140)
plt.show()

"""The graph indicates that the three most sought‑after profiles are Full‑Stack Web Developer, Front‑End Developer, and Back‑End Developer, in that order. The next most in‑demand role is Mobile Developer. Together, these four profiles account for nearly 64% of the total.

## New Coders - Locations and Densities
"""
countries = survey['CountryLive'].unique()
survey_filtered = survey[survey['JobRoleInterest'].notnull()].copy()

absolute_frequencies = survey_filtered['CountryLive'].value_counts()
relative_frequencies = survey_filtered['CountryLive'].value_counts(normalize=True)*100

frequencies = pd.DataFrame({'count': absolute_frequencies, 'proportion': relative_frequencies})

frequencies.head()

"""The top five countries with the highest share of potential customers are the United States, India, the United Kingdom, Canada and Poland with 45.7, 7.7, 4.6, 3.8 and 1.9 percent respectively.

## Spending Money for Learning
"""
survey_filtered_country = survey_filtered[survey_filtered['CountryLive'].notnull()]
survey_filtered_country = survey_filtered_country[survey_filtered_country['CountryLive'].isin(['United States of America', 'India', 'United Kingdom', 'Canada'])]
survey_filtered_country['MonthsProgramming'] = survey_filtered_country['MonthsProgramming'].replace(0, 1)

survey_filtered_country['spent_per_month'] = survey_filtered_country['MoneyForLearning']/survey_filtered_country['MonthsProgramming']
survey_filtered_country = survey_filtered_country[survey_filtered_country['spent_per_month'].notnull()]

spent_mean_4 = survey_filtered_country.groupby('CountryLive').mean(numeric_only=-True)
spent_mean_4['spent_per_month']

"""
## Dealing with Extreme Outliers
The results for the United Kingdom and Canada appear unexpectedly low when compared with the values observed for India. Based on socio‑economic indicators such as GDP per capita, one might anticipate that individuals in the UK and Canada would invest more in learning than those in India.

Several factors could explain this discrepancy. It’s possible that the dataset for these three countries is not fully representative, leading to skewed averages. Outliers—perhaps due to inaccurate or unintentional survey responses—may also be inflating the mean for India or suppressing it for the UK and Canada. Alternatively, the findings may simply reflect genuine differences in spending behaviour."""
sns.boxplot(x='spent_per_month', y='CountryLive', data= survey_filtered_country)
plt.title('Money Spent per month per Country \n(Distributions)')
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.show()

"""As we can see in the US has two outliers and we will drop them to prevent wrong calculations."""

survey_filtered_country = survey_filtered_country[survey_filtered_country['spent_per_month']<20000]
spent_mean_4 = survey_filtered_country.groupby('CountryLive').mean(numeric_only=-True)
spent_mean_4['spent_per_month']

sns.boxplot(x='spent_per_month', y='CountryLive', data = survey_filtered_country)
plt.title('Money Spent Per Month Per Country\n(Distributions)')
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.show()

"""As we can see, we still have outliers in the US, India, and Canada. This time, we'll drop the outliers individually for each country to avoid losing information."""

survey_filtered_country = survey_filtered_country.drop(survey_filtered_country[
    (survey_filtered_country['CountryLive'] == 'India') & 
    (survey_filtered_country['spent_per_month'] >= 2500)].index)

survey_filtered_country = survey_filtered_country.drop(survey_filtered_country[
    (survey_filtered_country['CountryLive'] == 'United States of America') & 
    (survey_filtered_country['spent_per_month'] >= 6000)].index)

survey_filtered_country = survey_filtered_country.drop(survey_filtered_country[
    (survey_filtered_country['CountryLive'] == 'Canada') & 
    (survey_filtered_country['spent_per_month'] >= 2500)].index)

spent_mean_4 = survey_filtered_country.groupby('CountryLive').mean(numeric_only=-True)
spent_mean_4['spent_per_month']

sns.boxplot(x='spent_per_month', y='CountryLive', data = survey_filtered_country)
plt.title('Money Spent Per Month Per Country\n(Distributions)')
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.show()

"""Although the United Kingdom and Canada have greater purchasing power (e.g., GDP per capita), the data show that monthly spending on education is lower or less varied than in India or the United States. This may indicate:

    Lack of representativeness in the sample

    Outliers that distort the average

    Real differences in education investment habits"""
