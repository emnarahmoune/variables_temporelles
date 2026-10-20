import pandas as pd


def profile_dataframe(df, name='jeu de données', max_cardinality=25):
    """Affiche un rapport d'exploration standard."""

    # 1. Nom, dimensions et mémoire
    print(f'=== {name} ===')
    print(f'Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes')
    print(f'Mémoire : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB')

    # 2. Nombre de lignes strictement dupliquées
    print()
    print(f'Lignes dupliquées : {df.duplicated().sum()}')

    # 3. Profil des colonnes
    print()
    print('--- Profil des colonnes ---')

    profile = pd.DataFrame({
        'type': df.dtypes.astype(str),
        'valeurs_manquantes': df.isna().sum(),
        'taux_manquants_%': (df.isna().mean() * 100).round(2),
        'valeurs_distinctes': df.nunique(dropna=True)
    })

    print(profile)

    # 4. Statistiques numériques
    print()
    print('--- Statistiques descriptives numériques ---')
    print(df.describe())

    # 5. Répartition des modalités
    print()
    print('--- Répartition des modalités ---')

    text_columns = df.select_dtypes(include='object').columns

    for col in text_columns:
        if df[col].nunique(dropna=True) < max_cardinality:
            print()
            print(f'{col} :')
            print(df[col].value_counts(dropna=False))