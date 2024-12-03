class ArbitraryCalculator:
    def __init__(self):
        pass

    # Perform addition of two large numbers
    def addition(self, num1, num2):
        result = []
        carry = 0

        # Reverse both numbers to perform addition from the least significant digit
        num1 = num1[::-1]
        num2 = num2[::-1]

        # Iterate through the digits
        for i in range(max(len(num1), len(num2))):
            dig1 = int(num1[i]) if i < len(num1) else 0  # Get digit or 0 if out of range
            dig2 = int(num2[i]) if i < len(num2) else 0  # Get digit or 0 if out of range

            # Calculate the sum and carry
            total = dig1 + dig2 + carry
            result.append(total % 10)  # Append current digit
            carry = total // 10  # Update carry

        # Add any remaining carry
        if carry:
            result.append(carry)

        # Reverse back to original order and join digits into a string
        return ''.join(map(str, result[::-1]))

    # Perform subtraction of two large numbers
    def subtract(self, num1, num2):
        if self.compare(num1, num2) < 0:  # Handle negative result
            return "-" + self.subtract(num2, num1)

        result = []
        borrow = 0

        # Reverse both numbers for easier subtraction
        num1, num2 = num1[::-1], num2[::-1]

        # Iterate through the digits of num1
        for i in range(len(num1)):
            digit1 = int(num1[i])
            digit2 = int(num2[i]) if i < len(num2) else 0

            # Perform subtraction considering borrow
            diff = digit1 - digit2 - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0

            result.append(diff)

        # Remove leading zeros
        while len(result) > 1 and result[-1] == 0:
            result.pop()

        # Reverse back to original order
        return ''.join(map(str, result[::-1]))

    # Perform multiplication of two large numbers
    def multiply(self, num1, num2):
        num1, num2 = num1[::-1], num2[::-1]
        result = [0] * (len(num1) + len(num2))  # Initialize result array

        # Perform digit-wise multiplication
        for i in range(len(num1)):
            for j in range(len(num2)):
                result[i + j] += int(num1[i]) * int(num2[j])
                result[i + j + 1] += result[i + j] // 10  # Handle carry
                result[i + j] %= 10  # Retain only single digit

        # Remove leading zeros
        while len(result) > 1 and result[-1] == 0:
            result.pop()

        # Convert result array to string
        return ''.join(map(str, result[::-1]))

    # Perform division of two large numbers
    def divide(self, num1, num2):
        if num2 == "0":
            raise ValueError("Division by zero is undefined.")  # Handle division by zero

        quotient = []
        remainder = "0"

        # Perform division digit by digit
        for digit in num1:
            remainder = self.addition(self.multiply(remainder, "10"), digit)
            count = 0
            while self.compare(remainder, num2) >= 0:
                remainder = self.subtract(remainder, num2)
                count += 1
            quotient.append(count)

        return ''.join(map(str, quotient)).lstrip("0") or "0", remainder

    # Compute factorial of a large number
    def factorial(self, num):
        result = "1"
        counter = "1"

        # Multiply result by counter until counter exceeds num
        while self.compare(counter, num) <= 0:
            result = self.multiply(result, counter)
            counter = self.addition(counter, "1")

        return result

    # Compare two large numbers (returns -1, 0, 1)
    def compare(self, num1, num2):
        if len(num1) != len(num2):
            return len(num1) - len(num2)
        for i in range(len(num1)):
            if num1[i] != num2[i]:
                return int(num1[i]) - int(num2[i])
        return 0

    # Evaluate mathematical expressions
    def evaluate(self, expression):
        try:
            if "!" in expression:
                num = expression.replace("!", "")
                return self.factorial(num)
            elif "+" in expression:
                num1, num2 = expression.split("+")
                return self.addition(num1.strip(), num2.strip())
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

    # Run a REPL for user input
    def repl(self):
        print("Arbitrary Precision Calculator (type 'exit' to quit)")
        while True:
            expression = input("> ").strip()
            if expression.lower() == "exit":
                break
            result = self.evaluate(expression)
            print(result)


# Example usage
if __name__ == "__main__":
    calc = ArbitraryCalculator()
    calc.repl()
