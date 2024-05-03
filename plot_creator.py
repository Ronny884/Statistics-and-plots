import os
import os.path
import pandas as pd
import matplotlib.pyplot as plt


class PlotCreator:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    necessary_deviation_columns = (
        'mean', 'max', 'min',
        'ceiling_mean', 'ceiling_max', 'ceiling_min',
        'floor_mean', 'floor_max', 'floor_min'
    )

    def create_plots_folder(self):
        plots_dir = os.path.join(self.ROOT_DIR, 'plots')

        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
            print(f'Папка "plots" успешно создана в корневой директории')

    def draw_plots(self, json):
        paths = []

        df = pd.read_json(json, orient='records')
        self.create_plots_folder()

        # График точности модели при подсчёте количества комнат
        plt.figure(figsize=(10, 6))
        plt.scatter(df['gt_corners'], df['rb_corners'], color='b', label='Predicted vs. Real')
        plt.xlabel('gt_corners')
        plt.ylabel('rb_corners')
        plt.title('Comparison of Real vs. Predicted Angles')
        path = os.path.join(self.ROOT_DIR, 'plots/room_count_estimation.png')
        plt.savefig(path)
        paths.append(path)
        plt.cla()

        for column in self.necessary_deviation_columns:
            # Построение гистограмм для каждого столбца отклонения
            plt.hist(df[column], bins=100, linewidth=1)
            plt.xlabel('Величина отклонения')
            plt.ylabel('Частота')
            plt.title(f'Распределение отклонений ({column})')
            path = os.path.join(self.ROOT_DIR, f'plots/histogram_{column}.png')
            plt.savefig(path)
            paths.append(path)
            plt.cla()

            # Построение диаграмм рассеяния для каждого столбца отклонения
            plt.scatter(df[column], df['name'], s=8)
            plt.gca().get_yaxis().set_ticks([])
            plt.xlabel('Величина отклонения')
            plt.title(f'Диаграмма рассеяния ({column})')
            path = os.path.join(self.ROOT_DIR, f'plots/scatter_plot_{column}.png')
            plt.savefig(path)
            paths.append(path)
            plt.cla()

        print('Пути к графикам:')
        for path in paths:
            print(path)
        print('=' * 100)

        return paths

