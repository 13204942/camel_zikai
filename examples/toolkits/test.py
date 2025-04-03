from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance


step01 = bmi_calculator.bmi_calculator_explanation({"weight": (55, "kg"), "height": (162.8, "cm")})

step02=ideal_body_weight.ibw_explanation({"height":(162.8,"cm"), "sex":"Female", "age":16})

result=creatinine_clearance.generate_cockcroft_gault_explanation({
    "weight": (54.918, "kg"),
    "height": (162.8, "cm"),
    "sex": "Female",
    "creatinine": (0.57, "mg/dL"),
    "age": (16, "years")
})
print(result)

   
   
    # {
    #     "usr_msg": "A 16-year-old female adolescent was referred to our hospital with severe hypertension (systolic pressure 178 mmHg), which was first detected 7 months prior to presentation during a routine annual physical examination. She complained of intermittent headache for about 1 year, and her previous blood pressure, measured 1 month prior to her detection of hypertension, had been normal. She showed mild hypokalemia (3.4 mmol/L) in a routine blood test, and an additional workup considering secondary hypertension was planned. Despite taking amlodipine (0.1 mg/kg twice a day), her blood pressure remained uncontrolled.\nUpon admission to our hospital, her systolic and diastolic blood pressures were 155 mmHg (>99th percentile) and 111 mmHg (>99th percentile) respectively. She was 162.8 cm tall (50th–75th percentile) and weighed 55 kg (50th–75th percentile). Physical examination including ophthalmological examination revealed no abnormality other than hypertension, and her family history was negative for hypertension or renal diseases. Laboratory examination revealed normal levels of hemoglobin (14.4 g/dL), serum creatinine (0.57 mg/dL), serum total cholesterol (144 mg/dL), and normal urinalysis. Serum sodium, potassium, chloride, and total carbon dioxide levels were 134 mmol/L, 3.4 mmol/L, 102 mmol/L, and 27 mmol/L, respectively. Plasma renin activity was 9.83 ng/mL/hr (normal, 0.5–3.3 ng/mL/hr), and serum aldosterone level was 77.3 ng/dL (normal, 4–48 ng/dL). Urinary levels of vanillylmandelic acid, epinephrine, norepinephrine, dopamine, metanephrine, and normetanephrine were normal, and plasma levels of epinephrine, norepinephrine, and dopamine were also normal. Chest radiography, electrocardiography, and echocardiography showed normal findings. Renal Doppler ultrasonography revealed an avascular bilobed cyst in the lower pole of the right kidney (). Abdominal computed tomography (CT) angiography showed bilaterally normal renal arteries and an eccentric soft tissue component at the peripheral aspect of the cystic lesion (). The mass remained unenhanced during the arterial phase, and its margin was indistinguishable from the surrounding tissue (). During the delayed phase, its eccentric capsule showed enhancement, and an intact mass could be observed (), consistent with CT findings of JGC tumors.\nA right partial nephrectomy was performed, and a clear resection margin was identified. The well-encapsulated mass measured 2.5 cm ×2.2 cm×2.0 cm in size with a partially cystic-appearing cut surface. Microscopic examination revealed sheets of polygonal tumor cells with amphophilic cytoplasm. Immunohistochemical examination showed that the tumor cells stained positive for CD34 and focally positive for CD117 (C-Kit) and smooth muscle actin. ()\nPostoperatively, her blood pressure returned to normal (105/63 mmHg) without using any antihypertensive medication. On the 3rd postoperative day, the plasma renin activity (0.52 ng/mL/hr), serum aldosterone (3.9 ng/dL), and serum potassium (3.6 mmol/L) levels returned to normal. Her blood pressure and laboratory findings remained within the reference range over the next 3 years postoperatively until her last follow-up. What is the patient's Creatinine Clearance using the Cockroft-Gault Equation in terms of mL/min? You should use the patient's adjusted body weight in kg instead of the patient's actual body weight if the patient is overweight or obese based on their BMI. If the patient's BMI's normal, set their adjusted body weight to the minimum of the ideal body and actual weight. If the patient is underweight, please set their adjusted body weight to their actual body weight.",
    #     "rationale": [
    #         {
    #             "tool_name": "bmi_calculator",
    #             "args": {
    #                 "weight_value": 55,
    #                 "weight_unit": "kg",
    #                 "height_value": 162.8,
    #                 "height_unit": "cm"
    #             },
    #             "result": "{\"rationale\": \"The formula for computing the patient's BMI is (weight)/(height * height), where weight is the patient's weight in kg and height is the patient's height in m.\\nThe patient's height is 162.8 cm, which is 162.8 cm * 1 m / 100 cm = 1.628 m. The patient's weight is 55.0 kg. The patient's bmi is therefore 55.0 kg / (1.628 m * 1.628 m) = 20.752 kg/m^2.\", \"final_answer\": \"20.752\"}",
    #             "tool_call_id": "call_3f8c0f23578f4f3eb7b6fd"
    #         },
    #         {
    #             "tool_name": "ideal_body_weight",
    #             "args": {
    #                 "height_value": 162.8,
    #                 "height_unit": "cm",
    #                 "sex": "Female",
    #                 "age": 16
    #             },
    #             "result": "{\"rationale\": \"The patient's gender is Female.\\nThe patient's height is 162.8 cm, which is 162.8 cm * 0.393701 in/cm = 64.095 in. \\nFor females, the ideal body weight (IBW) is calculated as follows:\\nIBW = 45.5 kg + 2.3 kg * (height (in inches) - 60)\\nPlugging in the values gives us 45.5 kg + 2.3 kg * (64.095 (in inches) - 60) = 54.918 kg.\\nHence, the patient's IBW is 54.918 kg.\", \"final_answer\": \"54.918\"}",
    #             "tool_call_id": "call_e5b4c6ab75204014ac2536"
    #         },
    #         {
    #             "tool_name": "creatinine_clearance",
    #             "args": {
    #                 "weight_value": 54.918,
    #                 "weight_unit": "kg",
    #                 "height_value": 162.8,
    #                 "height_unit": "cm",
    #                 "sex": "Female",
    #                 "creatinine_value": 0.57,
    #                 "creatinine_unit": "mg/dL",
    #                 "age_value": 16,
    #                 "age_unit": "years"
    #             },
    #             "result": "{\"rationale\": \"The formula for computing Cockcroft-Gault is given by CrCl = ((140 - age) * adjusted weight * (gender_coefficient)) / (serum creatinine * 72), where the gender_coefficient is 1 if male, and 0.85 if female. The serum creatinine concentration is in mg/dL.\\nThe patient's gender is female, which means that the gender coefficient is 0.85.\\nThe patient is 16.0 years old. \\nThe concentration of creatinine is 0.57 mg/dL. \\nThe formula for computing the patient's BMI is (weight)/(height * height), where weight is the patient's weight in kg and height is the patient's height in m.\\nThe patient's height is 162.8 cm, which is 162.8 cm * 1 m / 100 cm = 1.628 m. The patient's weight is 54.918 kg. The patient's bmi is therefore 54.918 kg / (1.628 m * 1.628 m) = 20.721 kg/m^2.The patient's BMI is 20.7, indicating they are normal weight.\\nBecause the patient is normal, we take minimum of the ideal body weight and the patient's body as the patient's adjusted weight for the Cockroft-Gault Equation. Hence, the adjusted body weight is the minimum of the two giving us an adjusted body weight of 54.918 kg.\\n\\nUsing the Cockcroft-Gault equation:\\nCrCl = ((140 - age) * adjusted weight * gender_coefficient) / (serum creatinine * 72).\\nPlugging the patient's values gives us ((140 - 16.0) * 54.918 * 0.85) / (0.57 * 72) = 141.042 mL/min. Hence, the patient's creatinine clearance is 141.042 mL/min.\\n\", \"final_answer\": \"141.042\"}",
    #             "tool_call_id": "call_d1e37bbe12e946749149a6"
    #         },
    #         {
    #             "content": "The patient's Creatinine Clearance using the Cockroft-Gault Equation is \\boxed{141.042} mL/min."
    #         }
    #     ],
    #     "final_answer": "141.042",
    #     "metadata": {
    #         "calc_name": "Creatinine Clearance (Cockcroft-Gault Equation)"
    #     }
    # },