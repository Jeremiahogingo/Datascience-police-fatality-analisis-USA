import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parents[1]
    data_path = repo_root / 'Deaths_by_Police_US.csv'
    out_dir = repo_root / 'assets'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / 'example_viz.png'

    # Read dataset with minimal parsing - be tolerant to format/encoding issues
    try:
        df = pd.read_csv(data_path, low_memory=False, encoding='utf-8')
    except Exception:
        # Fall back to latin-1 which is common for Windows-saved CSVs
        df = pd.read_csv(data_path, low_memory=False, encoding='latin-1')

    # Prepare 'armed' text values
    df['armed'] = df.get('armed').fillna('Unarmed').astype(str).str.strip()
    df['armed'] = df['armed'].replace({'': 'Unknown', 'nan': 'Unarmed'})

    # Compute top 10 weapon labels
    counts = df['armed'].value_counts().head(10).sort_values()

    # Plot horizontal bar chart
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot.barh(ax=ax, color='tab:blue')
    ax.set_xlabel('Number of fatalities')
    ax.set_ylabel('Weapon / Armed status')
    ax.set_title('Top 10 `armed` labels in Deaths_by_Police_US.csv')
    for i, v in enumerate(counts):
        ax.text(v + max(counts) * 0.01, i, str(v), va='center')

    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    print(f'Wrote example visualization to: {out_png}')


if __name__ == '__main__':
    main()
