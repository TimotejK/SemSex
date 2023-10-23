import time
import warnings

import numpy as np
import pandas as pd

import threading
def split_data(df, oversample=False, label_name='class', train_size=0.6, val_size=0.2, split_by_documents=True):
    groups = df.groupby(label_name)
    number_of_groups = 3
    number_of_relations = len(groups)
    final_dataframes = [None for _ in range(number_of_groups)]
    # train_df = None
    # val_df = None
    # test_df = None
    warnings.filterwarnings("ignore", category=FutureWarning)
    if split_by_documents:
        df = df.sort_values(by=['document_id'])
        border1 = int(train_size * len(df))
        border2 = int((train_size + val_size) * len(df))
        while df['document_id'][border1] == df['document_id'][border1 - 1]:
            border1 -= 1
        while df['document_id'][border2] == df['document_id'][border2 - 1]:
            border2 -= 1
        final_dataframes = np.split(df, [border1, border2])
        pass
    else:
        for group in groups.groups:
            group_df = groups.get_group(group)
            group_split = np.split(group_df.sample(frac=1, random_state=42),
                                     [int(train_size * len(group_df)), int((train_size + val_size) * len(group_df))])
            for i in range(number_of_groups):
                final_dataframes[i] = pd.concat([final_dataframes[i], group_split[i]])


    # oversampling
    if oversample:
        for i in range(number_of_groups):
            max_class_count = final_dataframes[i][label_name].value_counts().max()
            final_dataframes[i] = final_dataframes[i].groupby(label_name).apply(lambda x: x.sample(max_class_count, replace=True)).reset_index(
                drop=True)

    # shuffle rows
    for i in range(number_of_groups):
        final_dataframes[i] = final_dataframes[i].sample(frac=1, random_state=42).reset_index(drop=True)

    return final_dataframes