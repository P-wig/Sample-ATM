from flask import Blueprint, render_template, session, jsonify


def get_blueprint():
    account_transaction_blueprint = Blueprint('account_transaction', __name__, url_prefix='/account')

    @account_transaction_blueprint.route('/', methods=['GET'])
    def render_account_page():
        return render_template('account.html')

    @account_transaction_blueprint.route('/balance', methods=['GET'])
    def get_balance():
        return {"balance": 1000} # Placeholder implementation

    return account_transaction_blueprint