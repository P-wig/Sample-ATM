from flask import Blueprint, render_template, session, jsonify
import csv


def get_balance_for_pin(pin):
    with open('data/accounts.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['pin'] == pin:
                return float(row['balance'])
    return None


def get_blueprint():
    account_transaction_blueprint = Blueprint('account_transaction', __name__, url_prefix='/account')

    @account_transaction_blueprint.route('/', methods=['GET'])
    def render_account_page():
        pin = session.get('pin')
        if not pin:
            # Redirect to login if not authenticated
            return render_template('login.html')
        balance = get_balance_for_pin(pin)
        return render_template('transaction.html', balance=balance)

    @account_transaction_blueprint.route('/balance', methods=['GET'])
    def get_balance():
        pin = session.get('pin')
        if not pin:
            return jsonify({"error": "Not logged in"}), 401
        balance = get_balance_for_pin(pin)
        return jsonify({"balance": balance})

    return account_transaction_blueprint