import scipy
import sklearn
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.metrics import mean_absolute_error, mean_squared_error


class Statistics:
    def __init__(self, json):
        self.df = pd.read_json(json, orient='records')

    def get_describe_statistic(self, column=None):
        # Описательная статистика
        if column is None:
            print('Описательная статистика всех данных:')
            describe = self.df.describe()
        else:
            print(f'Описательная статистика для столбца {column}:')
            describe = self.df[column].describe()
        print(describe, '\n', '=' * 100)

    def model_quality_assessment(self):
        # Подсчёт ошибок при вычислении количества углов комнаты
        mae = mean_absolute_error(self.df['gt_corners'], self.df['rb_corners'])
        mse = mean_squared_error(self.df['gt_corners'], self.df['rb_corners'])
        print('Подсчёт ошибок при вычислении количества углов комнаты:', '\n')
        print(f'Средняя абсолютная ошибка (MAE): {mae:.2f}')
        print(f'Среднеквадратичная ошибка (MSE): {mse:.2f}')
        if mae == 0 and mse == 0:
            print('Модель успешно справилась с вычислением количества углов', '\n', '=' * 100)
            return True
        else:
            print('Модель вычислила количество углов с некоторыми погрешностями', '\n', '=' * 100)
            return False

    def shapiro_test(self, column):
        # Тест Шапиро-Уилка
        stat, p = scipy.stats.shapiro(self.df[column])
        print(f'Тест Шапиро-Уилка для столбца {column}:', '\n')
        print(f'Statistics={stat:.3f}, p-value={p:.3f}')

        alpha = 0.05
        if p > alpha:
            print('Принять гипотезу о нормальности', '\n', '=' * 100)
            return True
        else:
            print('Отклонить гипотезу о нормальности', '\n', '=' * 100)
            return False

    def pearsons_criterion_of_agreement(self, column):
        # Критерий согласия Пирсона
        stat, p = scipy.stats.normaltest(self.df[column])
        print(f'Критерий согласия Пирсона для столбца {column}:', '\n')
        print(f'Statistics={stat:.3f}, p-value={p:.3f}')

        alpha = 0.05
        if p > alpha:
            print('Принять гипотезу о нормальности', '\n', '=' * 100)
            return True
        else:
            print('Отклонить гипотезу о нормальности', '\n', '=' * 100)
            return False

    def t_test(self, column):
        # Тест Стьюдента (при условии нормального распределения)
        half = len(self.df[column]) // 2
        sam1 = self.df.loc[:half, column]
        sam2 = self.df.loc[half:, column]
        t_statistic = scipy.stats.ttest_ind(sam2, sam1)
        print(f'Тест Стьюдента для столбца {column} (при условии нормального распределения):', '\n')
        print(t_statistic)
        dfs = (half - 1) + (half - 1)
        table_value = scipy.stats.t.ppf(0.975, dfs)
        if t_statistic.statistic < table_value:
            print('Средние двух выборок равны при условии их нормального распределения', '\n', '=' * 100)
            return True
        else:
            return False

    def line_regression(self, dependent_column, independent_columns):
        # Линейная регрессия
        formula = f'{dependent_column} ~ {" + ".join(independent_columns)}'
        model = smf.ols(formula, data=self.df)
        res = model.fit()
        print(f'Линейная регрессия для столбца {dependent_column} относительно {", ".join(independent_columns)}:', '\n')
        print(res.summary(), '\n')

