#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 67.005

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''A 53-year old man (height, 175 cm; weight, 87 kg) was scheduled to undergo subtotal stomach-preserving pancreatoduodenectomy with portal vein reconstr...'''


step01 = bmi_calculator.bmi_calculator_explanation({'weight': (87, 'kg'), 'height': (175, 'cm')})

step02 = ideal_body_weight.ibw_explanation({'height': (175, 'cm'), 'sex': 'Male', 'age': 53})

step03 = adjusted_body_weight.abw_explanation({'weight': (87, 'kg'), 'height': (175, 'cm'), 'sex': 'Male', 'age': 53})

step04 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (77.079, 'kg'), 'height': (175, 'cm'), 'sex': 'Male', 'creatinine': (1.39, 'mg/dL'), 'age': (53, 'years')})

# 打印最终结果
result = step04
print(result)
