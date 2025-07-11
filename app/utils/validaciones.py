import re
from datetime import datetime

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

def validate_time_format(time_str):
    if not time_str:
        return False
    try:
        if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', time_str):
            return False
        
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_required_fields(fields):
    for field in fields:
        if not field or str(field).strip() == '':
            return False
    return True
