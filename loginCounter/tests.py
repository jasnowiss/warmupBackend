import json
import unittest
from django.test import Client
from django.test import TestCase

# Create your tests here.

class WarmupTests(TestCase):

    def setUp(self):
        self.c = Client()

        self.j1 = json.dumps({'username':'jeff1','pwd':'1234'})
        self.j2 = json.dumps({'username':'snow2','pwd':'1234'})

        self.j3 = json.dumps({'username':'jeff3','pwd':'abcd'})
        self.j4 = json.dumps({'username':'snow4','pwd':'abcd'})

        self.j5 = json.dumps({'username':'jeff5','pwd':'5678'})
        self.j6 = json.dumps({'username':'jeff5','pwd':'efgh'})

        self.j7 = json.dumps({'username':'jeff7','pwd':'stuff'})
        self.j8 = json.dumps({'username':'snow8','pwd':'stuff2'})

        self.j9 = json.dumps({'username':'jefflaksdjflakwejljdoiajsklfjsoiejalkdjalkfjoiawejlfajsdfliakjeaoisjflkdsjfasodiafjaelkfjalwekjfoiawlejflaskjfszdoifjldkjfaeoijfasdlkjflkaerjfioaelkjflkdjffoiaejlksflkdajfaoisejklrfldksjfasdoifjelaksjrasdlkjieo','pwd':'hi'})
        self.j10 = json.dumps({'username':'','pwd':'hi2'})

        self.j11 = json.dumps({'username':'jeff11','pwd':'stuffaslkdfjealksdlkfsdoxclzjklxkljewalrjelkajflskdjfoixcjvzlkjflkejaroiewjklxcjzvioeajwkljzxcoivjelakfjoxcijfklaewjoivdxjkalewjfozivjlkaejfiozxcjlkfjeaoijzxclkfjalkejrioesajzxlkjzlkjfoieajflkzjlkz'})
        self.j12 = json.dumps({'username':'snow12','pwd':'laweslakdfjklxcjoiekljskljkahsfdkjhlkaekjhakejfhaesldjhfsjkadhfeiuwnxcvneasfdskjfhsdakjhcxkjhekjanfkjdnvkjanfkejshkjdhvkjxchkjxhejkhkjahejkheskjhvcjkhxzkjfdhskjaehjkhsaefjkhsadkjhxckjvhdkjhewakjrhs'})

        self.j13 = json.dumps({'username':'jeff13','pwd':'count1'})
        self.j14 = json.dumps({'username':'snow14','pwd':'count2'})

        self.j15 = json.dumps({'username':'jeff15','pwd':'status1'})
        self.j16 = json.dumps({'username':'snow16','pwd':'status2'})

        self.j17 = json.dumps({'username':'jeff17','pwd':'countlarge'})

    def test_index(self):
        response = self.c.get('/users/')
        self.assertEqual(response.content, "Hello, world. You're at the user index.")

    def test_usernameError(self): # j1, j2
        response = self.c.post('/users/login/', self.j1, content_type="application/json")
        self.assertEqual(response.content, '{"errCode": -1}')
        response = self.c.post('/users/login/', self.j2, content_type="application/json")
        self.assertEqual(response.content, '{"errCode": -1}')

    def test_add(self): # j3, j4
        response = self.c.post('/users/add/', self.j3, content_type="application/json")
        self.assertEqual(response.content, '{"count": 1, "errCode": 1}')
        response = self.c.post('/users/add/', self.j4, content_type="application/json")
        self.assertEqual(response.content, '{"count": 1, "errCode": 1}')

    def test_passwordError(self): # j5, j6
        response = self.c.post('/users/add/', self.j5, content_type="application/json")
        self.assertEqual(response.content, '{"count": 1, "errCode": 1}')
        response = self.c.post('/users/add/', self.j6, content_type="application/json")
        self.assertEqual(response.content, '{"errCode": -2}')

    def test_login(self): # j7, j8
        response = self.c.post('/users/add/', self.j7, content_type="application/json")
        self.assertEqual(response.content, '{"count": 1, "errCode": 1}')
        response = self.c.post('/users/add/', self.j8, content_type="application/json")
        self.assertEqual(response.content, '{"count": 1, "errCode": 1}')
        response = self.c.post('/users/login/', self.j7, content_type="application/json")
        self.assertEqual(response.content, '{"count": 2, "errCode": 1}')
        response = self.c.post('/users/login/', self.j8, content_type="application/json")
        self.assertEqual(response.content, '{"count": 2, "errCode": 1}')

    def test_usernameLength(self): # j9, j10
        response = self.c.post('/users/add/', self.j9, content_type="application/json")
        self.assertEqual(response.content, '{"errCode": -3}')
        response = self.c.post('/users/add/', self.j10, content_type="application/json")
        self.assertEqual(response.content, '{"errCode": -3}')

    def test_passwordLength(self): # j11, j12
        response = self.c.post('/users/add/', self.j11, content_type="application/json")
        self.assertEqual(response.content, '{"errCode": -4}')
        response = self.c.post('/users/add/', self.j12, content_type="application/json")
        self.assertEqual(response.content, '{"errCode": -4}')

    def test_small_count(self): # j13, j14
        response = self.c.post('/users/add/', self.j13, content_type="application/json")
        self.assertEqual(response.content, '{"count": 1, "errCode": 1}')
        response = self.c.post('/users/add/', self.j14, content_type="application/json")
        self.assertEqual(response.content, '{"count": 1, "errCode": 1}')
        response = self.c.post('/users/login/', self.j13, content_type="application/json")
        self.assertEqual(response.content, '{"count": 2, "errCode": 1}')
        response = self.c.post('/users/login/', self.j14, content_type="application/json")
        self.assertEqual(response.content, '{"count": 2, "errCode": 1}')
        response = self.c.post('/users/login/', self.j13, content_type="application/json")
        self.assertEqual(response.content, '{"count": 3, "errCode": 1}')
        response = self.c.post('/users/login/', self.j14, content_type="application/json")
        self.assertEqual(response.content, '{"count": 3, "errCode": 1}')
        response = self.c.post('/users/login/', self.j13, content_type="application/json")
        self.assertEqual(response.content, '{"count": 4, "errCode": 1}')
        response = self.c.post('/users/login/', self.j14, content_type="application/json")
        self.assertEqual(response.content, '{"count": 4, "errCode": 1}')

    def test_large_count(self): # j17
        response = self.c.post('/users/add/', self.j17, content_type="application/json")
        for i in range(0, 9):
            response = self.c.post('/users/login/', self.j17, content_type="application/json")
        self.assertEqual(response.content, '{"count": 10, "errCode": 1}')
        for i in range(0, 90):
            response = self.c.post('/users/login/', self.j17, content_type="application/json")
        self.assertEqual(response.content, '{"count": 100, "errCode": 1}')
        for i in range(0, 900):
            response = self.c.post('/users/login/', self.j17, content_type="application/json")
        self.assertEqual(response.content, '{"count": 1000, "errCode": 1}')

    def test_statusCode(self): # j15, j16
        response = self.c.post('/users/login/', self.j15, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.c.post('/users/login/', self.j16, content_type="application/json")
        self.assertEqual(response.status_code, 200)


