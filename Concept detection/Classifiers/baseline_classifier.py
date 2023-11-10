def compute_baseline_score(dataframe, label_column='label'):
    return dataframe.groupby(label_column).count().max().iloc[0] / len(dataframe)