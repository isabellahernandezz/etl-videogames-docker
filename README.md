cat > README.md << 'EOF'
# 🎮 ETL Docker Project: Video Game Genres 2024

Pipeline ETL para analizar ventas globales por género de videojuegos.  
Procesa un archivo CSV (`genres_v2.csv`), limpia los datos, calcula estadísticas por género y genera un ranking de los 10 más populares.

---

## 🚀 Ejecución Rápida

### 1️⃣ Construir la Imagen
docker build -t etl-genres:latest .

### 2️⃣ Ejecutar el Contenedor
docker run --rm -v ${PWD}/output:/app/output etl-genres:latest

### 3️⃣ Ver los Resultados
Los archivos estarán en:
- ./output/genre_stats.csv
- ./output/top10_genres.csv

---

## ⚙️ Ejecución Manual (Debug)
docker run --rm -it -v ${PWD}/output:/app/output etl-genres:latest bash

Una vez dentro:
python ETL.py --input genres_v2.csv --out-dir output

---

## 🧹 Limpiar Docker
docker system prune -a --volumes

---

## 📊 Métricas Calculadas
- Ventas totales globales por género
- Ventas por región (NA, EU, JP)
- Ranking ponderado (`Rank_Score`)

---

## 📄 Licencia
Proyecto educativo para prácticas de ETL con Docker y Python.
EOF
