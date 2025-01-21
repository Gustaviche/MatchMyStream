import streamlit as st
import pandas as pd

def load_data(url, index_col=None):
    """
    Charge un fichier CSV à partir d'une URL ou d'un chemin local.

    Args:
        url (str): L'URL ou le chemin local du fichier CSV.
        index_col (int or str, optional): Colonne à utiliser comme index. Par défaut, None.

    Returns:
        pd.DataFrame: Le dataframe chargé.
    """

    df = pd.read_csv(url, index_col=index_col)
    return df
    
