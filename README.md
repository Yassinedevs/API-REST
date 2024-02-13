# Le Richardson Maturity Model

Le Richardson Maturity Model, également connu sous le nom de "REST Maturity Model" ou "Richardson RESTful Maturity Model", a été proposé par Leonard Richardson en 2008. Il vise à évaluer le niveau de maturité des services web RESTful en fonction de certaines caractéristiques clés. Le modèle est composé de quatre niveaux, chacun représentant une étape vers une conception RESTful plus avancée et évolutive.

Voici une explication détaillée de chaque niveau du Richardson Maturity Model :

## Niveau 0: Le Point d'Origine (The Swamp of POX)
Au niveau 0, les services web sont conçus comme des points d'origine (POX - Plain Old XML) sans l'utilisation des principes REST. Ces services utilisent souvent des protocoles non-RESTful tels que SOAP (Simple Object Access Protocol) et exposent des opérations spécifiques en tant que méthodes RPC (Remote Procedure Call).

### Caractéristiques du Niveau 0 :

* Utilisation de protocoles non-RESTful (comme SOAP).
* Absence d'utilisation des méthodes HTTP (GET, POST, PUT, DELETE).
* L'interaction se fait généralement via des opérations spécifiques plutôt que des ressources.

## Niveau 1: Ressources Individuelles (Resources)
Au niveau 1, l'architecture commence à adopter les principes REST. Les services commencent à exposer des ressources individuelles via des URI (Uniform Resource Identifiers), mais l'interaction avec ces ressources est toujours effectuée via des opérations non-RESTful (par exemple, en utilisant uniquement POST pour toutes les actions).

### Caractéristiques du Niveau 1 :

* Utilisation d'URIs pour identifier les ressources.
* Les ressources individuelles sont exposées.

## Niveau 2: Utilisation des Verbes HTTP (HTTP Verbs)
Au niveau 2, les services web commencent à utiliser correctement les méthodes HTTP (GET, POST, PUT, DELETE) pour interagir avec les ressources. Chaque ressource est associée à une URI unique et les méthodes HTTP sont utilisées de manière appropriée pour effectuer des opérations sur ces ressources.

### Caractéristiques du Niveau 2 :

* Utilisation appropriée des méthodes HTTP pour interagir avec les ressources.
* Les URI identifient de manière unique chaque ressource.

## Niveau 3: Hypermedia comme Moteur de l'Application (HATEOAS)
Au niveau 3, le principe de HATEOAS est introduit, ce qui signifie que l'API fournit des liens hypertexte avec les réponses, permettant ainsi aux clients de naviguer et d'interagir dynamiquement avec l'API sans nécessiter une connaissance préalable de l'ensemble de l'API.

### Caractéristiques du Niveau 3 :

* Utilisation de HATEOAS pour fournir des liens hypertexte dans les réponses.
* Les clients peuvent naviguer dynamiquement à travers l'API en suivant les liens.

Atteindre le niveau 3 indique un haut niveau de maturité en termes de conception RESTful, car cela implique non seulement l'utilisation correcte des méthodes HTTP mais aussi l'exploitation de la dynamique des liens pour guider les clients à travers l'API.

Le Richardson Maturity Model offre une progression graduelle pour aider à évaluer et améliorer la conception des services web RESTful, en mettant l'accent sur les principes fondamentaux de REST tels que l'utilisation d'URIs, de méthodes HTTP et de HATEOAS.


# Comment l'avons nous respecté ?

Dans notre code Flask, nous avons respecté plusieurs principes du modèle de Richardson pour les API REST, bien que certains aspects pourraient être améliorés pour atteindre un niveau de maturité plus élevé. Voici une analyse point par point :

## Niveau 1:
Ressources individuelles identifiées par des URIs : Nous utilisons des URIs pour identifier les ressources, par exemple dans la route "/int:id" pour obtenir un film spécifique.

## Niveau 2:
Utilisation des verbes HTTP : Nous utilisons les méthodes HTTP appropriées pour interagir avec les ressources (GET, POST, DELETE). Par exemple, nous utilisons GET pour obtenir un film, DELETE pour supprimer un film, et POST pour créer ou mettre à jour un film.

## Niveau 3:
Hypermedia comme moteur de l'application (HATEOAS) : Nous fournissons des liens hypertexte dans les réponses qui permettent aux clients de naviguer dynamiquement à travers l'API. Par exemple dans la méthode GET pour obtnir un film, nous listns des liens des peoples qui pointent vers une people spécifique

## Autres observations :
1. Utilisation de JSON pour les réponses : Nous renvoyons les données sous forme JSON, ce qui est une bonne pratique pour les API RESTful.
1. Gestion des erreurs : Nous gérons les erreurs de manière appropriée en renvoyant des réponses JSON avec un statut d'erreur et un message d'erreur approprié lorsqu'une exception se produit.
1. Validation des entrées : Nous devrions envisager d'ajouter une validation des entrées pour les requêtes POST et PUT afin de garantir que les données fournies sont correctes.

En résumé, notre API respecte les niveaux 1, 2 et 3 du modèle de Richardson.