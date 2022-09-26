from flask import Flask, jsonify, request
import json
import re
from datetime import date, datetime


app = Flask(__name__)

check_for_variable = []
list_of_dob = []
conditon_of_409 = False

info_user = [
    {
        "username": "Adamisfun12",
        "password": "pythonIsmad2",
        "email": "adamisfun@fun.com",
        "DoB": "1999-01-19",
        "creditcard": " ",
    },
    {
        "username": "rachel12",
        "password": "pythonIsfun1",
        "email": "rachiscool@fun.com",
        "DoB": "1999-01-20",
        "creditcard": "5555555555554444",
    },
    {
        "username": "malikthefreak2",
        "password": "pythonIsmad2",
        "email": "malikthefreak@fun.com",
        "DoB": "1999-06-01",
        "creditcard": "4111111111111111",
    },
]

used_username = []
registered_credit_details = []


@app.route("/user", methods=["GET", "POST"])
def index_page():
    condition_of_400 = False
    condition_of_403 = False
    # fileData = 0
    if request.method == "GET":
        data = request.get_json()
        credit = data["creditcard"]
        if credit == " ":
            dob = data["DoB"]
            email = data["email"]
            password = data["password"]
            username = data["username"]
            return jsonify(info_user), 201
        else:
            # is_creditcard_valid = check_creditcard(credit)
            dob = data["DoB"]
            email = data["email"]
            password = data["password"]
            username = data["username"]

        return jsonify(info_user), 201

    if request.method == "POST":
        data = request.get_json()
        dob = data["DoB"]
        credit = data["creditcard"]
        email = data["email"]
        password = data["password"]
        username = data["username"]
        # check data
        valid_or_not = check_username(username)
        if valid_or_not == True:
            if username in used_username:
                # only add username that are verified
                return (
                    json.dumps(
                        {
                            "status": "fail",
                            "message": "unsuccessful POST message. 409",
                        }
                    ),
                    409,
                )
        is_password_valid = check_password(password)
        is_email_valid = check_email(email)
        is_dob_valid = check_dob(dob)
        list_of_dob.append(dob)
        is_creditcard_valid = check_creditcard(credit)
        check_for_variable.append(valid_or_not)
        check_for_variable.append(is_password_valid)
        check_for_variable.append(is_email_valid)
        check_for_variable.append(is_dob_valid)
        check_for_variable.append(is_creditcard_valid)
        print(list_of_dob)
        bool_age_limit, new_condition_of_403 = check_if_age_is_within_limit(
            list_of_dob, condition_of_403
        )
        if bool_age_limit == False:
            return (
                json.dumps(
                    {"status": "fail", "message": "unsuccessful POST message. 403"}
                ),
                403,
            )
        if all(check_for_variable) == False:
            condition_of_400 = True
            check_for_variable.clear()
            return (
                json.dumps(
                    {
                        "status": "fail",
                        "message": "unsuccessful POST message. 400",
                    }
                ),
                400,
            )
        if new_condition_of_403 == False and condition_of_400 == False:
            used_username.append(username)
        # print(used_username)
        # print(condition_of_400)
        # print(condition_of_403)
        # print(check_for_variable)
        info_user.append(
            {
                "dob": dob,
                "creditcard": credit,
                "email": email,
                "password": password,
                "username": username,
            }
        )
        return (
            jsonify(info_user),
            201,
        )


payment_bool = []
payment_example = [{}]


@app.route("/payment", methods=["POST"])
def payment():
    if request.method == "POST":
        data = request.get_json()
        credit = data["credit_card_number"]
        amount = data["Amount"]
        check_card = check_creditcard(credit)
        check_amount = check_amount_func(amount)
        # retrieve all registered people with card -> create a list
        # if element not in list -> 404
        for user in info_user:
            # print(user["creditcard"])
            # print(user["creditcard"])
            if user["creditcard"] != " ":
                registered_credit_details.append(user["creditcard"])
        # registered_credit_details = get_credit_resgister(info_user)
        # print(set(registered_credit_details))
        payment_bool.append(check_card)
        payment_bool.append(check_amount)
        # print(payment_bool)
        check_if_card_not_registered = credit not in registered_credit_details
        if all(payment_bool) == False:
            payment_bool.clear()
            return (
                json.dumps(
                    {"status": "fail", "message": "unsuccessful POST message. 400"}
                ),
                400,
            )
        if check_if_card_not_registered == True:
            return (
                json.dumps(
                    {"status": "fail", "message": "unsuccessful POST message. 404"}
                ),
                404,
            )
        # payment_bool.clear()
        # print(boool)
    return (
        json.dumps({"status": "success", "message": "successful POST message. 201"}),
        201,
    )


# check each variable in list -> check if all the data is cool
def check_list_for_truth(list_of_truth):
    return len(set(list_of_truth)) == 1


# you want to include some checks to see if it complies
# checks if the username is alpha numeric and has no space
# if alpha numeric -> True
# doesnt have space -> False
# hence why the shouldnt be equal -> if they are equal -> the format is incorrect
def check_username(name):
    regex = "^(?=.*[a-zA-Z])(?=.*[0-9])[A-Za-z0-9]+$"
    p = re.compile(regex)
    if re.search(p, name):
        return True
    return False
    # return name.isalnum() != name.isspace()


def check_password(password):
    condition1 = False
    condition2 = False
    condition3 = False
    # check if the length is >= 8
    if len(password) >= 8:
        condition1 = True
    for char in password:
        # check if the string has a number
        if char.isdigit():
            condition2 = True
        # check if the string has a uppercase
        if char.isupper():
            condition3 = True
    return condition1 == True and condition2 == True and condition3 == True


# regex for ISO 8601 date format : https://www.regextester.com/107704
def check_dob(date):
    regex_date = re.compile(r"^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[0-1])$")
    if re.fullmatch(regex_date, date):
        return True
    return False


# check if the email is in a correct format
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
def check_email(email):
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if re.fullmatch(regex, email):
        return True
    return False


# check if its empty or not
# if not empty -> check the length of the string
def check_creditcard(credit_card):
    if credit_card == " ":
        return True
    else:
        return len(credit_card) == 16 and credit_card.isdigit()


# checks if the length of the amount of money = 3
def check_amount_func(amount):
    return len(amount) == 3 and amount.isdigit()


# checks if the username is in the list of previously used usernames
def check_for_duplicate(username, used_username):
    if username in used_username:
        return False
    return True


def check_if_age_is_within_limit(list_of_dob, condition_of_403):
    bool_age_limit = True
    for date in list_of_dob:
        date_time_obj = datetime.strptime(date, "%Y-%m-%d")
        age = datetime.now().date() - date_time_obj.date()
        ag = age.days / 365.25
        if ag < 18:
            bool_age_limit = False
            list_of_dob.remove(date)
            condition_of_403 = True

    return bool_age_limit, condition_of_403
