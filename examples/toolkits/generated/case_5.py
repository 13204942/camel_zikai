#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 33.001

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''This is a 61-year-old woman who presented with diabetic symptoms and was misclassified as having type 1 diabetes with negative autoimmune-related type...'''


step01 = adjusted_body_weight.abw_explanation({'weight': (46, 'kg'), 'height': (154, 'cm'), 'sex': 'Female', 'age': 61})

step02 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (46.569, 'kg'), 'height': (154, 'cm'), 'sex': 'Female', 'creatinine': (1.3, 'mg/dL'), 'age': (61, 'years')})

# 打印最终结果
result = step02
print(result)
