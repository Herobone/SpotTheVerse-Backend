import unittest
from src import index


class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("testing response.")
        result = index.handler()
        print(result)
        self.assertEqual(result[1], 200)
        self.assertEqual(result[2]['Content-Type'], 'application/json')
        self.assertIn('Hello World 2', result[0])


if __name__ == '__main__':
    unittest.main()
