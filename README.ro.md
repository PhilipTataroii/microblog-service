# MicroBlog Service

🇬🇧 [English](README.md) | 🇷🇴 **Română**

### Prezentare generală

MicroBlog este o aplicație de microblogging bazată pe o arhitectură RESTful API, dezvoltată ca proiect final în cadrul programului de formare profesională Python Advanced.

Aplicația permite utilizatorilor să creeze și să șteargă postări, să încarce imagini, să aprecieze postările altor utilizatori, să urmărească alți utilizatori și să exploreze un flux personalizat de postări.

Proiectul demonstrează competențe practice în dezvoltarea backend, proiectarea API-urilor REST, gestionarea bazelor de date, containerizarea aplicațiilor și testarea automată.

## Funcționalități

- Crearea și ștergerea postărilor
- Încărcarea imaginilor și atașarea acestora la postări
- Adăugarea și eliminarea aprecierilor
- Urmărirea și anularea urmăririi utilizatorilor
- Vizualizarea profilurilor utilizatorilor
- Vizualizarea fluxului de postări
- Sortarea postărilor în funcție de popularitate
- Autentificarea utilizatorilor prin antetul HTTP `api-key`
- Explorarea documentației interactive API prin Swagger
- Rularea și implementarea aplicației utilizând Docker Compose

## Tehnologii utilizate

- **Backend:** Python, Flask
- **Bază de date:** PostgreSQL, SQLAlchemy
- **Migrarea bazei de date:** Flask-Migrate, Alembic
- **Documentație API:** Flasgger, Swagger
- **Testare:** Pytest
- **Calitatea codului:** Flake8
- **Containerizare:** Docker, Docker Compose

## Instalare și pornire

### Cerințe preliminare

Asigurați-vă că Docker și Docker Compose sunt instalate pe sistem.

### Instalare și implementare

Clonați repository-ul:

```bash
git clone https://github.com/PhilipTataroii/microblog-service.git
cd microblog-service
```

Construiți și porniți aplicația:

```bash
docker compose up -d --build
```

Verificați starea containerelor:

```bash
docker compose ps
```

După pornirea aplicației, aceasta va fi disponibilă la adresa:

`http://127.0.0.1:5000/`

Pentru oprirea aplicației:

```bash
docker compose down
```

## Baza de date

MicroBlog utilizează PostgreSQL ca sistem de gestionare a bazei de date relaționale.

La rularea aplicației prin Docker Compose, PostgreSQL funcționează într-un container separat.

Migrațiile bazei de date sunt aplicate automat înainte de pornirea aplicației Flask, utilizând comanda:

```bash
flask db upgrade
```

## Autentificare

Aplicația identifică utilizatorii prin intermediul antetului HTTP `api-key`.

Exemplu:

```http
api-key: test
```

Utilizatorul asociat acestei chei trebuie să existe în baza de date.

## Endpoint-uri REST API

| Metodă | Endpoint | Descriere |
|---|---|---|
| GET | `/api/users/me` | Obținerea informațiilor despre utilizatorul curent |
| GET | `/api/users/<user_id>` | Obținerea unui utilizator după ID |
| GET | `/api/tweets` | Obținerea fluxului de postări |
| POST | `/api/tweets` | Crearea unei postări |
| DELETE | `/api/tweets/<tweet_id>` | Ștergerea unei postări |
| POST | `/api/medias` | Încărcarea unei imagini |
| POST | `/api/tweets/<tweet_id>/likes` | Aprecierea unei postări |
| DELETE | `/api/tweets/<tweet_id>/likes` | Eliminarea unei aprecieri |
| POST | `/api/users/<user_id>/follow` | Urmărirea unui utilizator |
| DELETE | `/api/users/<user_id>/follow` | Anularea urmăririi unui utilizator |

## Documentație Swagger API

Documentația interactivă a API-ului este disponibilă la adresa:

`http://127.0.0.1:5000/apidocs/`

Swagger permite consultarea endpoint-urilor disponibile, a parametrilor cererilor HTTP și a operațiilor API.

## Testare

Pentru executarea tuturor testelor automate:

```bash
pytest -v
```

Rezultatele testării la finalizarea proiectului:

**12 teste trecute cu succes.**

## Verificarea calității codului

Pentru verificarea calității codului cu Flake8:

```bash
flake8 app tests run.py config.py
```

Dacă verificarea se încheie cu succes, comanda nu va raporta erori.

## Structura proiectului

```text
microblog-service/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── dist/
├── migrations/
├── tests/
├── uploads/
├── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
├── swagger.yml
├── README.md
└── README.ro.md
```

## Autor

**Filip Tataroi**

Dezvoltator Python Backend

GitHub: https://github.com/PhilipTataroii

LinkedIn: https://www.linkedin.com/in/filip-tataroi/

**Tipul proiectului:** Python Advanced — Proiect final de formare profesională
