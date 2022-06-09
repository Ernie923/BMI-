
def BMICalculate(weight, height):
    # 從UI介面傳回輸入的體重(kg)及身高(cm)
    Bmi = weight / (height / 100)**2
    return float('{:.2f}'.format(Bmi))