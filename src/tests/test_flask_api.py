from flask_api import app
import unittest


# Adding very simple test cases. More test cases could be added for example mocking Exception etc.
class MyTestCase(unittest.TestCase):

    def test_hello(self):
        response = app.test_client().get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Up")

    def test_get_weather(self):
        with self.subTest("By default return 10 records"):
            response = app.test_client().get('api/weather')
            deta_ten = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(deta_ten), 10)

        with self.subTest("Count per page should return exact number"):
            response = app.test_client().get('api/weather?page=2&count_per_page=5')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 5)
            new_list = deta_ten[5:]
            self.assertEqual(new_list, data)

        with self.subTest("Filter based on year and weather station"):
            response = app.test_client().get('api/weather?wx_station=USC00110072&wx_date=19850101')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 1)

    def test_get_yield(self):
        with self.subTest("By default return 10 records"):
            response = app.test_client().get('api/yield')
            deta_ten = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(deta_ten), 10)

        with self.subTest("Count per page should return exact number"):
            response = app.test_client().get('api/yield?page=2&count_per_page=5')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 5)
            new_list = deta_ten[5:]
            self.assertEqual(new_list, data, "Paging is not working")

        with self.subTest("Filter based on year"):
            response = app.test_client().get('api/yield?yld_year=1985')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 1)

    def test_get_weather_stats(self):
        with self.subTest("By default return 10 records"):
            response = app.test_client().get('api/weather/stats')
            deta_ten = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(deta_ten), 10)

        with self.subTest("Count per page should return exact number"):
            response = app.test_client().get('api/weather/stats?page=2&count_per_page=5')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 5)
            new_list = deta_ten[5:]
            self.assertEqual(new_list, data)

        with self.subTest("Filter based on year and weather station"):
            response = app.test_client().get('api/weather/stats?wx_station=USC00110072&wx_year=1985')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 1)


if __name__ == '__main__':
    unittest.main()
