import streamlit as st

# Simple in-memory "database" for demo purpose
if 'users' not in st.session_state:
    st.session_state.users = {}  # {username: {password, income, savings, days, expenses}}

if 'login' not in st.session_state:
    st.session_state.login = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def register():
    st.subheader("📝 Register New User")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    new_income = st.number_input("Monthly Income", min_value=0.0, format="%.2f")
    new_savings = st.number_input("Initial Savings", min_value=0.0, format="%.2f")
    new_days = st.number_input("Number of Days", min_value=1, step=1)

    if st.button("Register"):
        if new_user in st.session_state.users:
            st.error("User already exists. Please login.")
        elif not new_user or not new_pass:
            st.error("Username and password cannot be empty.")
        else:
            st.session_state.users[new_user] = {
                "password": new_pass,
                "income": new_income,
                "savings": new_savings,
                "days": new_days,
                "expenses": []
            }
            st.success(f"User {new_user} registered! Please login.")

def login():
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user]["password"] == pwd:
            st.session_state.login = True
            st.session_state.current_user = user
            st.success(f"Welcome {user}!")
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state.login = False
    st.session_state.current_user = None
    st.info("Logged out successfully")

def expense_tracker():
    user = st.session_state.current_user
    user_data = st.session_state.users[user]

    st.header(f"💼 Expense Tracker for {user}")

    income = user_data["income"]
    savings = user_data["savings"]
    days = user_data["days"]
    expenses = user_data["expenses"]

    # Calculate daily limit
    if days > 0:
        expense_limit = (income - savings) / days
    else:
        expense_limit = 0

    st.markdown(f"### Your Monthly Income: ₹{income:.2f}")
    st.markdown(f"### Your Current Savings: ₹{savings:.2f}")
    st.markdown(f"### Number of Days: {days}")
    st.markdown(f"### Daily Expense Limit: ₹{expense_limit:.2f}")

    st.markdown("---")
    st.subheader("Add New Expense (Simulating UPI Payment)")

    new_expense = st.number_input("Enter Expense Amount", min_value=0.0, format="%.2f")
    expense_note = st.text_input("Expense Note / Description")

    if st.button("Add Expense"):
        if new_expense <= 0:
            st.error("Expense amount must be greater than zero")
        else:
            daily_expense_sum = sum(exp['amount'] for exp in expenses) + new_expense
            # Check if daily limit exceeded (approximate by dividing total expense over days)
            if daily_expense_sum > expense_limit * len(expenses) + expense_limit:
                st.warning(f"⚠️ Warning: Adding this expense exceeds your daily limit of ₹{expense_limit:.2f}")
            # Save expense
            expenses.append({"amount": new_expense, "note": expense_note})
            st.session_state.users[user]["expenses"] = expenses
            st.success(f"Expense of ₹{new_expense:.2f} added!")

    st.markdown("---")
    st.subheader("Expense History")

    if expenses:
        for idx, exp in enumerate(expenses, 1):
            st.write(f"{idx}. ₹{exp['amount']:.2f} - {exp['note']}")
    else:
        st.info("No expenses added yet.")

    st.markdown("---")
    if st.button("Logout"):
        logout()

def main():
    st.title("🔷 Expense Management with Login & User Tracking")

    if not st.session_state.login:
        tab = st.sidebar.selectbox("Choose Action", ["Login", "Register"])
        if tab == "Login":
            login()
        else:
            register()
    else:
        expense_tracker()

if __name__ == "__main__":
    main()
