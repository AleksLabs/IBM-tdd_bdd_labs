"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)
        
    def test_repr(self):
        """ Test __repr__ method"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.name = "Foo"
        self.assertEqual(str(account), "<Account 'Foo'>")
    
    def test_to_dict(self):
        """ Test Serializing the class as a dictionary"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(account.to_dict(), {
            "id": account.id,
            "name": account.name,
            "email": account.email,
            "phone_number": account.phone_number,
            "disabled": account.disabled,
            "date_joined": account.date_joined
            })
        
    def test_from_dict(self):
        """ Test Setting attributes from a dictionary"""
        data = {
        "name": "Jennifer Smith",
        "email": "stevensjennifer@example.org",
        "phone_number": "351.317.1639x79470",
        "disabled": True
        }   
        account = Account()
        account.from_dict(data)
        self.assertEqual(account.name, "Jennifer Smith")
        self.assertEqual(account.email, "stevensjennifer@example.org")
        self.assertEqual(account.phone_number, "351.317.1639x79470")
        self.assertEqual(account.disabled, True)

    def test_update(self):
        """ Test Updating an Account in the database"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        account = Account.find(1)
        account.name = "Foo"
        account.update()
        account = Account.find(1)
        self.assertEqual(account.name, "Foo")

    def test_delete(self):
        """ Test deleting an Account in the database"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        account = Account.find(1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_update_no_id_error(self):
        """ Test raising DataValidationError"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        account = Account.find(1)
        account.id = None
        self.assertRaises(DataValidationError, account.update)