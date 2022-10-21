import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def elasticity_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    функция принимает на вход датасет и возвращает эластичность для каждого SKU
    :param df:
    sku - уникальный идентификатор товара.
    dates - уникальный день.
    price - средняя цена для товара-дня.
    qty - суммарное кол-во покупок.
    :return: pd.DataFrame
    sku - уникальный идентификатор товара.
    elasticity -  коэффициент детерминации линейной регрессии R2 как оценка эластичности для данного товара
    """

    dfs = df.copy()
    dfs["qty"] = dfs["qty"].apply(lambda x: np.log(x + 1))
    results_values = {
        "sku": [],
        "elasticity": [],
    }
    # Append x_values with y_values per same product name
    for i in dfs.sku.unique():
        dda = dfs.query(f'sku == {i}')
        column = i

        x_pivot = dda.pivot(index='dates', columns='sku', values='price')
        y_pivot = dda.pivot(index='dates', columns='sku', values='qty')
        lr = LinearRegression()
        lr.fit(x_pivot, y_pivot)
        y_pred = lr.predict(x_pivot)
        elasticity = r2_score(y_pivot, y_pred)

        # Append results into dictionary for dataframe
        results_values["sku"].append(column)
        results_values["elasticity"].append(elasticity)

    final_df = pd.DataFrame.from_dict(results_values)
    df_elasticity = final_df[['sku', 'elasticity']]

    return df_elasticity
