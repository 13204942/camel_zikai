#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 84.025

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''A 67-year-old Japanese woman underwent OWHTO to treat SPONK that had occurred in the left medial femoral condyle (Fig. ). The patient reported the fol...'''


step01 = ideal_body_weight.ibw_explanation({'height': (157, 'cm'), 'sex': 'Female', 'age': 67})

step02 = adjusted_body_weight.abw_explanation({'weight': (62, 'kg'), 'height': (157, 'cm'), 'sex': 'Female', 'age': 67})

step03 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (54.599, 'kg'), 'height': (157, 'cm'), 'sex': 'Female', 'creatinine': (0.56, 'mg/dL'), 'age': (67, 'years')})

# 打印最终结果
result = step03
print(result)
