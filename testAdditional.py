import unittest
import os
import testLib

class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAdd(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'username' : 'user1', 'pwd' : 'pass1'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/add", method="POST", data = { 'username' : 'user1-1', 'pwd' : 'pass1-1'} )
        self.assertResponse(respData, count = 1)

    def testUsernameError(self):
        respData = self.makeRequest("/users/login", method="POST", data = {'username' : 'user2', 'pwd' : 'pass2'} )
        self.assertResponse(respData, errCode = -1)

    def testPasswordError(self):
        respData = self.makeRequest("/users/add", method="POST", data = {'username' : 'user3', 'pwd' : 'pass3'} )
        self.assertResponse(respData, errCode = 1)
        respData = self.makeRequest("/users/add", method="POST", data = {'username' : 'user3', 'pwd' : 'pass3'} )
        self.assertResponse(respData, errCode = -2)

    def testLogin(self):
        respData = self.makeRequest("/users/add", method="POST", data = {'username' : 'user4', 'pwd' : 'pass4'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/login", method="POST", data = {'username' : 'user4', 'pwd' : 'pass4'} )
        self.assertResponse(respData, count = 2)

    def testSmallCount(self):
        respData = self.makeRequest("/users/add", method="POST", data = {'username' : 'user5', 'pwd' : 'pass5'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/login", method="POST", data = {'username' : 'user5', 'pwd' : 'pass5'} )
        self.assertResponse(respData, count = 2)
        respData = self.makeRequest("/users/login", method="POST", data = {'username' : 'user5', 'pwd' : 'pass5'} )
        self.assertResponse(respData, count = 3)
        respData = self.makeRequest("/users/login", method="POST", data = {'username' : 'user5', 'pwd' : 'pass5'} )
        self.assertResponse(respData, count = 4)
        respData = self.makeRequest("/users/login", method="POST", data = {'username' : 'user5', 'pwd' : 'pass5'} )
        self.assertResponse(respData, count = 5)

    def testLargeCount(self):
        respData = self.makeRequest("/users/add", method="POST", data = {'username' : 'user6', 'pwd' : 'pass6'} )
        self.assertResponse(respData, count = 1)
        for i in range(0, 9):
            respData = self.makeRequest("/users/add", method="POST", data = {'username' : 'user6', 'pwd' : 'pass6'} )
        self.assertResponse(respData, count = 10)
        for i in range(0, 90):
            respData = self.makeRequest("/users/add", method="POST", data = {'username' : 'user6', 'pwd' : 'pass6'} )
        self.assertResponse(respData, count = 100)
        for i in range(0, 400):
            respData = self.makeRequest("/users/add", method="POST", data = {'username' : 'user6', 'pwd' : 'pass6'} )
        self.assertResponse(respData, count = 500)
