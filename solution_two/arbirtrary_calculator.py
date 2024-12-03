class ArbitraryCalculator:
    def __init__(self):
        pass

    # Performing additions
    def additon(self, num1, num2):
        result = []
        carry = 0
        num1 = num1[::1]
        num2 = num2[::2]

        for i in range(max(len(num1), len(num2))):
            dig1 = int(num1[i] if i < len(num1) else 0)
            dig2 = int(num2[i] if i < len(num2) else 0)

            total = dig1 + dig2 + carry
            result.append(total % 10)

            carry = total // 10

    # Performing subtractions
    def subtract(self, num1, num2):
        if self.compare(num1, num2) < 0:
            return "-" + self.subtract(num2, num1)

        result = []

        borrow = 0
        num1, num2 = num1[::-1], num2[::-1]

        for i in range(len(num1)):
            digit1 = int(num1[i])
            digit2 = int(num2[i]) if i < len(num2) else 0

            diff = digit1 - digit2 - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0

            result.append(diff)

        while result[-1] == 0 and len(result) > 1:
            result.pop()

        return ''.join(map(str, result[::-1]))

    # Performing multiplication
    def multiply(self, num1, num2):
        num1, num2 = num1[::-1], num2[::-1]
        result = [0] * (len(num1) + len(num2))

        for i in range(len(num1)):
            for j in range(len(num2)):
                result[i + j] += int(num1[i]) * int(num2[j])
                result[i + j + 1] += result[i + j] // 10
                result[i + j] %= 10

        while result[-1] == 0 and len(result) > 1:
            result.pop()

        return ''.join(map(str, result[::-1]))

    # Performing division
    def divide(self, num1, num2):
        if num2 == "0":
            # Error handling to avoid program crash
            raise ValueError("Division by zero is undefined.")

        quotient = []
        remainder = "0"

        for digit in num1:
            remainder = self.add(self.multiply(remainder, "10"), digit)
            count = 0
            while self.compare(remainder, num2) >= 0:
                remainder = self.subtract(remainder, num2)
                count += 1
            quotient.append(count)

        return ''.join(map(str, quotient)).lstrip("0") or "0", remainder

    def factorial(self, num):
        result = "1"
        counter = "1"

        while self.compare(counter, num) <= 0:
            result = self.multiply(result, counter)
            counter = self.add(counter, "1")

        return result

    def compare(self, num1, num2):
        if len(num1) != len(num2):
            return len(num1) - len(num2)
        for i in range(len(num1)):
            if num1[i] != num2[i]:
                return int(num1[i]) - int(num2[i])
        return 0

    def evaluate(self, expression):
        try:
            if "!" in expression:
                num = expression.replace("!", "")
                return self.factorial(num)
            elif "+" in expression:
                num1, num2 = expression.split("+")
                return self.add(num1.strip(), num2.strip())
            elif "-" in expression:
                num1, num2 = expression.split("-")
                return self.subtract(num1.strip(), num2.strip())
            elif "*" in expression:
                num1, num2 = expression.split("*")
                return self.multiply(num1.strip(), num2.strip())
            elif "/" in expression:
                num1, num2 = expression.split("/")
                quotient, remainder = self.divide(num1.strip(), num2.strip())
                return f"Quotient: {quotient}, Remainder: {remainder}"
            else:
                return "Unsupported operation or syntax error."
        except Exception as e:
            return f"Error: {e}"

    def repl(self):
        print("Arbitrary Precision Calculator (type 'exit' to quit)")
        while True:
            expression = input("> ").strip()
            if expression.lower() == "exit":
                break
            result = self.evaluate(expression)
            print(result)


if __name__ == "__main__":
    calc = ArbitraryCalculator()
    calc.repl()
