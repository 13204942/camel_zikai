#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 17.406

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''A 43-years-old Caucasian male (height 198 cm, weight 115 kg, tobacco smoker – 1 packet of cigarettes/day) was admitted to the intensive care unit (ICU...'''


step01 = bmi_calculator.bmi_calculator_explanation({'weight': (115, 'kg'), 'height': (198, 'cm')})

step02 = ideal_body_weight.ibw_explanation({'height': (198, 'cm'), 'sex': 'Male', 'age': 43})

step03 = adjusted_body_weight.abw_explanation({'weight': (115, 'kg'), 'height': (198, 'cm'), 'sex': 'Male', 'age': 43})

step04 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (100.775, 'kg'), 'height': (198, 'cm'), 'sex': 'Male', 'creatinine': (691.6, 'µmol/L'), 'age': (43, 'years')})

# 打印最终结果
result = step04
print(result)
