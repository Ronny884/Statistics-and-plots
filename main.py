import cProfile
from memory_profiler import profile
from statistics import Statistics
from plot_creator import PlotCreator


@profile
def main():
    url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'

    # Построение и сохранение графиков, возврат и печать путей к ним
    pc = PlotCreator()
    paths = pc.draw_plots(url)

    st = Statistics(url)

    # Описательные характеристики для всех столбцов
    columns_to_describe = [
        'name', 'gt_corners', 'rb_corners',
        'mean', 'max', 'min',
        'floor_mean', 'floor_max', 'floor_min',
        'ceiling_mean', 'ceiling_max', 'ceiling_min'
    ]
    for column in columns_to_describe:
        st.get_describe_statistic(column)

    # Оценка точности модели при подсчёте количества углов комнаты
    st.model_quality_assessment()

    # Проверка на нормальность результатов отклонений: тест Шапиро-Уилка и критерий согласия Пирсона
    necessary_deviation_columns_for_normality_test = [
        'mean', 'max', 'min',
        'ceiling_mean', 'ceiling_max', 'ceiling_min',
        'floor_mean', 'floor_max', 'floor_min'
    ]
    for column in necessary_deviation_columns_for_normality_test:
        test_1 = st.shapiro_test(column)
        test_2 = st.pearsons_criterion_of_agreement(column)
        if test_1 and test_2:
            # Тест Стьюдента при условии нормального распределения
            st.t_test(column)

    # Линейная регрессия для оценки взаимосвязи между количеством комнат и общей величиной отклонений
    st.line_regression('gt_corners', ['mean', 'min', 'max'])

    # Взаимосвязи между величинами отклонений для пола и потолка
    st.line_regression('floor_min', ['ceiling_min'])
    st.line_regression('floor_max', ['ceiling_max'])
    st.line_regression('floor_mean', ['ceiling_mean'])
    st.line_regression('min', ['ceiling_min', 'floor_min'])
    st.line_regression('max', ['ceiling_max', 'floor_max'])
    st.line_regression('mean', ['ceiling_mean', 'floor_mean'])


if __name__ == '__main__':
    # main()
    cProfile.run('main()')




