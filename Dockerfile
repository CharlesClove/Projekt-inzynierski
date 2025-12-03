# 1. Obraz bazowy (Python 3.12.1 - slim dla mniejszego rozmiaru)
FROM python:3.12.1-slim

# 2. Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# 3. Kopiowanie pliku zależności (najpierw, aby wykorzystać cache Dockera)
COPY requirements.txt .

# 4. Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopiowanie reszty plików aplikacji
COPY . .

# 6. Otwarcie portu 5000 (informacyjnie)
EXPOSE 5000

# 7. Komenda uruchamiająca serwer
CMD ["python3", "app/app.py"]