# ckd_epi_2021_creatinine function call:
from camel.toolkits.medcalc_bench.ckd_epi_2021_creatinine import ckd_epi_2021_explanation

# reall for parms
input_variables = {
    "sex": 'Female',       # sex
    "age": (63, 'years'),  # age
    "creatinine": (6.46, 'mg/dL'),  # creatinine
}

# call function
result = ckd_epi_2021_explanation(input_variables)

# return result
print(result)