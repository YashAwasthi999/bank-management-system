import json
import secrets
import string
from pathlib import Path
from datetime import datetime


class Bank:
    database = Path("data.json")

    def __init__(self):
        self.data = self._load_data()

    # -----------------------------
    # File Handling
    # -----------------------------

    def _load_data(self):
        try:
            if not self.database.exists():
                return []

            with open(self.database, "r", encoding="utf-8") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError) as error:
            print(f"Error loading database: {error}")
            return []

    def _update(self):
        try:
            with open(self.database, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4)

        except OSError as error:
            raise Exception(f"Unable to save database: {error}")

    # -----------------------------
    # Account Number Generation
    # -----------------------------

    def _account_generate(self):
        characters = (
            string.ascii_uppercase
            + string.digits
            + "!@#$%^&*"
        )

        while True:
            account = "".join(
                secrets.choice(characters)
                for _ in range(9)
            )

            if not any(
                user["account"] == account
                for user in self.data
            ):
                return account

    # -----------------------------
    # Find Account
    # -----------------------------

    def find_account(self, account_number, pin):
        for user in self.data:
            if (
                user["account"] == account_number
                and user["pin"] == pin
            ):
                return user

        return None

    # -----------------------------
    # Create Account
    # -----------------------------

    def create_account(self, name, age, email, pin):

        name = name.strip()
        email = email.strip()
        pin = pin.strip()

        if not name:
            return False, "Name cannot be empty."

        if age < 18:
            return False, "You must be at least 18 years old."

        if not pin.isdigit() or len(pin) != 4:
            return False, "PIN must contain exactly 4 digits."

        if "@" not in email or "." not in email:
            return False, "Please enter a valid email address."

        account_number = self._account_generate()

        user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account": account_number,
            "balance": 0,
            "transactions": []
        }

        self.data.append(user)
        self._update()

        return True, account_number

    # -----------------------------
    # Deposit
    # -----------------------------

    def deposit(self, account_number, pin, amount):

        user = self.find_account(account_number, pin)

        if not user:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Deposit amount must be greater than 0."

        if amount > 10000:
            return False, "Maximum deposit is ₹10,000 per transaction."

        user["balance"] += amount

        user["transactions"].append({
            "type": "Deposit",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self._update()

        return True, f"₹{amount:,.2f} deposited successfully."

    # -----------------------------
    # Withdraw
    # -----------------------------

    def withdraw(self, account_number, pin, amount):

        user = self.find_account(account_number, pin)

        if not user:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Withdrawal amount must be greater than 0."

        if amount > user["balance"]:
            return False, "Insufficient balance."

        user["balance"] -= amount

        user["transactions"].append({
            "type": "Withdrawal",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self._update()

        return True, f"₹{amount:,.2f} withdrawn successfully."

    # -----------------------------
    # Get Account Details
    # -----------------------------

    def get_details(self, account_number, pin):

        user = self.find_account(account_number, pin)

        if not user:
            return None

        # Never expose PIN
        details = user.copy()
        details.pop("pin", None)

        return details

    # -----------------------------
    # Update Details
    # -----------------------------

    def update_details(
        self,
        account_number,
        pin,
        name=None,
        email=None,
        new_pin=None
    ):

        user = self.find_account(account_number, pin)

        if not user:
            return False, "Invalid account number or PIN."

        if name is not None and name.strip():
            user["name"] = name.strip()

        if email is not None and email.strip():
            if "@" not in email or "." not in email:
                return False, "Invalid email address."

            user["email"] = email.strip()

        if new_pin is not None and new_pin.strip():

            new_pin = new_pin.strip()

            if not new_pin.isdigit() or len(new_pin) != 4:
                return False, "PIN must contain exactly 4 digits."

            user["pin"] = new_pin

        self._update()

        return True, "Account details updated successfully."

    # -----------------------------
    # Delete Account
    # -----------------------------

    def delete_account(self, account_number, pin):

        user = self.find_account(account_number, pin)

        if not user:
            return False, "Invalid account number or PIN."

        if user["balance"] != 0:
            return False, (
                "Account cannot be deleted while balance is not zero."
            )

        self.data.remove(user)
        self._update()

        return True, "Account deleted successfully."