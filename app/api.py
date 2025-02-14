from sanic import Blueprint, response
from sanic_validation import validate_json
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError

from utils import *
from json_validators import user_schema, update_user_schema, transaction_schema, login_user_schema
from settings import SECRET_KEY

users_blueprint = Blueprint('users_blueprint', url_prefix='/user')
admin_blueprint = Blueprint('admin_blueprint', url_prefix='/admin')


@users_blueprint.route('/register', methods=['POST'])
@validate_json(user_schema)
async def register(request):
    full_name = request.json.get('full_name')
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        session = request.ctx.session
        async with session.begin():
            user = await session.execute(insert(User).values(
                full_name=full_name,
                email=email,
                password_hash=generate_password_hash(password)))
            token = generate_token(user.inserted_primary_key[0], 'user')
            return response.json({
                'message': "Logged in successfully",
                'token': token
            })
    except IntegrityError:
        return response.json(
            {'error': {'message': 'non-unique email'}},
            status=400
        )


@users_blueprint.route('/login', methods=['POST'])
@validate_json(login_user_schema)
async def register(request):
    email = request.json.get('email')
    password = request.json.get('password')
    session = request.ctx.session
    async with session.begin():
        result = await session.execute(select(User.user_id, User.password_hash).where(User.email == email))
        user = result.first()
        if verify_password(user[1], password):
            token = generate_token(user[0], 'user')
            return response.json({
                'message': "Logged in successfully",
                'token': token
            })
        return response.json(
            {'error': {'message': 'Login error'}},
            status=401
        )


@users_blueprint.route('/get_profile_info', methods=['GET'])
@check_token
async def get_profile_info(request, user):
    return response.json({'id': user[0], 'full_name': user[1], 'email': user[2]})


@users_blueprint.route('/get_accounts', methods=['GET'])
@check_token
async def get_accounts(request, user):
    user_id = user[0]
    session = request.ctx.session
    async with session.begin():
        result = await session.execute(select(Account.account_id, Account.amount).where(
            Account.user_id == user_id))
        accounts = result.all()
        return response.json({
            'accounts': [{'account_id': account_id, 'amount': amount} for account_id, amount in accounts]
        })


@users_blueprint.route('/get_transactions', methods=['GET'])
@check_token
async def get_transactions(request, user):
    user_id = user[0]
    session = request.ctx.session
    async with session.begin():
        result = await session.execute(select(Transaction.transaction_id, Transaction.account_id, Transaction.amount).where(
            Transaction.user_id == user_id))
        transactions = result.all()
        return response.json({
            'accounts': [{'transaction_id': transaction_id, 'account_id': account_id, 'amount': amount} for
                         transaction_id, account_id, amount in transactions]
        })


@users_blueprint.route('/transaction_processing', methods=['POST'])
@validate_json(transaction_schema)
async def transaction_processing(request):
    transaction_id = request.json.get('transaction_id')
    user_id = request.json.get('user_id')
    account_id = request.json.get('account_id')
    amount = request.json.get('amount')
    signature = request.json.get('signature')

    if signature != hashlib.sha256(str(account_id).encode() + str(amount).encode() + transaction_id.encode() + str(
            user_id).encode() + SECRET_KEY.encode()).hexdigest():
        return response.json({
            'message': "incorrect signature",
        })

    try:
        session = request.ctx.session
        async with session.begin():
            result = await session.execute(select(Account).where(
                Account.account_id == account_id, Account.user_id == user_id))
            if len(result.all()) < 1:
                await session.execute(insert(Account).values(account_id=account_id, user_id=user_id, amount=0))
            await session.execute(insert(Transaction).values(transaction_id=transaction_id, user_id=user_id,
                                                             account_id=account_id, amount=amount))
            await session.execute(update(Account).where(Account.account_id == account_id).values(
                amount=Account.amount + amount))

        return response.json({
            'message': "transaction processed",
        })
    except IntegrityError:
        return response.json(
            {'error': {'message': 'non-unique transaction'}},
            status=400
        )


@admin_blueprint.route('/register', methods=['POST'])
@validate_json(user_schema)
async def register(request):
    full_name = request.json.get('full_name')
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        session = request.ctx.session
        async with session.begin():
            admin = await session.execute(insert(Admin).values(
                full_name=full_name,
                email=email,
                password_hash=generate_password_hash(password)))
            token = generate_token(admin.inserted_primary_key[0], 'admin')
            return response.json({
                'message': "Logged in successfully",
                'token': token
            })
    except IntegrityError:
        return response.json(
            {'error': {'message': 'non-unique email'}},
            status=400
        )


@admin_blueprint.route('/login', methods=['POST'])
@validate_json(login_user_schema)
async def register(request):
    email = request.json.get('email')
    password = request.json.get('password')
    session = request.ctx.session
    async with session.begin():
        result = await session.execute(select(Admin.admin_id, Admin.password_hash).where(Admin.email == email))
        admin = result.first()
        if verify_password(admin[1], password):
            token = generate_token(admin[0], 'admin')
            return response.json({
                'message': "Logged in successfully",
                'token': token
            })
        return response.json(
            {'error': {'message': 'Login error'}},
            status=401
        )


@admin_blueprint.route('/get_profile_info', methods=['GET'])
@check_token
async def get_profile_info(request, admin):
    return response.json({'id': admin[0], 'full_name': admin[1], 'email': admin[2]})


@admin_blueprint.route('/create_user', methods=['POST'])
@validate_json(user_schema)
@check_token
async def create_user(request, admin):
    full_name = request.json.get('full_name')
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        session = request.ctx.session
        async with session.begin():
            user = await session.execute(insert(User).values(
                full_name=full_name,
                email=email,
                password_hash=generate_password_hash(password)))
            return response.json({
                'message': "user created successfully",
                'user_id': user.inserted_primary_key[0]
            })
    except IntegrityError:
        return response.json(
            {'error': {'message': 'non-unique email'}},
            status=400
        )


@admin_blueprint.route('/delete_user/<user_id:int>', methods=['DELETE'])
@check_token
async def delete_user(request, admin, user_id: int):
    try:
        session = request.ctx.session
        async with session.begin():
            await session.execute(delete(User).where(User.user_id == user_id))
            return response.json({
                'message': "user deleted successfully"
            })
    except IntegrityError:
        return response.json(
            {'error': {'message': 'user referenced from other table'}},
            status=400
        )


@admin_blueprint.route('/update_user', methods=['PUT'])
@validate_json(update_user_schema)
@check_token
async def update_user(request, admin):
    user_id = request.json.get('user_id')
    values = {}
    if 'full_name' in request.json:
        values['full_name'] = request.json['full_name']
    if 'email' in request.json:
        values['email'] = request.json['email']
    if 'password' in request.json:
        password = request.json.get('password')
        values['password_hash'] = generate_password_hash(password)
    try:
        session = request.ctx.session
        async with session.begin():
            await session.execute(update(User).where(User.user_id == user_id).values(**values))
            return response.json({
                'message': "user updated successfully"
            })
    except IntegrityError:
        return response.json(
            {'error': {'message': 'non-unique email'}},
            status=400
        )


@admin_blueprint.route('/get_users', methods=['GET'])
@check_token
async def get_accounts(request, admin):
    session = request.ctx.session
    async with session.begin():
        result = await session.execute(select(User.user_id, User.full_name, User.email, Account.account_id, Account.amount).select_from(User).join(Account, isouter=True))
        accounts = result.all()
        users = []
        for row in accounts:
            if len(users) > 0 and row[0] != users[-1]['user_id'] or len(users) == 0:
                users.append({'user_id': row[0], 'full_name': row[1], 'email': row[2], 'accounts': []})
                if row[3]:
                    users[-1]['accounts'].append({'account_id': row[3], 'amount': row[4]})
            else:
                users[-1]['accounts'].append({'account_id': row[3], 'amount': row[4]})
        return response.json({
            'users': users
        })