import pandas as pd


def load_dataframe(file_path):
    column_names = input('Есть ли название колонок в файле?\nЕсли есть, то просто введите Y\n'
                         'Eсли нет, то введите их через запятую: ').split(',')
    if len(column_names) == 1:
        return pd.read_csv(file_path)
    else:
        return pd.read_csv(file_path, names=column_names)


def get_statistic(df):
    statistic = []
    for column in df._get_numeric_data().columns:
        statistic.append((column, df[column].dtype,
                          df[column].min(), df[column].max(
        ), df[column].mean(),
                          df[column].median(), df[column].mode()[0],
                          df[column].isnull().sum() / df.shape[0] * 100,
                          df[column].var(),
                          df[column].std(),
                          # межквартильный интервал от -1,25 до 0,75
                          f'({df[column].quantile(q=0.25)}, {df[column].quantile(q=0.75)})',
                          # коэффициент вариации - отношение средне квадратического отклонения к среднему
                          df[column].std() / df[column].mean(),
                          df[column].nunique(),
                          # порой необходимо знать какую долю от общего
                          # количества значений признака занимает самый распространенный
                          df[column].value_counts(normalize=True).values[-1]
                          ))
    df_statistic = pd.DataFrame(statistic, columns=['column_name', 'column_type',
                                                    'min', 'max', 'mean', 'median', 'mode',
                                                    'percent of zero rows', 'variance',
                                                    'standard deviation',
                                                    'interquartile range', 'coefficient of variation',
                                                    'number of distinct values', 'part of common value'])
    return df_statistic


def save_result(out_type, out_name, df):
    if out_type == 'md':
        save_as_markdown(out_name, df)
    elif out_type == 'html':
        save_as_html(out_name, df)
    else:
        df.to_excel(out_name + '.xlsx', index=False)


def save_as_markdown(out_name, df):
    md_df = df.to_markdown()
    with open(out_name + '.md', 'w+') as out_file:
        out_file.writelines(md_df)


def save_as_html(out_name, df):
    html_df = df.to_html()
    with open(out_name + '.html', 'w+') as out_file:
        out_file.writelines(html_df)


if __name__ == '__main__':
    try:
        out_name, out_type = input('Имя выходного файла c разрешением (пример: file.txt): ').split('.')

        file_path = input('Введите путь к файлу с данными: ')

        data_frame = load_dataframe(file_path)
        df_stats = get_statistic(data_frame)
        save_result(out_type, out_name, df_stats)
    except Exception as ex:
        print(ex)
