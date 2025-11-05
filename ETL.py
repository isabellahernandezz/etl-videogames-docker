cat > ETL.py << 'EOF'
import pandas as pd
import argparse
import os

def extract(input_file):
    print("📥 Extrayendo datos desde:", input_file)
    return pd.read_csv(input_file)

def transform(df):
    print("⚙️ Transformando datos...")
    df = df.dropna(subset=['Genre', 'Global_Sales'])
    df['Global_Sales'] = pd.to_numeric(df['Global_Sales'], errors='coerce').fillna(0)

    # Calcular estadísticas por género
    genre_stats = df.groupby('Genre', as_index=False).agg({
        'Global_Sales': 'sum',
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum'
    })
    genre_stats['Rank_Score'] = (
        genre_stats['Global_Sales'] * 1.5 +
        genre_stats['NA_Sales'] +
        genre_stats['EU_Sales'] +
        genre_stats['JP_Sales'] * 0.5
    )
    return genre_stats

def load(df, output_dir):
    print("💾 Cargando resultados...")
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, "genre_stats.csv"), index=False)
    top10 = df.sort_values(by="Rank_Score", ascending=False).head(10)
    top10.to_csv(os.path.join(output_dir, "top10_genres.csv"), index=False)
    print("✅ Archivos generados en:", output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Video Game Genres 2024")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="output")
    args = parser.parse_args()

    df = extract(args.input)
    transformed = transform(df)
    load(transformed, args.out_dir)
    print("🎮 ETL completado correctamente.")
EOF
