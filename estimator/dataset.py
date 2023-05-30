import asyncio
import re

from loaders.bfo_loader import BFOLoader
from loaders.ggl_loader import GoogleTrendLoader
from loaders.stat_loader import StatLoader
import pandas as pd
from tqdm import tqdm


MODALITY_LOADERS = (
    BFOLoader,
    GoogleTrendLoader,
    StatLoader,
)


async def mine_attributes(company_name: str, train=True):
    res = dict()
    for loader_cls in MODALITY_LOADERS:
        loader = loader_cls()
        loader_resp = await loader.get(name=company_name, train=train, **res)
        res |= loader_resp

    return res


async def make_df():
    with open('../data/names.txt', 'r') as f:
        names = list(map(str.strip, f.readlines()))
    results = []
    for name in tqdm(names):
        res = await mine_attributes(name)
        res |= {'name': name}
        results.append(res)
    df = pd.DataFrame(results)
    df.to_csv('../data/dataset.csv')


def clean_name(name: str):
    pattern = re.compile(r'<[^>]+>')
    return re.sub(pattern, '', name)


async def make_df_with_mark():
    df = pd.read_csv('../data/dataset.csv', index_col=0)
    marks = {}
    with open('../data/marks.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(':')
            marks[line[0]] = float(line[1])
    df.insert(0, 'mark', -1)
    for i, row in df.iterrows():
        df.at[i, 'mark'] = marks[row['name']]
    df.to_csv('../data/dataset_with_target.csv')


if __name__ == '__main__':
    # asyncio.run(make_df())
    # Тут бага. В конец файла dataset.csv надо добавить две двойные кавычки - ""
    asyncio.run(make_df_with_mark())
