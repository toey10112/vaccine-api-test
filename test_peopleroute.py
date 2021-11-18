import unittest
import requests

# Author = Suchon Prasert

URL = "https://suchonsite-server.herokuapp.com/people"
schema = {
    '__v': 0,
    "_id": "617588258afc4f9aae4e8df5",
    "date": "23-10-2021",
    "people": [
        {
            "reservation_id": 6,
            "register_timestamp": "2021-10-23T06:44:25.849000",
            "name": "foo",
            "surname": "rockmakmak",
            "birth_date": "2002-10-22",
            "citizen_id": "1234567848204",
            "occupation": "programmer",
            "address": "bkk thailand",
            "priority": "3",
            "vac_time": 9
        }
    ],
}


class PeopleRouteTest(unittest.TestCase):

    def test_get_all_people(self):
        """

        Test ID: 1
        Test get all people work normally
        """
        api = URL + "/all"
        res = requests.get(api)
        self.assertEqual(200, res.status_code)

    def test_get_people_by_date(self):
        """

          Test ID: 2
          Test get people by date work normally
        """
        api = URL + "/by_date/23-10-2021"
        res = requests.get(api)
        self.assertEqual(200, res.status_code)
        self.assertEqual(schema, res.json())

    def test_get_people_by_wrong_date_format(self):
        """

        Test ID: 3
        Test get people by using wrong format date
        """
        api = URL + "/by_date/10-20-2021"
        # date format: m/d/y
        res = requests.get(api)
        self.assertEqual(404, res.status_code)

    def test_get_people_without_date(self):
        """

        Test ID: 4
        Test get people by date but without date input
        """
        api = URL + "/by_date/"
        res = requests.get(api)
        self.assertEqual(404, res.status_code)

    def test_get_people_by_date_without_data(self):
        """

        Test ID: 5
        Test get people by date without data
        """
        api = URL + "/by_date/24-10-2021"
        # Database doesn't have people appointment on this day
        res = requests.get(api)
        self.assertEqual(202, res.status_code)
        self.assertEqual("no date included", res.json())
        # So it should be empty

    def test_get_people_by_future_date(self):
        """

        Test ID: 6
        Test get people by date with future date
        """
        api = URL + "/by_date/24-10-2150"
        # Future date
        res = requests.get(api)
        self.assertEqual(202, res.status_code)
        self.assertEqual("", res.text)

    def test_delete_people_by_date_without_data(self):
        """

        Test ID: 7
        Test delete people by date but that date doesn't have data
        """
        api = URL + "/by_date/25-09-2021"
        # Database doesn't have people in this date
        res = requests.delete(api)
        self.assertEqual(202, res.status_code)
        self.assertEqual("no date included", res.json())

    def test_delete_people_by_date(self):
        """

        Test ID: 8
        Test delete people by date
        """
        api = URL + "/by_date/23-10-2021"
        res = requests.delete(api)
        self.assertEqual(200, res.status_code)
        self.assertEqual(schema, res.json())
