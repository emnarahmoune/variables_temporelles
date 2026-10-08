import numpy as np
import pandas as pd


def clean_sales(df, drop_negative_quantities=True, max_quantity=None, verbose=True):

    log = {'lignes_initiales': len(df)}

    # 1. Copier le DataFrame
    df = df.copy()

    # 2. Convertir prix_unitaire en numérique
    df['prix_unitaire'] = pd.to_numeric(
        df['prix_unitaire'],
        errors='coerce'
    )

    # 3. Normaliser les colonnes texte descriptives
    text_columns = [
        col for col in df.select_dtypes(include='object').columns
        if not col.startswith('id_')
    ]

    for col in text_columns:
        df[col] = (
            df[col]
            .astype('string')
            .str.strip()
            .str.lower()
        )

    log['colonnes_texte_normalisees'] = len(text_columns)

    # 4. Supprimer les doublons stricts
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    log['doublons_supprimes'] = int(duplicates)

    # 5. Convertir date_commande et supprimer les dates manquantes
    df['date_commande'] = pd.to_datetime(
    df['date_commande'],
    errors='coerce',
    format='mixed',
    dayfirst=True
)

    missing_dates = df['date_commande'].isna().sum()
    df = df.dropna(subset=['date_commande'])

    log['dates_manquantes_supprimees'] = int(missing_dates)

    # 6. Remplacer les remises manquantes par 0
    missing_discount = df['remise_pct'].isna().sum()

    df['remise_pct'] = df['remise_pct'].fillna(0)

    log['remises_manquantes_remplacees'] = int(missing_discount)

    # 7. Traiter les quantités négatives
    negative_mask = df['quantite'] < 0
    negative_count = negative_mask.sum()

    if drop_negative_quantities:
        df = df.loc[~negative_mask].copy()
    else:
        df.loc[negative_mask, 'quantite'] = np.nan

    log['quantites_negatives_traitees'] = int(negative_count)

    # 8. Limite facultative des grandes quantités
    if max_quantity is not None:
        high_quantity_mask = df['quantite'] > max_quantity
        high_quantity_count = high_quantity_mask.sum()

        df = df.loc[~high_quantity_mask].copy()

        log['quantites_superieures_limite_supprimees'] = int(
            high_quantity_count
        )

    # 9. Calculer le montant
    df['montant'] = (
        df['quantite']
        * df['prix_unitaire']
        * (1 - df['remise_pct'] / 100)
    )

    # Nombre final de lignes
    log['lignes_finales'] = len(df)

    if verbose:
        for key, value in log.items():
            print(f'  {key:<40} {value}')

    return df, log