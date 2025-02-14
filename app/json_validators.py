full_name_validation = {
    'type': 'string',
    'required': True,
}
update_full_name_validation = {
    'type': 'string',
}
email_validation = {
    'type': 'string',
    'regex': r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
    'required': True,
}
update_email_validation = {
    'type': 'string',
    'regex': r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
}
password_validation = {
    'type': 'string',
    'minlength': 6,
    'maxlength': 64,
    'required': True,
}
update_password_validation = {
    'type': 'string',
    'minlength': 6,
    'maxlength': 64,
}
transaction_id_validation ={
    'type': 'string',
    'required': True,
}
account_id_validation ={
    'type': 'integer',
    'required': True,
}
user_id_validation ={
    'type': 'integer',
    'required': True,
}
amount_validation ={
    'type': 'integer',
    'required': True,
}
signature_validation ={
    'type': 'string',
    'required': True,
}

transaction_schema = {
    'transaction_id': transaction_id_validation,
    'account_id': account_id_validation,
    'user_id': user_id_validation,
    'amount': amount_validation,
    'signature': signature_validation
}

user_schema = {
    'full_name': full_name_validation,
    'email': email_validation,
    'password': password_validation
}

update_user_schema = {
    'user_id': user_id_validation,
    'full_name': update_full_name_validation,
    'email': update_email_validation,
    'password': update_password_validation
}

login_user_schema = {
    'email': update_email_validation,
    'password': update_password_validation
}