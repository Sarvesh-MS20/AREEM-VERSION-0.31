#tools/calculator.py
import re
def calculator(query):
    equation = " ".join(re.findall(r"[0-9+\-*/.]+",query))
    try:
        result = str(eval(equation))
        return result
    except:
        return "ERROR"
