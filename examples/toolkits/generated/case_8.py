#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 51.212

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''A 51-year-old lady presented to our emergency department because of generalized body ache and marked weakness in both lower extremities for two days d...'''


step01 = ideal_body_weight.ibw_explanation({'height': (65, 'in'), 'sex': 'Female', 'age': 51})

step02 = adjusted_body_weight.abw_explanation({'weight': (79, 'kg'), 'height': (65, 'in'), 'sex': 'Female', 'age': 51})

step03 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (65.8, 'kg'), 'height': (65, 'in'), 'sex': 'Female', 'creatinine': (1.35, 'mg/dL'), 'age': (51, 'years')})

# 打印最终结果
result = step03
print(result)
