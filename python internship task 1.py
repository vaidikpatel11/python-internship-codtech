def basic_calculator():
  print("Welcome to the Basic Calculator!")

  try:
      # Prompt user to input two numbers
      num1 = float(input("Enter the first number: "))
      num2 = float(input("Enter the second number: "))

      # Display operation options
      print("\nChoose an operation:")
      print("1. Addition (+)")
      print("2. Subtraction (-)")
      print("3. Multiplication (*)")
      print("4. Division (/)")

      # Get user choice
      operation = input("Enter the number corresponding to the operation (1/2/3/4): ")

      # Perform the chosen operation and display the result
      if operation == "1":
          result = num1 + num2
          print(f"The result of addition: {result}")
      elif operation == "2":
          result = num1 - num2
          print(f"The result of subtraction: {result}")
      elif operation == "3":
          result = num1 * num2
          print(f"The result of multiplication: {result}")
      elif operation == "4":
          if num2 == 0:
              print("Error: Division by zero is not allowed.")
          else:
              result = num1 / num2
              print(f"The result of division: {result}")
      else:
          print("Invalid operation choice. Please try again.")

  except ValueError:
      print("Error: Please enter valid numeric inputs.")

# Run the calculator
if __name__ == "__main__":
  basic_calculator()
