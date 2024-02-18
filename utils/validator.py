import re

# check valid email
def isValidEmail(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False

# check required field and trim value
def isRequired(field):
    if field == "":
        return False
    else:
        return True
    
# check number
# def isNumber(field) {

# }