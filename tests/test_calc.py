from app.calc import add, BankAccount
import pytest

@pytest.fixture
def class_instance():
    bank_acct = BankAccount(50)
    return bank_acct

@pytest.mark.parametrize("x, y, result", [(1,2,3), (2,2,4), (3,3,6)])
def test_add(x, y, result):
    sum = add(x, y)
    assert sum == result


def test_bank_set_inital_amt(class_instance):
    assert class_instance.balance == 50


def test_bank_default_initial_amt():
    bank_acct = BankAccount()
    assert bank_acct.balance == 0


def test_bank_deposit(class_instance):
    class_instance.deposit(50)
    assert class_instance.balance == 100


def test_bank_withdraw(class_instance):
    class_instance.withdraw(30)
    assert class_instance.balance == 20


def test_bank_interest(class_instance):
    class_instance.collect_interest()
    assert round(class_instance.balance, 2) == 55