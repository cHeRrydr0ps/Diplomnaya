import asyncio

import pandas as pd
from joblib import load

from estimator.dataset import mine_attributes, clean_name


async def main():
    comp_name = input('Введите название компании: ')

    attributes = await mine_attributes(comp_name, train=False)
    print(f'Имя компании: {clean_name(attributes["short_name"])}')
    attributes.pop('short_name')
    df = pd.DataFrame([attributes])

    model = load('data/models/model.joblib')
    predictor = model['model']
    print('Оценка: {:2.2f}'.format(predictor.predict(df)[0]))
    formatter(attributes)


def formatter(data):
    def recur(key, values, depth=0):
        offset = '\t' * depth
        if isinstance(values, str):
            value = data.get(values)
            value = value if value is not None else '?'
            print(f'{offset}{key}:\t{value}')
        else:
            print(f'{offset}{key}')
            for sub_key, value in values.items():
                recur(sub_key, value, depth + 1)
    pattern = {
        'Расчёты': {
            'Валовая рентабельность': 'val_rent',
            'Рентабельность активов': 'roa',
            'Коэффициент текущей ликвидности': 'cr',
        },
        'Медиа': {
            'Количество запросов за прошедние 5 недель': 'ggl_trend5',
            'Количество запросов за прошедние 10 недель': 'ggl_trend10',
        },
        'Бухгалтерский баланс': {
            'Нематериальные активы': 'intangible_assets',
            'Основные средства': 'fixes_assets',
            'Внеоборотные активы': 'non_current_assets',
            'Баланс оборотных активов': 'balance',
            'Резервы': 'reserves',
            'Итог капитал и резервы': 'capital_and_reserves_total',
            'Добавочный капитал': 'additional_capital',
            'Долгосрочные обязательства': 'long_term_liabilities',
            'Краткосрочные обязательства': 'short_term_liabilities',
        },
        'Отчет о финансовых результатах': {
            'Выручка': 'revenue',
            'Себестоимость продаж': 'cost_price',
            'Валовая прибыль (убыток)': 'gross_profit',
            'Чистая прибыль (убыток)': 'clear_profit',
        },
        'Отчет о движении денежных средств': {
            'Денежные потоки от текущих операций': {
                'Поступления': 'income',
                'Поступления от продажи': 'income_sell',
                'От продажи': 'income_sell',
                'Платежи': 'payments',
                'Сальдо': 'balance_stream',
            },
            'Денежные потоки от инвестиционных операций': {
                'Поступления': 'income_invest',
                'Платежи': 'payments_invest',
                'Сальдо': 'balance_invest',
            },
            'Денежные потоки от финансовых операций': {
                'Поступления': 'income_fin',
                'Платежи': 'payments_fin',
                'Сальдо': 'balance_fin',
            },
        }
    }
    for k, v in pattern.items():
        recur(k, v)


if __name__ == '__main__':
    asyncio.run(main())
