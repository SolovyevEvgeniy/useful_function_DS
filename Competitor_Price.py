import pandas as pd

dict_agg = {'avg': 'mean',
            'med': 'median',
            'min': 'min',
            'max': 'max'
            }

def agg_comp_price(X: pd.DataFrame) -> pd.DataFrame:
    '''
    make agg for new price 
    :param X:
     sku - id товара
     agg -тип агрегации:
            'avg' – берем среднее
            'med' – медиану
            'min' – минимальную цену
            'max' – максимальную
            'rnk' – цену конкурента, имеющего наибольший приоритет (наименьший ранг)
     rank -приоритет конкурентов
     base_price - текущая цена
     comp_price - цена конкурентов
    :return: pd.DataFrame
    '''
    df = X.copy()
    df_fin = pd.DataFrame()

    for i in df.sku.unique():
        df_temp = df.query(f"sku == {i}")
        if df_temp.iloc[0]['agg'] != "rnk":
            ag = dict_agg[df_temp.iloc[0]['agg']]
            df2 = df_temp.loc[:]
            df2['new'] = df2.groupby('sku', as_index = False).agg({'comp_price': ag}).iloc[0]['comp_price']
            df2 = df2.iloc[:1]
            df_fin = pd.concat([df2,df_fin])

        elif df_temp.iloc[0]['agg'] == "rnk":
            df2 = df_temp.loc[:]
            df2 = df2.sort_values('rank').iloc[:1]
            df2['new'] = df2['comp_price']
            df_fin = pd.concat([df2,df_fin])

    df_fin = df_fin.sort_values('sku')
    df_fin = df_fin.drop(columns="comp_price").rename(columns={'new': 'comp_price'})
    df_fin = df_fin[['sku','agg', 'base_price','comp_price']]

    df_fin['new_price'] = df_fin['base_price'].where(df_fin['comp_price'] != df_fin['comp_price'])
    df_fin['procent'] = abs((df_fin['base_price'] - df_fin['comp_price'])/ df_fin['base_price']*100)
    df_fin.loc[(df_fin.procent <= 20), 'new_price'] = df_fin['comp_price']
    df_fin.loc[(df_fin.procent >= 20), 'new_price'] = df_fin['base_price']
    df_fin = df_fin[['sku','agg', 'base_price','comp_price', 'new_price']]

    return df_fin
