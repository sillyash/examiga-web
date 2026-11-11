---
title: "EX-AMIGA - Rapport de projet"
subtitle: "Bases du Web · ENSIIE FISA 2025-2026"
author: "Ashley Merienne"
---


Lorsque j'ai lu le sujet, j'ai décidé de faire d'une pierre deux coups et de créer un site pour mon groupe de musique EX-AMIGA, un groupe de midwest emo / post-emo.

Le site est une vitrine qui présente le groupe, les dates de tournée et un livre d'or pour le rendre fun. Il est déployé et disponible en ligne à l'adresse suivante : https://examigaband.com.

# 1. Technologies utilisées

## Architecture

J'ai fait le choix de séparer le front-end et le back-end, avec un client Vue 3 (JS/TS) qui communique avec un back-end Flask (Python) via une API REST.

## Choix des technologies

| Technologie         | Rôle                   | Pourquoi                                                  |
| ------------------- | ---------------------- | --------------------------------------------------------- |
| Vue 3 + TypeScript  | client                 | 2 ans d'expérience au travail, TypeScript pour progresser |
| Vite                | build / serveur de dev | Par défaut avec Vue, rapide                               |
| vue-i18n            | traduction FR/EN       | Plus pratique que de gérer les langues à la main          |
| Flask + APIFlask    | serveur API            | Léger, simple, plus sûr qu'un accès direct à la BDD       |
| SQLAlchemy + SQLite | base de données        | Léger, adapté aux contraintes du projet                   |
| Flask-Limiter       | anti-spam              | S'intègre à Flask pour protéger le livre d'or             |
| uv · just           | outillage              | Dépendances Python, commandes auto                        |

## Base de données

La base de données est une base SQLite. Elle contient seulement deux tables : `tour_dates` et `shoutouts`.

La table `tour_dates` contient les dates de tournée du groupe. Elle est en lecture seule.

La table `shoutouts` contient les messages laissés par les visiteur·rices dans le livre d'or. Elle est en lecture et en écriture, avec une limitation de débit pour éviter le spam.

L'accès à la base de données se fait via l'API Flask en Python.

L'API utilise l'ORM SQLAlchemy, ce qui permet de ne pas écrire de SQL à la main.

Le remplissage de la base de données se fait via un script Python `fill_db.py`.

## Justification du nombre de fichiers

Au total, le projet contient 45 fichiers non binaires (hors fichiers de configuration).

Le serveur API contient 9 fichiers, ce qui respecte la contrainte.

Le client web, quant à lui, contient 36 fichiers (dont 21 dans `src/`, le reste étant de la configuration).
Cela s'explique par le choix de technologie (Vue 3) qui impose une division du code et du contenu en composants,
chacun ayant son propre fichier source. Cela permet de rendre le code plus lisible et réutilisable.

# 2. Manuel d'utilisation

**Lancement** : toutes les étapes d'installation sont dans le `README.md`. Avec `just`, il suffit de lancer `just install` puis `just dev` à la racine du projet (serveur API Flask + serveur de dev Vite) ; les commandes `uv` et `npm` équivalentes y sont aussi données pour ne pas avoir à installer `just`. Le site est également en ligne sur https://examigaband.com, avec le même front-end (le back-end de production a été remplacé par Django, mais l'archive fonctionne seule en local).

**Sur chaque page**, l'en-tête contient le menu ainsi que deux boutons : FR/EN pour changer de langue et jour/nuit pour changer de thème. Le changement est instantané, sans rechargement, et le choix est mémorisé pour la prochaine visite. Le pied de page contient les crédits.

**Accueil** : une photo du groupe, la prochaine date de concert, une présentation des membres et les derniers messages du livre d'or.

**Concerts** : la liste des dates de tournée, lue depuis la base. Chaque carte affiche la description du concert et un menu « ajouter au calendrier » (lien Google Agenda ou fichier .ics pour Apple / Outlook).

**Livre d'or** : on peut lire les messages laissés par les visiteur·rices et en laisser un nouveau (nom + message). Cela rajoute un peu d'interactivité au site et permet de créer une communauté autour du groupe. C'est ici que se fait la requête d'écriture (INSERT) demandée par le sujet.

**Contact** : un formulaire qui ouvre la messagerie du visiteur avec le message déjà rempli, ainsi que les liens vers les réseaux sociaux du groupe.

# 3. Détails techniques

## Protection du livre d'or contre le spam

Le site étant vraiment en ligne, et mes domaines constamment attaqués par des robots, il fallait protéger le livre d'or. J'ai combiné un *honeypot* et une limitation de débit : le *honeypot* est un champ `website` caché, invisible pour les humains mais rempli par les robots ; s'il n'est pas vide, le serveur rejette la requête (erreur 422). Flask-Limiter bloque ensuite chaque IP au-delà de 3 messages par minute et 20 par jour (erreur 429).

> En production, avec Django, j'ai gardé la même logique en ajoutant une surcouche Cloudflare et des challenges CAPTCHA pour les utilisateurs suspects. Mon combat contre les bots est long et passionnant, mais je ne peux pas trop m'étaler dessus ici...

## Thème jour et nuit

J'ai hésité entre un *store* Pinia et un simple *composable*, `useTheme.ts`. Pour un seul état, un *store* aurait été overkill : le `ref` du thème, déclaré au niveau du module, est partagé par tous les composants. Il est initialisé depuis le `localStorage` ou la préférence système, et un `watch` met à jour l'attribut `data-theme` de `<html>` : les variables CSS de `main.css` changent alors instantanément, sans rechargement.

```{=typst}
#pagebreak()
```

# Captures d'écran

<!--
  Le sujet exige chaque page visitable × FR/EN × jour/nuit = 16 captures (hors limite des 2 pages).
  Prises sous Firefox à 1280px, en JPG compressé (~100 Ko) dans docs/screenshots/,
  nommées <page>-<langue>-<thème>.jpg. Les chemins sont relatifs à la racine du dépôt.
  Tant que les fichiers n'existent pas, `just pdf` échoue : décommente les grilles au fur et à mesure,
  ou commente la section entière.
-->

```{=typst}
#grid(columns: 1, gutter: 14pt,
  figure(image("docs/screenshots/home-fr-day.jpg"),   caption: [Accueil - FR - jour]),
  figure(image("docs/screenshots/home-fr-night.jpg"), caption: [Accueil - FR - nuit]),
  figure(image("docs/screenshots/home-en-day.jpg"),   caption: [Accueil - EN - jour]),
  figure(image("docs/screenshots/home-fr-day-2.jpg"),   caption: [Accueil (pt. 2) - FR - jour]),
  figure(image("docs/screenshots/home-fr-night-2.jpg"), caption: [Accueil (pt. 2) - FR - nuit]),
  figure(image("docs/screenshots/home-en-day-2.jpg"),   caption: [Accueil (pt. 2) - EN - jour])
)
```

```{=typst}
#grid(columns: 1, gutter: 14pt,
  figure(image("docs/screenshots/shows-fr-day.jpg"),   caption: [Concerts - FR - jour]),
  figure(image("docs/screenshots/shows-fr-night.jpg"), caption: [Concerts - FR - nuit]),
  figure(image("docs/screenshots/shows-en-day.jpg"),   caption: [Concerts - EN - jour])
)
```

```{=typst}
#grid(columns: 1, gutter: 14pt,
  figure(image("docs/screenshots/guestbook-fr-day.jpg"),   caption: [Livre d'or - FR - jour]),
  figure(image("docs/screenshots/guestbook-fr-night.jpg"), caption: [Livre d'or - FR - nuit]),
  figure(image("docs/screenshots/guestbook-en-day.jpg"),   caption: [Livre d'or - EN - jour])
)
```

```{=typst}
#grid(columns: 1, gutter: 14pt,
  figure(image("docs/screenshots/contact-fr-day.jpg"),   caption: [Contact - FR - jour]),
  figure(image("docs/screenshots/contact-fr-night.jpg"), caption: [Contact - FR - nuit]),
  figure(image("docs/screenshots/contact-en-day.jpg"),   caption: [Contact - EN - jour])
)
```
