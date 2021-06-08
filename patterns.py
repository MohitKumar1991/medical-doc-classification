## changes - if multiple match match the longest one
## 

import re
import functools
value_pattern  = re.compile(r'[0-9]{1,6}[\.-]?[0-9]{0,3}|nil|na|negative|normal|absent',flags=re.IGNORECASE)
method_pattern = re.compile(r'method\s*:', flags=re.IGNORECASE)
sep_pattern = re.compile(r'\t|[ ]{2,}')
#instead of putting ug/dl need to put all permutations like ug/dl, ug / dl, ug/ dl, ug /dl
units_group = ['g/dl', 'million/cu.mm','cells/cu.mm', 'pg','u/l','mL/min','/hpf','μiu/mL','g/l', 'mg/l','pg/ml', 'ng/ml','μg/dl', 'ug/dl','%', '10^3 / μL', '10^3/μL','10^3/ µL', 'fl', '10^6/µL', '10^6 / µL','10^6/ µL','pq','ratio','μiu/ml','ml/min','mg/dl','ng/dl','μg/dl','u/l', 'gm/dl']
test_name_group = ['covid antibody', 'covid antibodies', 'vitamin d', 'vitamin b-12', 'testosterone', 'iron','transferrin saturation', 'iron binding capacity'
                  ,'total cholestrol','hdl cholestrol', 'ldl cholestrol', 'triglycerides', 'vldl cholestrol', 'non-hdl cholestrol', 'alkaline phosphatase', 'bilirubin',
                  'gamma glutamyl transferase', 'serum globulin', 'albumin', 'total triiodothyronine', 'total thyroxine', 'thyroid stimulating hormone', 'blood urea nitrogen'
                  ,'creatinine', 'calcium', 'uric acid','GLOMERULAR FILTRATION RATE'.lower(),'hb1ac', 'LEUCOCYTES COUNT'.lower(), 'neutrophils',
                  'lymphocyte', 'monocytes', 'eosinophils', 'basophils', 'immature granulocyte', 'hemoglobin', 'hematocrit', 'red cell distribution width'
                  ,'platelet distribution width', 'platelet count', 'plateletcrit','mean corp']

patient_name_pattern = re.compile(r'^(patient\s)?name', flags=re.IGNORECASE)
patient_id_pattern = re.compile(r'^(patientid|patient id|id)',flags=re.IGNORECASE)

def isRegex(reg, v):
    sr = reg.search(v)
    if sr is not None:
        return (sr[0], sr.start(), sr.end(), v)
    else:
        return False
    
def isInGroup(group, v):
    lower_v = v.lower()
    for g in group:
        try:
            sind = lower_v.index(g)
        except ValueError:
            sind = -1
        if  sind > -1:
            return (g, sind, sind + len(g), v)
    return False

def follow(patterns, match_str):
    curr_str = match_str
    results = []
    for pattern in patterns:
        res = pattern(curr_str)
#         print('res',res, curr_str, pattern)
        if res:
            curr_str = curr_str[res[2]:]
            results.append((res[0], res[3]))
        else:
            return False
    return results

    
isUnit = functools.partial(isInGroup, units_group)  
isValue = functools.partial(isRegex, value_pattern)
isPatientName = functools.partial(isRegex, patient_name_pattern)
isPatientId = functools.partial(isRegex, patient_id_pattern)
isSeperator = functools.partial(isRegex, sep_pattern)
isTestName  = functools.partial(isInGroup, test_name_group)
isMethodLabel = functools.partial(isRegex, method_pattern)
isMethod = functools.partial(follow, [isMethodLabel, functools.partial(isRegex, re.compile('[a-z .-]+', flags=re.IGNORECASE)) ])
isVU = functools.partial(follow, [isValue, isSeperator, isUnit])
isTestVal = functools.partial(follow, [isTestName, isValue, isSeperator, isUnit])