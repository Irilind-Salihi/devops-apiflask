  ## Étape 1 : Ajouter les secrets à votre cluster Kubernetes ```bash kubectl apply -f flaskapi-secrets.yml`

## Étape 2 : Créer un Volume Persistant et une Demande de Volume Persistant pour la base de données

bash

`kubectl apply -f mysql-pv.yml`

## Étape 3 : Créer le Déploiement MySQL

bash

`kubectl apply -f mysql-deployment.yml`

## Étape 4 : Créer le Déploiement de Flask API

bash

`kubectl apply -f flaskapp-deployment.yml`

## Vérification de l'État

Vous pouvez vérifier l'état des pods, services et déploiements avec les commandes `kubectl get pods`, `kubectl get services` et `kubectl get deployments`.

# Création de la Base de Données et du Schéma

## Étape 1 : Se connecter à la Base de Données MySQL

bash

`kubectl run -it --rm --image=mysql --restart=Never mysql-client -- mysql --host mysql --password=<mot-de-passe-super-secret>`

Assurez-vous d'entrer le mot de passe (décodé) spécifié dans `flaskapi-secrets.yml`.

## Étape 2 : Créer la Base de Données et la Table

1. `CREATE DATABASE flaskapi;`
2. `USE flaskapi;`
3. `CREATE TABLE users(user_id INT PRIMARY KEY AUTO_INCREMENT, user_name VARCHAR(255), user_email VARCHAR(255), user_password VARCHAR(255));`

# Exposer l'API

Exposer l'API en utilisant minikube :

bash

`minikube service flask-service`

Cela renverra une URL. Collez cette URL dans votre navigateur pour voir le message "hello world". Utilisez cette `service_URL` pour effectuer des requêtes vers l'API.

# Commencer à effectuer des requêtes

Maintenant, vous pouvez utiliser l'API pour effectuer des opérations CRUD sur votre base de données.

1. Ajouter un utilisateur :

bash

`curl -H "Content-Type: application/json" -d '{"name": "<nom_utilisateur>", "email": "<email_utilisateur>", "pwd": "<mot_de_passe_utilisateur>"}' <service_URL>/create`

2. Obtenir tous les utilisateurs :

bash

`curl <service_URL>/users`

3. Obtenir les informations d'un utilisateur spécifique :

bash

`curl <service_URL>/user/<id_utilisateur>`

4. Supprimer un utilisateur par id_utilisateur :

bash

`curl -H "Content-Type: application/json" <service_URL>/delete/<id_utilisateur>`

5. Mettre à jour les informations d'un utilisateur :

bash

`curl -H "Content-Type: application/json" -d '{"name": "<nom_utilisateur>", "email": "<email_utilisateur>", "pwd": "<mot_de_passe_utilisateur>", "user_id": <id_utilisateur>}' <service_URL>/update`