import pandas as pd
from .forms import PackageForm, get_tracking_form, ReplyForm, phone_number_validator
import re 

def phone_number_validator(phone_number):
    pattern = re.compile(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$')
    match = pattern.match(str(phone_number))
    if match:
        return ''.join(match.groups('')[:4])
    return phone_number


def read_customer_data(file_path):
    df = pd.read_csv(file_path)
    df["Phone Number"] = df["Phone Number"].apply(phone_number_validator)
    print(df)
    return pd.read_csv(file_path)