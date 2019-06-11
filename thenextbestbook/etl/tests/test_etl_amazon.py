import os
import sys
from subprocess import check_output
import pandas as pd
import unittest
# To make etl_amazon discoverable by tests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import etl_amazon as ea


class MyTest(unittest.TestCase):
    def test_read_row(self):
        etl = ea.ETLAmazon()
        test_file = etl.read_json("thenextbestbook/etl/tests/data/test_file.json.gz")
        test_file_pd = test_file.toPandas()
        test_file_truth = pd.read_json("thenextbestbook/etl/tests/data/test_file.json")
        self.assertEqual(test_file_pd.shape[0], test_file_truth.shape[0])

    def test_read_col(self):
        etl = ea.ETLAmazon()
        test_file = etl.read_json("thenextbestbook/etl/tests/data/test_file.json.gz")
        test_file_pd = test_file.toPandas()
        test_file_truth = pd.read_json("thenextbestbook/etl/tests/data/test_file.json")
        self.assertEqual(test_file_pd.shape[1], test_file_truth.shape[1])

    def test_sql_cmd(self):
        etl = ea.ETLAmazon()
        runs = etl.read_json("thenextbestbook/etl/tests/data/test_file.json.gz")
        runs.createGlobalTempView("runs")
        query_result = etl.sql_query(
            "SELECT COUNT(*)"
            "FROM global_temp.runs"
        )
        query_result_pd = query_result.toPandas()
        self.assertEqual(int(query_result_pd.iloc[0]), 263)


if __name__ == '__main__':
    unittest.main()
