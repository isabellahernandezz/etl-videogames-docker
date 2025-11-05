import pandas as pd
import os

def main():
    print("🎧 Iniciando proceso ETL para datos de Spotify (genres_v2.csv)...")

    input_file = "genres_v2.csv"
    output_dir = "output"

    # Crear carpeta de salida dentro del contenedor
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Carpeta de salida: {os.path.abspath(output_dir)}")

    # Comprobar si el archivo existe
    if not os.path.exists(input_file):
        print(f"❌ ERROR: No se encontró el archivo {input_file}. Verifica que esté dentro del contenedor /app.")
        return

    # Cargar CSV
    print("📂 Cargando datos...")
    df = pd.read_csv(input_file)

    # Mostrar columnas disponibles
    print("📋 Columnas del dataset:", list(df.columns))

    # LIMPIEZA DE DATOS
    print("🧹 Limpiando datos...")
    df = df.dropna(subset=["genre"]) if "genre" in df.columns else df.dropna(subset=["genres"])
    genre_col = "genre" if "genre" in df.columns else "genres"
    df[genre_col] = df[genre_col].astype(str).str.strip().str.title()

    # Normalizar columnas numéricas comunes (si existen)
    numeric_cols = [c for c in ["energy", "danceability", "loudness", "tempo", "valence"] if c in df.columns]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Guardar datos limpios
    cleaned_path = os.path.join(output_dir, "cleaned_genres.csv")
    df.to_csv(cleaned_path, index=False)
    print(f"✅ Datos limpios guardados en: {cleaned_path}")

    # TRANSFORMACIÓN: estadísticas por género
    print("📊 Calculando estadísticas por género...")
    group = df.groupby(genre_col).agg({
        col: ["mean", "max", "min"] for col in numeric_cols
    })
    group.columns = ['_'.join(col).strip() for col in group.columns.values]
    group["count"] = df.groupby(genre_col).size()

    stats_path = os.path.join(output_dir, "genre_stats.csv")
    group.to_csv(stats_path)
    print(f"📈 Estadísticas guardadas en: {stats_path}")

    # Cargar top 10 géneros por promedio de energía (si existe)
    if "energy_mean" in group.columns:
        top10 = group.sort_values("energy_mean", ascending=False).head(10)
        top10_path = os.path.join(output_dir, "top10_genres.csv")
        top10.to_csv(top10_path)
        print(f"🏆 Top 10 géneros más energéticos guardado en: {top10_path}")
    else:
        print("⚠️ No se encontró columna 'energy' para generar el ranking.")

    print("🎉 ETL finalizado con éxito.")
    print("📂 Archivos generados dentro de /app/output/")

if __name__ == "__main__":
    main()
