#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 79.333

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''A 56-year-old man was admitted to the renal unit of the tertiary university hospital with symptoms of polyuria with nocturia, and polydipsia with seve...'''


step01 = bmi_calculator.bmi_calculator_explanation({'weight': (68, 'kg'), 'height': (176, 'cm')})

step02 = ideal_body_weight.ibw_explanation({'height': (176, 'cm'), 'sex': 'Male', 'age': 56})

step03 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (68, 'kg'), 'height': (176, 'cm'), 'sex': 'Male', 'creatinine': (1.0, 'mg/dL'), 'age': (56, 'years')})

# 打印最终结果
result = step03
print(result)
