#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 70.556

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''A 65-year-old female consulted our office for naturopathic primary-care support for a myriad of conditions, which included diabetes with weight gain, ...'''


step01 = adjusted_body_weight.abw_explanation({'weight': (195.0, 'lb'), 'height': (66.5, 'in'), 'sex': 'Female', 'age': 65})

step02 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (114.27, 'kg'), 'height': (170, 'cm'), 'sex': 'Female', 'creatinine': (79, 'µmol/L'), 'age': (65, 'years')})

# 打印最终结果
result = step02
print(result)
