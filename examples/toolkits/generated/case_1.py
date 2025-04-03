#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 141.042

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''A 16-year-old female adolescent was referred to our hospital with severe hypertension (systolic pressure 178 mmHg), which was first detected 7 months ...'''


step01 = bmi_calculator.bmi_calculator_explanation({'weight': (55, 'kg'), 'height': (162.8, 'cm')})

step02 = ideal_body_weight.ibw_explanation({'height': (162.8, 'cm'), 'sex': 'Female', 'age': 16})

step03 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (54.918, 'kg'), 'height': (162.8, 'cm'), 'sex': 'Female', 'creatinine': (0.57, 'mg/dL'), 'age': (16, 'years')})

# 打印最终结果
result = step03
print(result)
