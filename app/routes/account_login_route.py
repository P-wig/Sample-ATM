from flask import Blueprint, request, session, render_template, redirect, url_for
import csv

def validate_pin(pin):
    with open('data/accounts.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['pin'] == pin:
                return True
    return False

def get_blueprint():
    account_login_blueprint = Blueprint('account_login', __name__, url_prefix='')

    @account_login_blueprint.route('/', methods=['GET'])
    def render_login_page():
        return render_template('login.html')

    @account_login_blueprint.route('/login', methods=['POST'])
    def login():
        """
        User login with PIN
        ---
        parameters:
          - name: pin
            in: formData
            type: string
            required: true
        responses:
          200:
            description: Login successful
          401:
            description: Invalid PIN
        """
        pin = request.form.get('pin')
        if validate_pin(pin):
            session['pin'] = pin
            return redirect(url_for('account_transaction.render_account_page'))
        return render_template('login.html', show_error=True)

    @account_login_blueprint.route('/logout', methods=['GET'])
    def logout():
        """
        User logout
        ---
        responses:
          200:
            description: Logout successful
        """
        session.pop('pin', None)
        return redirect(url_for('account_login.render_login_page'))

    return account_login_blueprint