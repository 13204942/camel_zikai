#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算: Creatinine Clearance (Cockcroft-Gault Equation)
# 最终答案: 21.467

from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance

# 用户消息摘要:
'''In 2008, a 59-year-old Japanese woman was admitted for evaluation of renal disease. RA had been diagnosed at another hospital in 1972 when she present...'''


step01 = bmi_calculator.bmi_calculator_explanation({'weight': (44.0, 'kg'), 'height': (154.2, 'cm')})

step02 = ideal_body_weight.ibw_explanation({'height': (154.2, 'cm'), 'sex': 'Female', 'age': 59})

step03 = creatinine_clearance.generate_cockcroft_gault_explanation({'weight': (44.0, 'kg'), 'height': (154.2, 'cm'), 'sex': 'Female', 'creatinine': (4.2, 'mg/dL'), 'age': (59, 'years')})

# 打印最终结果
result = step03
print(result)
