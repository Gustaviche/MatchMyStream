import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import film_utils
import series_utils
import data


df_movies = data.load_data("/Users/algaumon/Documents/MatchMyStream/df_films.csv", index_col=None)
df_series = data.load_data("/Users/algaumon/Documents/MatchMyStream/df_series.csv")

def background():
    st.markdown("""
    <style>
    /* Fond global pour l'application */
    .stApp {
        background-image: url('https://github.com/Gustaviche/MatchMyMovie/blob/main/poster_film.jpg?raw=true');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Ciblage des widgets (conteneur principal) */
    div.block-container {
        background: rgba(0, 0, 0, 0.85); /* Transparence blanche */
        border-radius: 15px; /* Coins arrondis */
        padding: 20px; /* Espacement interne */
                }
                
    div.data-v-5af006b8{
                 border-radius: 15px;
                }
     }
    </style>
    """, unsafe_allow_html=True)

def center_content():
    st.markdown("""
    <style>
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="MatchMyStream",
    page_icon="🍿",
    layout="centered",
    initial_sidebar_state="expanded"
)

if 'viewed_movies' not in st.session_state:
    st.session_state['viewed_movies'] = []

if 'viewed_series' not in st.session_state:
    st.session_state['viewed_series'] = []

background()

center_content()

# Ajout d'onglets pour basculer entre les films et les séries
tab1, tab2 = st.tabs(["🎥 Films", "📺 Séries"])

# Menu de navigation
with st.sidebar:
    selection = option_menu(
        menu_title="Menu",  # Titre du menu dans la sidebar
        options=["Accueil", "Recommendation par genre","Top 10","Ma liste","Déconnexion"],
        icons=["house-door", "film","bar-chart","clipboard2-check","power"],
        default_index=0,
        orientation="vertical",  # Menu vertical
        styles={
            "background-color" : "#000000",
            "container": {"padding": "5px"},
            "icon": {"font-size": "20px", "color": "#ffffff"},
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "10px", 
                "--hover-color": "#ff4242"
            },
            "nav-link-selected": {"background-color": "#7b0000"}
        }
    )
with tab1:
        
    if selection == "Accueil":
        st.title("Bienvenue sur MatchMyStream !")
        st.subheader("L'IA au service de vos soirées chill !")
        st.title("Recommandations")
        # Demander à l'utilisateur d'entrer des mots-clés pour la recherche
        query = st.text_input("Entrez un ou plusieurs mots-clés",key='queury film')  # Ajout d'une clé unique
        if query:
            # Appeler la fonction de recommandation avec les mots-clés et les données des films
            results = film_utils.recommend_movies_keyword(df_movies, query, n_neighbors=10, threshold_distance=0.9, stopwords=None)
            # Appeler la fonction d'affichage de films
            if results:
                film_utils.afficher_films(results)
            else:
                st.write("Aucun film trouvé, veuillez écrire d'autres mots-clés.")

    elif selection == "Recommendation par genre":
        st.title("Recommandation de films par genre")
        
        # Sélection du premier genre
        genre_1 = st.selectbox("Sélectionner un genre", ["", "Action", 'Adventure', 'Animation', "Comedy", "Crime", "Drama", 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'Thriller', 'War', 'Western'])
        
        # Sélection du deuxième genre (optionnel)
        genre_2 = st.selectbox("Sélectionner un deuxième genre (optionnel)", ["", "Action", 'Adventure', 'Animation', "Comedy", "Crime", "Drama", 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'Thriller', 'War', 'Western'])
        
        # Création de la liste des genres sélectionnés
        user_genres = [genre_1]
        if genre_2:
            user_genres.append(genre_2)

        # Vérification si au moins un genre a été sélectionné
        if user_genres and "" not in user_genres:
            # Appeler la fonction de recommandation avec les genres sélectionnés
            results = film_utils.recommend_movies_genres(df_movies, user_genres)
            film_utils.afficher_films(results)

        else:
            st.write("Veuillez sélectionner au moins un genre pour voir les recommandations.")

    elif selection == "Top 10":
        st.title("Top 10 des meilleurs films")
        st.subheader("Choisissez un genre pour découvrir les meilleurs films du genre")

        # Liste des genres
        genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "Thriller", "War", "Western"]

        # Sélection du genre avec st.selectbox (ou st.radio si vous préférez)
        genre = st.pills("Choisissez un genre", options=genres)
        if genre:
        # Appeler la fonction pour filtrer et obtenir les films
            results = film_utils.top_10(df_movies, genre)
            # Vérifier si des films sont trouvés et les afficher
            film_utils.afficher_films(results)
        else:
            st.write("Veuillez sélectionner un genre pour voir les recommandations.")

    elif selection == "Ma liste":
        # Affichage des films vus
        st.title("Films déjà vus")
        
        # Si la liste des films vus contient des films
        film_utils.afficher_ma_liste(df_movies)

    elif selection == "Déconnexion":
        st.write("Vous êtes déconnecté.")

with tab2:
    if selection == "Accueil":
        st.title("Bienvenue sur MatchMyStream !")
        st.subheader("L'IA au service de vos soirées chill !")
        st.title("Recommandations")
        # Demander à l'utilisateur d'entrer des mots-clés pour la recherche
        query = st.text_input("Entrez un ou plusieurs mots-clés", key='queury series')  # Ajout d'une clé unique
        if query:
            # Appeler la fonction de recommandation avec les mots-clés et les données des films
            results = series_utils.recommend_series_keyword(df_series, query, n_neighbors=10, threshold_distance=0.9, stopwords=None)
            # Appeler la fonction d'affichage de films
            if results:
                series_utils.afficher_series(results)
            else:
                st.write("Aucun film trouvé, veuillez écrire d'autres mots-clés.")

    elif selection == "Recommendation par genre":
        st.title("Recommandation de films par genre")
        
        # Sélection du premier genre
        genre_1 = st.selectbox("Sélectionner un genre", ['', 'Action & Adventure', 'Animation', 'Comédie', 'Crime', 'Documentaire', 'Drame', 'Familial', 'Kids', 'Mystère', 'Reality', 'Science-Fiction & Fantastique', 'Soap', 'Talk', 'War & Politics', 'Western'],key='series')
        
        # Sélection du deuxième genre (optionnel)
        genre_2 = st.selectbox("Sélectionner un deuxième genre (optionnel)", ['', 'Action & Adventure', 'Animation', 'Comédie', 'Crime', 'Documentaire', 'Drame', 'Familial', 'Kids', 'Mystère', 'Reality', 'Science-Fiction & Fantastique', 'Soap', 'Talk', 'War & Politics', 'Western'],key='series2')
        
        # Création de la liste des genres sélectionnés
        user_genres = [genre_1]
        if genre_2:
            user_genres.append(genre_2)

        # Vérification si au moins un genre a été sélectionné
        if user_genres and "" not in user_genres:
            # Appeler la fonction de recommandation avec les genres sélectionnés
            results = series_utils.recommend_series_genres(df_series, user_genres)
            series_utils.afficher_series(results)

        else:
            st.write("Veuillez sélectionner au moins un genre pour voir les recommandations.")

    elif selection == "Top 10":
        st.title("Top 10 par genre")
        st.subheader("Choisissez un genre pour découvrir les meilleurs films du genre")

        # Liste des genres
        genres = ['Action & Adventure', 'Animation', 'Comédie', 'Crime', 'Documentaire', 'Drame', 'Familial', 'Kids', 'Mystère', 'Reality', 'Science-Fiction & Fantastique', 'Soap', 'Talk', 'War & Politics', 'Western']

        # Sélection du genre avec st.selectbox (ou st.radio si vous préférez)
        genre = st.pills("Choisissez un genre", options=genres,key='series')
        if genre:
        # Appeler la fonction pour filtrer et obtenir les films
            results = series_utils.top_10(df_series, genre)
            # Vérifier si des films sont trouvés et les afficher
            series_utils.afficher_series(results)
        else:
            st.write("Veuillez sélectionner un genre pour voir les recommandations.")

    elif selection == "Ma liste":
        # Affichage des films vus
        st.title("Séries dans votre liste")
        
        # Si la liste des films vus contient des films
        series_utils.afficher_ma_liste(df_series)