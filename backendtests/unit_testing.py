import unittest
from time import sleep
from faker import Faker

from clientside.resources import User_Requests

data_gen = Faker(['en_GB'])

class TestUser():

    def __init__(self):
        self._user_info = self.get_user_info()
        self._resp = User_Requests.create(self._user_info)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sleep(5)
        resp = User_Requests.delete(
            self._resp['data']['User_ID'], 
            self._resp['access_token']
        )
        if resp is not None:
            print('Deleted User: {id}, {fname} {lname}'.format(
                id=self._resp['data']['User_ID'],
                fname=self._user_info['First_Name'],
                lname=self._user_info['Last_Name']
            ))
        else:
            print('Failed to deleted User: {id}, {fname} {lname}'.format(
                id=self._resp['data']['User_ID'],
                fname=self._user_info['First_Name'],
                lname=self._user_info['Last_Name']
            ))

    def get_user_info(self):
        name = data_gen.name().split()
        First_Name, Last_Name = name if len(name) == 2 else name[1:3]
        Email = '{l_name}.{f_letter}@university.ac.uk'.format(l_name=Last_Name.lower(), f_letter=First_Name[0].lower())
        DateOfBirth = str(data_gen.date_of_birth(minimum_age=18, maximum_age=21))
        Password = data_gen.password()
        return {
            'Email':Email,
            'Password':Password,
            'First_Name':First_Name,
            'Last_Name':Last_Name,
            'DateOfBirth':DateOfBirth,
        }

class TestUserFunctions(unittest.TestCase):

    def test_user_creation(self):
        with TestUser() as output:
            print(output._resp)
            self.assertIsNotNone(output._resp)
    
    def test_user_login_manual(self):
        with TestUser() as user:
            output = User_Requests.login({
                'Email':user._user_info['Email'],
                'Password':user._user_info['Password']
            })
            print(output)
            self.assertIsNotNone(output)
    
    def test_user_login_auto(self):
        with TestUser() as user:
            output = User_Requests.login(
                {}, 
                auth_token=user._resp['access_token']
            )
            print(output)
            self.assertIsNotNone(output)
    
    # def test_user_delete(self):
    #     with TestUser() as user:       

if __name__ == "__main__":
    unittest.main()