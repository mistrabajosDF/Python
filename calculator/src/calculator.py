from src import operations

def calculate():
    num1 = float(input("Ingrese el primer número: "))
    num2 = float(input("Ingrese el segundo número: "))

    print("Suma:", operations.add(num1, num2))
    print("Resta:", operations.substract(num1, num2))
    print("Multiplicación:", operations.multiply(num1, num2))
    print("División:", operations.divide(num1, num2))