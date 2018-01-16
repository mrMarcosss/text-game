from django.test import TestCase
from django.urls import reverse


class GameTestCase(TestCase):

    def test_main_page(self):
        response = self.client.get(reverse('main'))
        button = '<a href="' + reverse('choose_gender') + '" class="btn btn-success btn-lg start-button">start the game</a>'
        self.assertContains(response, button, status_code=200)

    def test_start_page(self):
        response = self.client.get(reverse('start'))
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertIn('rating', session)
        self.assertEqual(session['rating'], 0)

    def test_gender_page(self):
        response = self.client.get(reverse('choose_gender'))
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertNotIn('gender', session)
        response = self.client.post(reverse('choose_gender'), {'gender': '0'})
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertIn('gender', session)
        self.assertEqual(session['gender'], 0)

    def test_make_research(self):
        response = self.client.get(reverse('make_research'))
        self.assertEqual(response.status_code, 302)
        self.client.get(reverse('start'))
        response = self.client.get(reverse('make_research'))
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertIn('rating', session)
        self.assertEqual(session['rating'], 25)

    def test_response_from_companies(self):
        self.client.get(reverse('start'))
        self.client.get(reverse('make_research'))
        response = self.client.get(reverse('response_from_companies'))
        session = self.client.session
        self.assertIn('rating', session)
        self.assertEqual(session['rating'], 75)

    def test_choose_company_1(self):
        self.client.get(reverse('choose_gender'))
        self.client.post(reverse('choose_gender'), {'gender': '0'})
        self.client.get(reverse('start'))
        self.client.get(reverse('make_research'))
        self.client.get(reverse('response_from_companies'))
        response = self.client.post(reverse('choose_company'), {'company': '1'})
        self.assertEqual(response.status_code, 200)
        response_str = str(response.content, encoding='utf8')
        self.assertTrue('"status": "not so bad"' in response_str)
        self.assertTrue('You not so bad!' in response_str)
        self.assertTrue('Restart :)' in response_str)
        session = self.client.session

    def test_choose_company_2(self):
        self.client.get(reverse('choose_gender'))
        self.client.post(reverse('choose_gender'), {'gender': '0'})
        self.client.get(reverse('start'))
        self.client.get(reverse('make_research'))
        self.client.get(reverse('response_from_companies'))
        response = self.client.post(reverse('choose_company'), {'company': '2'})
        self.assertEqual(response.status_code, 200)
        response_str = str(response.content, encoding='utf8')
        self.assertTrue('"status": "win"' in response_str)
        self.assertTrue('You win!' in response_str)
        self.assertTrue('Restart :)' in response_str)
        session = self.client.session
        self.assertEqual(session['rating'], 100)

    def test_choose_company_3(self):
        self.client.get(reverse('choose_gender'))
        self.client.post(reverse('choose_gender'), {'gender': '0'})
        self.client.get(reverse('start'))
        self.client.get(reverse('make_research'))
        self.client.get(reverse('response_from_companies'))
        response = self.client.post(reverse('choose_company'), {'company': '3'})
        self.assertEqual(response.status_code, 200)
        response_str = str(response.content, encoding='utf8')
        self.assertTrue('"status": "lose"' in response_str)
        self.assertTrue('You lose!' in response_str)
        self.assertTrue('Restart :)' in response_str)
        session = self.client.session
        self.assertNotIn('rating', session)

    def test_choose_company_error(self):
        self.client.get(reverse('choose_gender'))
        self.client.post(reverse('choose_gender'), {'gender': '0'})
        self.client.get(reverse('start'))
        self.client.get(reverse('make_research'))
        self.client.get(reverse('response_from_companies'))
        response = self.client.post(reverse('choose_company'), {'company': 'error'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Company value must be a number!'}
        )

    def test_get_drink_coffee(self):
        self.client.get(reverse('main'))
        response = self.client.get(reverse('drink_coffee'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'cups': 0}
        )

    def test_add_drink_coffee(self):
        self.client.get(reverse('main'))
        self.client.post(reverse('drink_coffee'))
        self.client.post(reverse('drink_coffee'))
        response = self.client.post(reverse('drink_coffee'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'cups': 3}
        )

    def test_stay_in_company(self):
        self.client.post(reverse('choose_gender'), {'gender': '0'})
        self.client.get(reverse('start'))
        self.client.get(reverse('stay_in_company'))
        session = self.client.session
        self.assertEqual(session['rating'], 10)

    def test_recruiter(self):
        self.client.post(reverse('choose_gender'), {'gender': '0'})
        self.client.get(reverse('start'))
        self.client.get(reverse('recruiter'))
        session = self.client.session
        self.assertEqual(session['rating'], 20)
