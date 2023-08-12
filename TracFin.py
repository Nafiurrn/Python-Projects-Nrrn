import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

def gather_financial_data():
    num_entries = int(input("Enter the number of months: "))
    data = []

    for _ in range(num_entries):
        print(f"Month {_ + 1}")
        income = float(input("Enter your monthly income: "))
        expenses = float(input("Enter your monthly expenses: "))
        investments = float(input("Enter your monthly investments: "))
        savings_goal = float(input("Enter your savings goal: "))
        data.append((income, expenses, investments, savings_goal))

    return data

def calculate_summary(income, expenses, investments, savings_goal):
    net_savings = income - expenses - investments
    return net_savings

def display_summary(net_savings, savings_goal):
    if net_savings >= savings_goal:
        print("Congratulations! You've reached your savings goal.")
    else:
        print(f"You are ${savings_goal - net_savings:.2f} away from your savings goal.")

def visualize_finances(data):
    categories = ['Income', 'Expenses', 'Investments', 'Net Savings']
    df = pd.DataFrame(data, columns=categories)
    sns.set(style="whitegrid")
    sns.barplot(data=df, palette="pastel")
    plt.xlabel('Months')
    plt.ylabel('Amount ($)')
    plt.title('Financial Overview')
    plt.xticks(rotation=45)
    plt.show()

def predict_future_savings(data):
    months = list(range(1, len(data) + 1))
    net_savings = [calculate_summary(*entry) for entry in data]

    model = LinearRegression()
    model.fit(np.array(months).reshape(-1, 1), net_savings)
    
    future_months = list(range(len(data) + 1, len(data) + 6))
    future_predictions = model.predict(np.array(future_months).reshape(-1, 1))

    return future_months, future_predictions

def display_future_predictions(months, predictions):
    print("Predicted Net Savings for Next Months:")
    for month, prediction in zip(months, predictions):
        print(f"Month {month}: ${prediction:.2f}")

def main():
    try:
        print("Welcome to the Financial Tracker!")
        data = gather_financial_data()
        net_savings = [calculate_summary(*entry) for entry in data]
        display_summary(net_savings[-1], data[-1][3])
        visualize_finances(data)
        future_months, future_predictions = predict_future_savings(data)
        display_future_predictions(future_months, future_predictions)
    except ValueError:
        print("Invalid input. Please enter valid numerical values.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
