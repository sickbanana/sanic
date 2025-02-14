import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = sa.Column(sa.types.Integer, primary_key=True, unique=True, autoincrement=True)
    full_name = sa.Column(sa.types.String, nullable=False)
    email = sa.Column(sa.types.String, unique=True, nullable=False)
    password_hash = sa.Column(sa.types.String, nullable=False)

    account = sa.orm.relationship("Account", backref="user")
    transaction = sa.orm.relationship("Transaction", backref="user")


class Admin(Base):
    __tablename__ = 'admin'

    admin_id = sa.Column(sa.types.Integer, primary_key=True, unique=True, autoincrement=True)
    full_name = sa.Column(sa.types.String, nullable=False)
    email = sa.Column(sa.types.String, unique=True, nullable=False)
    password_hash = sa.Column(sa.types.String, nullable=False)


class Account(Base):
    __tablename__ = 'account'

    account_id = sa.Column(sa.types.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = sa.Column(sa.types.Integer, sa.ForeignKey('user.user_id'), nullable=False)
    amount = sa.Column(sa.types.Integer, nullable=False)

    transaction = sa.orm.relationship("Transaction", backref="account")


class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id = sa.Column(sa.types.String, primary_key=True, unique=True)
    user_id = sa.Column(sa.types.Integer, sa.ForeignKey('user.user_id'), nullable=False)
    account_id = sa.Column(sa.types.Integer, sa.ForeignKey('account.account_id'), nullable=False)
    amount = sa.Column(sa.types.Integer, nullable=False)