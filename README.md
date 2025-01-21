## MatchMyStream

MatchMyStream est une application interactive permettant aux utilisateurs de découvrir et de gérer leurs films et séries préférés. Grâce à l'intégration de l'API TMDB, et des datasets du site IMDB, l'application permet de récupérer des informations sur les films et les séries, d'afficher des recommandations personnalisées et de gérer une liste de contenus déjà vus. Les utilisateurs peuvent également consulter des informations détaillées, telles que les genres, acteurs, réalisateurs, et bien plus encore.

# Fonctionnalités principales
* Recherche de films et séries : Trouvez vos films et séries préférés via une interface intuitive.
* Affichage des détails : Consultez les informations détaillées telles que les genres, réalisateurs, acteurs, synopsis, et affiches.
* Liste personnalisée : Ajoutez des films et des séries à votre liste des contenus vus et gérez-les facilement.
* Recommandations intelligentes : Découvrez des films et séries similaires à ceux que vous avez déjà appréciés.

# Structure du projet

Voici une vue d'ensemble des fichiers et dossiers principaux de ce projet :

MatchMyStream/
│
├── app.py                  # Fichier principal qui lance l'application Streamlit
├── config.toml             # Fichier de configuration pour l'application
├── data.py                 # Script Python pour gérer les données (par exemple : import, nettoyage)
├── df_films.csv            # Fichier CSV contenant les informations sur les films
├── df_series.csv           # Fichier CSV contenant les informations sur les séries
├── film_utils.py           # Fichier Python avec des fonctions utilitaires pour les films
├── poster_film.jpg         # Image d'affiche de film
├── poster_series.jpg       # Image d'affiche de série
├── series_utils.py         # Fichier Python avec des fonctions utilitaires pour les séries
├── LICENSE                 # Fichier de licence du projet
└── README.md               # Documentation du projet


# Technologies utilisées
* Streamlit : Framework pour la création rapide d'applications interactives.
* Pandas : Librairie pour la manipulation des données.
* Requests : Utilisée pour interagir avec l'API TMDB.
* TMDB API : Source de données pour les films et séries.
* Python 3.x : Langage de programmation utilisé pour le développement.

Ce projet est sous licence MIT.


