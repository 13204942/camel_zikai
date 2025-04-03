#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 33.034

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''A 34-year-old man was admitted for evaluation of worsening pedal edema. He was apparently healthy until four years back, when he developed edema of bo...'''


step01 = bmi_calculator.bmi_calculator_explanation({'weight': (74, 'kg'), 'height': (174, 'cm')})

step02 = ideal_body_weight.ibw_explanation({'height': (174, 'cm'), 'sex': 'Male', 'age': 34})

step03 = adjusted_body_weight.abw_explanation({'weight': (74, 'kg'), 'height': (174, 'cm'), 'sex': 'Male', 'age': 34})

step04 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (71.335, 'kg'), 'height': (174, 'cm'), 'sex': 'Male', 'creatinine': (3.1, 'mg/dL'), 'age': (34, 'years')})

# 打印最终结果
result = step04
print(result)
