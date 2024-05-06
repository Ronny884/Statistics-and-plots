import io
import json
import unittest
from statistics import Statistics


class TestStatistics(unittest.TestCase):
    def setUp(self):
        # Данные для тестирования метода подсчёта ошибок при вычислении количества углов
        data_1 = {
            "gt_corners": {"0": 4, "1": 5},
            "rb_corners": {"0": 4, "1": 5}
        }
        data_2 = {
            "gt_corners": {"0": 4, "1": 5},
            "rb_corners": {"0": 3, "1": 6.9}
        }  # различия в количестве комнат

        # Данные для тестирования методов проверки на нормальность и метода t-теста
        data_3 = {
            "column": {  # нормальное распределение
                '0': 9.5, '1': 10.2, '2': 11.8, '3': 9.9, '4': 10.5,
                '5': 11.0, '6': 10.7, '7': 9.8, '8': 10.3, '9': 11.2,
                '10': 10.0, '11': 9.7, '12': 10.9, '13': 11.5, '14': 10.4,
                '15': 9.6, '16': 11.3, '17': 10.8, '18': 11.1, '19': 10.6
            }
        }
        data_4 = {
            "column": {  # нормальное распределение отсутствует
                '0': 9.5, '1': 10.2, '2': 11.8, '3': 12.9, '4': 13.5,
                '5': 14.0, '6': 15.7, '7': 16.8, '8': 17.3, '9': 18.2,
                '10': 119.0, '11': 21110.7, '12': 21.9, '13': 22.5,
                '14': 21111111113.4, '15': 24.6, '16': 251111.3,
                '17': 26.8, '18': 27.1, '19': 28.6
            }
        }
        data_5 = {
            'column': {  # нормальное распределение
                '0': 11000, '1': 10000, '2': 11000, '3': 9000,
                '4': 10000, '5': 9000, '6': 8000, '7': 8000
            }
        }

        json_data_1 = io.StringIO(json.dumps(data_1))
        json_data_2 = io.StringIO(json.dumps(data_2))
        json_data_3 = io.StringIO(json.dumps(data_3))
        json_data_4 = io.StringIO(json.dumps(data_4))
        json_data_5 = io.StringIO(json.dumps(data_5))

        self.stats_1 = Statistics(json_data_1)
        self.stats_2 = Statistics(json_data_2)
        self.stats_3 = Statistics(json_data_3)
        self.stats_4 = Statistics(json_data_4)
        self.stats_5 = Statistics(json_data_5)

    def test_model_quality_assessment(self):
        self.assertEqual(self.stats_1.model_quality_assessment(), True)
        self.assertEqual(self.stats_2.model_quality_assessment(), False)

    def test_shapiro_test(self):
        self.assertEqual(self.stats_3.shapiro_test('column'), True)
        self.assertEqual(self.stats_4.shapiro_test('column'), False)
        self.assertEqual(self.stats_5.shapiro_test('column'), True)

    def test_pearsons_criterion_of_agreement(self):
        self.assertEqual(self.stats_3.pearsons_criterion_of_agreement('column'), True)
        self.assertEqual(self.stats_4.pearsons_criterion_of_agreement('column'), False)

    def test_t_test(self):
        self.assertEqual(self.stats_4.t_test('column'), True)
        self.assertEqual(self.stats_5.t_test('column'), True)


if __name__ == '__main__':
    unittest.main()

