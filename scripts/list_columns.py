import pandas as pd
df = pd.read_excel('data/raw/enquete_bob.xlsx')
print(f'Nombre de repondants: {len(df)}')
print('\nColonnes:')
for i, col in enumerate(df.columns[:10]):
    print(f'{i}: {col}')

