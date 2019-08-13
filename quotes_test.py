import unittest
import random
import json
from quotes import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    def test_lambda_handler(self):
        """
        Test the lambda_handler function.
        """
        print(lambda_handler())


if __name__ == "__main__":
    unittest.main()
