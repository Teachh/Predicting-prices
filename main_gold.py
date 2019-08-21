import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import datetime
from datetime import timedelta
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
import csv

archivo = pd.read_csv("data/gold-prices-csv_csv.csv", names=["Date", "Price"], sep=",", skiprows=1, skip_blank_lines=True,)
column_names_used = [
    "Date"
]

def make_numeric_values(arr, title):
    new_arr = []
    for date in arr[title]:
        new_date = make_date(date)
        new_arr.append(new_date)
    arr[title] = new_arr

def fix_array(arr):
    for name in column_names_used:
        make_numeric_values(arr, name)


def make_date(date):
    new_date = date.split(' ')
    new_date = new_date[0]
    new_date = new_date.split('-')
    new_number = ''
    first = True
    for number in new_date:
        if first:
            first = False
        else:
            new_number = new_number + number
    return new_number
def make_date(date):
    new_date = date.split(' ')
    new_date = new_date[0]
    new_date = new_date.split('-')
    new_number = ''
    first = True
    for number in new_date:
        if first:
            first = False
        else:
            new_number = new_number + number
    return new_number

def convert_date_to_string(plus_days):
    date = datetime.datetime.today() + timedelta(days=plus_days)
    date = date.strftime("%Y-%m-%d %H:%M:%S") 
    date = date.split(' ')
    date = date[0]
    date = date.split('-')
    date = date[1]+date[2]
    return date

def train():

    X = archivo.drop(["Price"], axis=1)
    fix_array(X)

    y = archivo['Price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=123)

    tree_model = DecisionTreeRegressor()
    tree_model.fit(X_train.values.reshape(-1, 1), y_train)
    joblib.dump(tree_model, 'gold_predictor.pkl')
    print("-" * 48)
    print("\nDone training\n")
    print("-" * 48)


def predict_price():
    tree_model = joblib.load('gold_predictor.pkl')

    print("-" * 48)
    print("Enter the details of the date you would like to predict")
    print("\n")
    option = input("Year: ")
    year = option
    option = input("Month number (00): ")
    month = option
    option = input("Day number (00): ")
    theday = option

    day = str(month) + str(theday)
    date = [
        [day]
    ]
    temp = tree_model.predict(date)[0]
    print("-" * 48)
    print("\nThe price is estimated to be: " + str(temp) + "\n")
    print("-" * 48)

def get_the_price(date):
    dia = archivo.Date
    precio = archivo.Price

    for i in range(0, len(dia)):
        day = datetime.datetime.strptime(dia[i], "%Y-%m-%d")
        if (day == date):
            return precio[i]


def run_program(option):
    if option == 1:
        train()
    elif option == 2:
        predict_price()


def run_menu():
    print("*" *48)
    print("-" *10 + " What would you like to do? " + "-" * 10)
    print("\n")
    print("1. Train")
    print("2. Predict the bitcoin price on a specific day")
    print("9. Exit")
    print("\n")

    option = input("Enter option: ")

    while True:
        if option == "2" or option == "1" or option == "9":
            break
        option = input("Enter option: ")
    return option

if __name__== "__main__":
    while True:
        option = run_menu()
        option = int(option)
        if option == 9:
            break
        else:
            run_program(option)