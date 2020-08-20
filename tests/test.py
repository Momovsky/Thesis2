import unittest
import data_table
import psycopg2
import user
import gettoken


class Test(unittest.TestCase):

    def test_create_db(self):
        try:
            data_table.create_db()
        except psycopg2.OperationalError:
            self.fail('create_db() вызывает OperationalError, проверьте параметры подключения!')

    def test_wrong_id(self):
        test_user = user.User(123123123123123123123123132123, 'ae157a971b4aea656a03587d7682c492de3663fb9ac689cc9339afecd2c42ff24929d51ccd61a3d410878')
        self.assertRaises(KeyError, test_user.get_info)

    def test_token_link(self):
        self.assertEqual(gettoken.get_token(1), 'https://oauth.vk.com/authorize?client_id=1&scope=friends&display=page&response_type=token&v=5.89')