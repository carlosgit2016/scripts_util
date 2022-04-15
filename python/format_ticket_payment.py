import re
import sys

def format_payment_ticket(ticket_number):
    formated_ticket_number = ticket_number.replace(".", "")
    pattern = r"\s+|-*"
    formated_ticket_number = re.sub(pattern, "", formated_ticket_number)
    return formated_ticket_number

if __name__ == "__main__":
    formated_ticket_number = format_payment_ticket(sys.argv[1])
    print(formated_ticket_number)
