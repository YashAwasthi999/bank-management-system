import streamlit as st
from main import Bank


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide"
)


# -----------------------------------ko
# Bank Object
# -----------------------------------

bank = Bank()


# -----------------------------------
# Session State
# -----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None

if "pin" not in st.session_state:
    st.session_state.pin = None


# -----------------------------------
# Helper Functions
# -----------------------------------

def login(account, pin):

    user = bank.find_account(account, pin)

    if user:
        st.session_state.logged_in = True
        st.session_state.account = account
        st.session_state.pin = pin
        return True

    return False


def logout():

    st.session_state.logged_in = False
    st.session_state.account = None
    st.session_state.pin = None

    st.rerun()


# -----------------------------------
# Header
# -----------------------------------

st.title("🏦 Bank Management System")
st.caption("Simple banking application built with Python + Streamlit")


# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    st.subheader("🔐 Account Login")

    with st.form("login_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "4 Digit PIN",
            type="password",
            max_chars=4
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if login_button:

            if not account_number or not pin:
                st.error("Please enter account number and PIN.")

            elif login(account_number, pin):
                st.success("Login successful!")
                st.rerun()

            else:
                st.error(
                    "Invalid account number or PIN."
                )


    st.divider()

    # -----------------------------------
    # Create Account
    # -----------------------------------

    st.subheader("📝 Create New Account")

    with st.form("create_account_form"):

        name = st.text_input(
            "Account Holder Name"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        email = st.text_input(
            "Email"
        )

        pin = st.text_input(
            "Create 4 Digit PIN",
            type="password",
            max_chars=4
        )

        create_button = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if create_button:

            success, result = bank.create_account(
                name,
                age,
                email,
                pin
            )

            if success:

                st.success(
                    "Account created successfully!"
                )

                st.info(
                    f"Your account number is: **{result}**"
                )

                st.warning(
                    "Please save your account number safely."
                )

            else:
                st.error(result)


# =====================================================
# DASHBOARD
# =====================================================

else:

    account = st.session_state.account
    pin = st.session_state.pin

    user = bank.find_account(account, pin)

    if not user:

        st.error("Account no longer exists.")
        logout()

    # -----------------------------------
    # Sidebar
    # -----------------------------------

    with st.sidebar:

        st.title("🏦 Menu")

        st.write(
            f"**Account:** `{account}`"
        )

        st.divider()

        menu = st.radio(
            "Choose an option",
            [
                "Dashboard",
                "Deposit Money",
                "Withdraw Money",
                "Account Details",
                "Update Details",
                "Transaction History",
                "Delete Account"
            ]
        )

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):
            logout()


    # =================================================
    # DASHBOARD
    # =================================================

    if menu == "Dashboard":

        st.header("📊 Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Account Holder",
                user["name"]
            )

        with col2:
            st.metric(
                "Current Balance",
                f"₹{user['balance']:,.2f}"
            )

        with col3:
            st.metric(
                "Account Number",
                user["account"]
            )

        st.divider()

        st.subheader("Recent Transactions")

        if user["transactions"]:

            recent = user["transactions"][-5:]

            for transaction in reversed(recent):

                if transaction["type"] == "Deposit":
                    icon = "⬆️"
                else:
                    icon = "⬇️"

                st.write(
                    f"{icon} **{transaction['type']}** "
                    f"₹{transaction['amount']:,.2f} "
                    f"— {transaction['date']}"
                )

        else:

            st.info("No transactions yet.")


    # =================================================
    # DEPOSIT
    # =================================================

    elif menu == "Deposit Money":

        st.header("💰 Deposit Money")

        st.info(
            f"Current Balance: "
            f"₹{user['balance']:,.2f}"
        )

        with st.form("deposit_form"):

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                max_value=10000.0,
                step=100.0
            )

            submit = st.form_submit_button(
                "Deposit Money",
                use_container_width=True
            )

            if submit:

                success, message = bank.deposit(
                    account,
                    pin,
                    amount
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


    # =================================================
    # WITHDRAW
    # =================================================

    elif menu == "Withdraw Money":

        st.header("💸 Withdraw Money")

        st.info(
            f"Available Balance: "
            f"₹{user['balance']:,.2f}"
        )

        with st.form("withdraw_form"):

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=100.0
            )

            submit = st.form_submit_button(
                "Withdraw Money",
                use_container_width=True
            )

            if submit:

                success, message = bank.withdraw(
                    account,
                    pin,
                    amount
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


    # =================================================
    # ACCOUNT DETAILS
    # =================================================

    elif menu == "Account Details":

        st.header("👤 Account Details")

        details = bank.get_details(
            account,
            pin
        )

        if details:

            col1, col2 = st.columns(2)

            with col1:

                st.write("**Name**")
                st.write(details["name"])

                st.write("**Age**")
                st.write(details["age"])

                st.write("**Email**")
                st.write(details["email"])

            with col2:

                st.write("**Account Number**")
                st.code(details["account"])

                st.write("**Balance**")
                st.metric(
                    "Balance",
                    f"₹{details['balance']:,.2f}"
                )

        else:
            st.error("Unable to retrieve account details.")


    # =================================================
    # UPDATE DETAILS
    # =================================================

    elif menu == "Update Details":

        st.header("✏️ Update Account Details")

        with st.form("update_form"):

            name = st.text_input(
                "New Name",
                value=user["name"]
            )

            email = st.text_input(
                "New Email",
                value=user["email"]
            )

            new_pin = st.text_input(
                "New PIN",
                type="password",
                max_chars=4
            )

            submit = st.form_submit_button(
                "Update Details",
                use_container_width=True
            )

            if submit:

                success, message = bank.update_details(
                    account,
                    pin,
                    name,
                    email,
                    new_pin
                )

                if success:

                    st.success(message)

                    # If PIN changed, force re-login
                    if new_pin:
                        st.session_state.pin = new_pin

                    st.rerun()

                else:
                    st.error(message)


    # =================================================
    # TRANSACTION HISTORY
    # =================================================

    elif menu == "Transaction History":

        st.header("📜 Transaction History")

        transactions = user["transactions"]

        if not transactions:

            st.info("No transactions found.")

        else:

            for transaction in reversed(transactions):

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(
                        f"**{transaction['type']}**"
                    )

                with col2:
                    st.write(
                        f"₹{transaction['amount']:,.2f}"
                    )

                with col3:
                    st.write(
                        transaction["date"]
                    )


    # =================================================
    # DELETE ACCOUNT
    # =================================================

    elif menu == "Delete Account":

        st.header("⚠️ Delete Account")

        st.warning(
            "Account deletion is permanent."
        )

        if user["balance"] != 0:

            st.error(
                "You cannot delete an account "
                "with a non-zero balance."
            )

        else:

            confirm = st.checkbox(
                "I understand that this action cannot be undone."
            )

            if confirm:

                if st.button(
                    "Delete My Account",
                    type="primary"
                ):

                    success, message = bank.delete_account(
                        account,
                        pin
                    )

                    if success:

                        st.success(message)

                        st.session_state.logged_in = False
                        st.session_state.account = None
                        st.session_state.pin = None

                        st.rerun()

                    else:
                        st.error(message)
