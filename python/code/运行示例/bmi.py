def calc_bmi_and_print(weight, height):

    if height <= 0:
        print("身高必须大于0")
        return

    if weight <= 0:
        print("体重必须大于0")
        return

    bmi = weight / (height ** 2)
    print(f"您的BMI是: {bmi:.2f}")

response_bmi=calc_bmi_and_print(70, 1.75)
print(response_bmi)