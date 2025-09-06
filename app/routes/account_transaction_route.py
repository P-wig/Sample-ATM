from flask import Blueprint, render_template, session, jsonify, request
import csv


def get_account_info(pin):
    with open('data/accounts.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['pin'] == pin:
                return {
                    "balance": float(row['balance']),
                    "withdrawal_limit": float(row.get('withdrawal_limit', 0))
                }
    return None


def get_blueprint():
    account_transaction_blueprint = Blueprint('account_transaction', __name__, url_prefix='/account')

    @account_transaction_blueprint.route('/', methods=['GET'])
    def render_account_page():
        """
        Render the transaction page
        ---
        tags:
          - Account
        responses:
          200:
            description: Renders the transaction page with current balance and withdrawal limit
          401:
            description: Not logged in
        """
        pin = session.get('pin')
        if not pin:
            # Redirect to login if not authenticated
            return render_template('login.html')
        info = get_account_info(pin)
        if info:
            balance = info['balance']
            withdrawal_limit = info['withdrawal_limit']
        else:
            balance = 0
            withdrawal_limit = 0
        return render_template('transaction.html', balance=balance, withdrawal_limit=withdrawal_limit)

    @account_transaction_blueprint.route('/balance', methods=['GET'])
    def get_balance():
        """
        Get account balance and withdrawal limit
        ---
        tags:
        - Account
        responses:
        200:
            description: Returns the account balance and withdrawal limit
            schema:
            type: object
            properties:
                balance:
                type: number
                withdrawal_limit:
                type: number
                example: 1500.00
        401:
            description: Not logged in
        """
        pin = session.get('pin')
        if not pin:
            return jsonify({"error": "Not logged in"}), 401
        info = get_account_info(pin)
        if info:
            balance = info['balance']
            withdrawal_limit = info['withdrawal_limit']
        else:
            balance = 0
            withdrawal_limit = 0
        return jsonify({"balance": balance, "withdrawal_limit": withdrawal_limit})

    @account_transaction_blueprint.route('/transaction', methods=['POST'])
    def transaction():
        """
        Perform a deposit or withdrawal
        ---
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                type:
                  type: string
                  description: Transaction type ('deposit' or 'withdraw')
                  example: deposit
                amount:
                  type: number
                  description: Amount to deposit or withdraw
                  example: 100.00
        responses:
          200:
            description: Transaction successful
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                new_balance:
                  type: number
                  example: 1600.00
          400:
            description: Invalid request
          401:
            description: Not logged in
        """
        pin = session.get('pin')
        if not pin:
            return jsonify({"success": False, "message": "Not logged in"}), 401
        data = request.get_json()
        transaction_type = data.get('type')
        amount = float(data.get('amount', 0))
        updated = False
        new_balance = None
        rows = []

        with open('data/accounts.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['pin'] == pin:
                    balance = float(row['balance'])
                    withdrawal_limit = float(row.get('withdrawal_limit', 0))
                    if transaction_type == "deposit":
                        balance += amount
                    elif transaction_type == "withdraw":
                        if amount > balance:
                            return jsonify({"success": False, "message": "Insufficient funds"})
                        if amount > withdrawal_limit:
                            return jsonify({"success": False, "message": "Withdrawal limit exceeded", "limit_exceeded": True, "withdrawal_limit": withdrawal_limit})
                        balance -= amount
                    row['balance'] = "%.2f" % balance
                    new_balance = "%.2f" % balance
                    updated = True
                rows.append(row)
        if updated:
            # Write back to CSV
            with open('data/accounts.csv', 'w', newline='') as csvfile:
                fieldnames = ['pin', 'balance', 'withdrawal_limit']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return jsonify({"success": True, "new_balance": new_balance})

        return jsonify({"success": False, "message": "Account not found"})

    return account_transaction_blueprint