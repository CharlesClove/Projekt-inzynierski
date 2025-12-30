# Projekt Inżynierski - Simple Shop DevOps

**Autor:** Karol Goździewski  
**Nr albumu:** 42368  
**Temat:** Implementacja rozwiązań DevOps na przykładzie aplikacji webowej.

## O projekcie
Prosta aplikacja webowa typu "sklep internetowy" stworzona w celu demonstracji nowoczesnych procesów wytwarzania oprogramowania (CI/CD) oraz konteneryzacji. Projekt obejmuje widok klienta, panel administratora oraz REST API.

## Stos technologiczny
*   **Backend:** Python 3.12.1 + Flask 3.1.2
*   **Baza danych:** SQLite
*   **Frontend:** HTML, CSS, JavaScript
*   **Konteneryzacja:** Docker
*   **CI/CD:** GitHub Actions

## Struktura projektu
*   `/templates` - pliki HTML (widoki)
*   `app.py` - główna logika aplikacji i API
*   `Dockerfile` - konfiguracja obrazu kontenera
*   `.github/workflows` - definicja potoku CI/CD

## Jak uruchomić aplikację?

### 1. Lokalnie (Python)
Zainstaluj zależności i uruchom serwer:
```bash
pip install -r requirements.txt
python app.py# Projekt-inzynierski
```
### Aplikacja dostępna pod adresem: http://localhost:5000

## 2. Używając Dockera

Zbuduj obraz i uruchom kontener:

```Bash
docker build -t simple-shop .
docker run -p 5000:5000 simple-shop
```

Sciągnij obraz z dockerhub i uruchom kontener:
```Bash
docker pull clovedockerhub/projekt-inzynierski:latest
    #opcjonalne otagowanie kontenera
    docker tag clovedockerhub/projekt-inzynierski:latest simple-shop-ver#
docker run -d -p 5000:5000 clovedockerhub/projekt-inzynierski:latest {simple-shop-ver#}
```

## Endpointy

    / - Strona główna sklepu (widok klienta)
    /admin - Panel administratora (dodawanie/usuwanie produktów)
    /items - API (GET, POST, DELETE)

