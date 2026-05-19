#!/usr/bin/env python3
"""Generate consolidated StreamNord workshop notebooks."""

import json
import os


BASE = os.path.dirname(os.path.abspath(__file__))
NB_DIR = os.path.join(BASE, "notebooks")
os.makedirs(NB_DIR, exist_ok=True)


def make_nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"},
        },
        "cells": cells,
    }


def md(source):
    lines = source.split("\n")
    return {
        "cell_type": "markdown",
        "metadata": {"language": "markdown"},
        "source": [line + "\n" for line in lines[:-1]] + [lines[-1]],
    }


def code(source):
    lines = source.split("\n")
    return {
        "cell_type": "code",
        "metadata": {"language": "python"},
        "source": [line + "\n" for line in lines[:-1]] + [lines[-1]],
        "outputs": [],
        "execution_count": None,
    }


def write_nb(name, cells):
    path = os.path.join(NB_DIR, name)
    with open(path, "w") as handle:
        json.dump(make_nb(cells), handle, indent=1, ensure_ascii=False)
    print(f"  wrote {name} ({os.path.getsize(path)} bytes)")


def clear_notebooks():
    for entry in os.listdir(NB_DIR):
        if entry.endswith(".ipynb"):
            os.remove(os.path.join(NB_DIR, entry))


SETUP = 'import sys, os\nsys.path.insert(0, os.path.abspath(".."))'


def nb00():
    write_nb(
        "00_velkommen.ipynb",
        [
            md(
                "# 🎬 Workshopstart — Lea, signalet og baseline\n\n"
                "**Lea er i ferd med å forsvinne.**\n\n"
                "Hun er en av StreamNords mest aktive brukere. Hun elsker nordisk indie-drama\n"
                "og mørkere katalogtitler — men får de samme blockbusterne som alle andre.\n"
                "Produktteamet trenger et svar til møtet i morgen: **hva bør vi bygge?**\n\n"
                "Du er den nye ML-ingeniøren hos StreamNord — en norsk strømmetjeneste\n"
                "med ~5 000 aktive brukere og ~10 000 filmer i katalogen.\n"
                "Denne notatboken gjør fire ting: etablerer caset, forklarer signalet,\n"
                "setter opp evalueringen og måler den sterkeste enkle baselinen.\n\n"
                "---\n\n"
                "### Konsolidert workshopløp\n\n"
                "| Notebook | Rolle i workshopen |\n"
                "|---|---|\n"
                "| `00_velkommen` | Case, signal, metrikker og baseline |\n"
                "| `01_content_based` | Første personaliserte modell |\n"
                "| `02_collaborative_filtering` | CF og matrix factorization |\n"
                "| `03_hybrid_systems` | Hybrider, kontekst og fairness |\n"
                "| `04_ship_decision` | Sluttanbefaling og produksjonsvalg |\n\n"
                "Tyngre eller mer spesialisert stoff ligger som **valgfri appendix** inne i de relevante notebookene."
            ),
            md("## 1. Verifiser miljøet"),
            code(
                "import sys\n"
                "print(f'Python {sys.version}')\n\n"
                "import pandas as pd\n"
                "import numpy as np\n"
                "import scipy\n"
                "import sklearn\n"
                "import matplotlib\n\n"
                "print(f'pandas {pd.__version__}')\n"
                "print(f'numpy {np.__version__}')\n"
                "print(f'scipy {scipy.__version__}')\n"
                "print(f'scikit-learn {sklearn.__version__}')\n"
                "print(f'matplotlib {matplotlib.__version__}')\n\n"
                "try:\n"
                "    import implicit\n"
                "    print(f'implicit {implicit.__version__}')\n"
                "except ImportError:\n"
                "    print('implicit not installed')\n\n"
                "try:\n"
                "    import faiss\n"
                "    print('faiss OK')\n"
                "except ImportError:\n"
                "    print('faiss-cpu not installed')\n\n"
                "print('\\nAlle importer OK')"
            ),
            md("## 2. Last ned og klargjør data"),
            code(
                SETUP
                + "\n\nfrom data.sample_ml25m import sample_and_save, OUT_DIR\n\n"
                "if (OUT_DIR / 'interactions.parquet').exists():\n"
                "    print(f'Data finnes allerede i {OUT_DIR}')\n"
                "else:\n"
                "    sample_and_save()"
            ),
            md("## 3. Last inn interaksjoner og metadata"),
            code(
                "from src.data import load_interactions, load_item_metadata, GENRE_COLS\n\n"
                "interactions = load_interactions()\n"
                "items = load_item_metadata()\n\n"
                "n_users = interactions.user_id.nunique()\n"
                "n_items = interactions.item_id.nunique()\n"
                "n_interactions = len(interactions)\n"
                "sparsity = 1 - n_interactions / (n_users * n_items)\n\n"
                "print(f'Interaksjoner: {n_interactions:,} rader')\n"
                "print(f'Brukere:       {n_users:,}')\n"
                "print(f'Filmer:        {n_items:,}')\n"
                "print(f'Sparsitet:     {sparsity:.2%}')\n\n"
                "interactions.head()"
            ),
            md(
                "## 4. 📊 Møt Lea\n\n"
                "Lea (bruker 451) er en av StreamNords mest trofaste brukere — men de siste\n"
                "ukene har hun nesten sluttet å klikke. La oss se hva hun faktisk har sett."
            ),
            code(
                "LEA_ID = 451\n"
                "lea_items = interactions[interactions.user_id == LEA_ID].merge(items, on='item_id')\n"
                "print(f'Lea har sett {len(lea_items)} filmer. De siste 10:')\n"
                "lea_items.tail(10)[['title'] + GENRE_COLS[:6]]"
            ),
            code(
                "import matplotlib.pyplot as plt\n\n"
                "lea_genre_dist = lea_items[GENRE_COLS].sum().sort_values(ascending=True)\n"
                "fig, ax = plt.subplots(figsize=(10, 5))\n"
                "lea_genre_dist.plot.barh(ax=ax, color='coral')\n"
                "ax.set_xlabel('Antall filmer')\n"
                "ax.set_title('Leas sjangerfordeling')\n"
                "plt.tight_layout()\n"
                "plt.show()"
            ),
            md(
                "## 🏋️ Før vi kjører noen modell\n\n"
                "Skriv ned tre gjetninger før du ser resultatene:\n\n"
                "1. Hva slags filmer tror du Lea vil ha anbefalt?\n"
                "2. Hva tror du popularitetslisten vil inneholde?\n"
                "3. Tror du popularitet vil gi Lea en god opplevelse? Hvorfor / hvorfor ikke?"
            ),
            code(
                "# DINE GJETNINGER (skriv i kommentarene)\n"
                "#\n"
                "# 1. Lea vil sannsynligvis like: \n"
                "# 2. Popularitetslisten inneholder trolig: \n"
                "# 3. Popularitet fungerer / fungerer ikke for Lea fordi: \n"
                "#\n"
                "# Kom tilbake hit etter at popularitetsbaselinen har kjørt."
            ),
            md(
                "## 5. Hvilket signal har vi?\n\n"
                "### Eksplisitt vs implisitt feedback\n\n"
                "| Type | Eksempler | Fordel | Problem |\n"
                "|---|---|---|---|\n"
                "| **Eksplisitt** | Stjerner, likes, tommel opp | Tydelig preferanse | Sjelden i virkelige produkter |\n"
                "| **Implisitt** | Klikk, visning, kjøp, avspilling | Finnes i store mengder | Manglende data er tvetydig |\n\n"
                "StreamNord-dataene våre er hovedsakelig **implisitte**. Tenk på det slik:\n"
                "en rating er en melding — et klikk er bare et blikk. Vi har bare blikkene.\n\n"
                "Vi vet at Lea så noe, men ikke sikkert om hun aktivt likte det.\n"
                "Derfor betyr manglende interaksjon ikke automatisk avvisning."
            ),
            md(
                "## 6. Evalueringsoppsett\n\n"
                "Vi løser et **topp-N-rangeringsproblem**, ikke rating-prediksjon.\n\n"
                "### Metrikker\n\n"
                "- **Recall@K**: fant vi relevant innhold i topp-K?\n"
                "- **NDCG@K**: lå det høyt nok i listen?\n"
                "- **MAP@K**: hvor tidlig dukker treffet opp?\n\n"
                "I tillegg bruker vi en leave-one-out-splitt: siste interaksjon per bruker\n"
                "holdes tilbake som test."
            ),
            code(
                "from src.split import leave_one_out_split, build_sparse_matrix\n"
                "from src.metrics import recall_at_k, ndcg_at_k, map_at_k\n\n"
                "train_df, test_df = leave_one_out_split(interactions)\n"
                "n_users = interactions.user_id.max() + 1\n"
                "n_items = interactions.item_id.max() + 1\n"
                "train_matrix = build_sparse_matrix(train_df, n_users, n_items)\n"
                "user_ids = test_df['user_id'].values\n"
                "test_items = test_df['item_id'].values\n"
                "K = 10\n\n"
                "print(f'Trening: {len(train_df):,} interaksjoner')\n"
                "print(f'Test:    {len(test_df):,} interaksjoner (1 per bruker)')\n"
                "print(f'Matrise: {train_matrix.shape}, nnz={train_matrix.nnz:,}')"
            ),
            md(
                "## 7. Den late anbefalingen\n\n"
                "\"Gi alle det samme.\" Popularitet er den enkleste strategien —\n"
                "og overraskende vanskelig å slå. La oss se hva den gjør med Lea."
            ),
            code(
                "item_counts = np.asarray(train_matrix.sum(axis=0)).flatten()\n"
                "global_ranking = np.argsort(-item_counts)\n\n"
                "def recommend_popular(train_matrix, user_ids, k=10):\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n"
                "    for row_index, user_id in enumerate(user_ids):\n"
                "        seen = set(train_matrix[user_id].indices)\n"
                "        unseen_popular = [item_id for item_id in global_ranking if item_id not in seen][:k]\n"
                "        recommendations[row_index] = unseen_popular\n"
                "    return recommendations\n\n"
                "recs_pop = recommend_popular(train_matrix, user_ids, k=K)\n"
                "recall_value = recall_at_k(recs_pop, test_items, K)\n"
                "ndcg_value = ndcg_at_k(recs_pop, test_items, K)\n"
                "map_value = map_at_k(recs_pop, test_items, K)\n\n"
                "print(f'Popularitet: Recall@{K}={recall_value:.4f}  NDCG@{K}={ndcg_value:.4f}  MAP@{K}={map_value:.4f}')"
            ),
            code(
                "lea_idx = np.where(user_ids == LEA_ID)[0][0]\n"
                "overlap_0_100 = len(set(recs_pop[0]) & set(recs_pop[100])) / K\n"
                "overlap_0_lea = len(set(recs_pop[0]) & set(recs_pop[lea_idx])) / K\n"
                "print(f'Overlapp bruker 0 vs bruker 100: {overlap_0_100:.0%}')\n"
                "print(f'Overlapp bruker 0 vs Lea (451):  {overlap_0_lea:.0%}')\n\n"
                "lea_titles = items.set_index('item_id').loc[recs_pop[lea_idx]]\n"
                "print('\\nPopularitetsanbefalinger til Lea:')\n"
                "for rank, (_, row) in enumerate(lea_titles.iterrows(), 1):\n"
                "    genres = [genre for genre in GENRE_COLS if row.get(genre, 0) == 1]\n"
                "    genre_label = ', '.join(genres[:3])\n"
                "    print(f'  {rank:>2}. {row[\"title\"]}  [{genre_label}]')"
            ),
            md(
                "Lea elsker nordisk indie-drama. Popularitetslisten gir henne mainstream.\n"
                "**Noe stemmer ikke.**\n\n"
                "> ✅ **Sjekk gjetningene dine**\n>\n"
                "> Gå tilbake til gjetningene du skrev ned. Stemte de?\n"
                "> Hva overrasket deg med popularitetslisten til Lea?"
            ),
            md(
                "## Valgfri appendix — tilfeldig baseline\n\n"
                "Denne delen kan brukes hvis dere vil vise en helt naiv nedre grense.\n"
                "I kjerneflyten kan den hoppes over."
            ),
            code(
                "def recommend_random(train_matrix, user_ids, k=10, seed=42):\n"
                "    rng = np.random.default_rng(seed)\n"
                "    all_items = np.arange(train_matrix.shape[1])\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n"
                "    for row_index, user_id in enumerate(user_ids):\n"
                "        unseen = np.setdiff1d(all_items, train_matrix[user_id].indices)\n"
                "        recommendations[row_index] = rng.choice(unseen, size=k, replace=False)\n"
                "    return recommendations\n\n"
                "recs_rand = recommend_random(train_matrix, user_ids, k=K)\n"
                "print(f\"{'Modell':<14} {'Recall@10':>10} {'NDCG@10':>10} {'MAP@10':>10}\")\n"
                "print('-' * 48)\n"
                "for name, recs in [('Popularitet', recs_pop), ('Tilfeldig', recs_rand)]:\n"
                "    recall_value = recall_at_k(recs, test_items, K)\n"
                "    ndcg_value = ndcg_at_k(recs, test_items, K)\n"
                "    map_value = map_at_k(recs, test_items, K)\n"
                "    print(f'{name:<14} {recall_value:>10.4f} {ndcg_value:>10.4f} {map_value:>10.4f}')"
            ),
            md(
                "---\n\n"
                "> *Marte:* «Bra. Nå vet vi hva signalet betyr, og vi ser at popularitet ikke er nok.\n"
                "> Men Lea har en tydelig smak — sjangerprofilen viser det. Kan vi bruke den informasjonen\n"
                "> direkte til å bygge noe bedre? La oss finne ut.»\n\n"
                "**Neste steg** → `01_content_based.ipynb`"
            ),
        ],
    )


def nb01():
    write_nb(
        "01_content_based.ipynb",
        [
            md(
                "# 🏷️ Notebook 01 — Innholdsbasert filtering\n\n"
                "**Popularitetslisten ga Lea blockbustere. Kan metadata gi henne noe bedre?**\n\n"
                "Vi prøver den enkleste personlige modellen: bruk det vi *vet* om filmene\n"
                "til å finne flere som ligner på det Lea allerede liker.\n"
                "Embeddings og ANN ligger som valgfri appendix til slutt."
            ),
            md(
                "## Metadata: nyttig eller bare pent?\n\n"
                "Innholdsbasert filtering er som å anbefale bøker basert på omslaget —\n"
                "det fungerer, men det er begrenset. Vi bygger en brukerprofil fra item-features\n"
                "som sjanger, tekst eller metadata.\n\n"
                "### Styrker\n\n"
                "- fungerer for **nye items** uten interaksjonshistorikk\n"
                "- er lett å forklare og inspisere\n"
                "- gir ofte god sjangermatch tidlig\n\n"
                "### Svakheter\n\n"
                "- er begrenset av kvaliteten på features\n"
                "- kan bli smal og forutsigbar\n"
                "- ser ikke mønstre som bare blir synlige når mange brukere samspiller"
            ),
            md("## Oppsett"),
            code(
                SETUP
                + "\n\nimport numpy as np\n"
                "from src.data import load_interactions, load_item_metadata, get_genre_matrix, GENRE_COLS\n"
                "from src.split import leave_one_out_split, build_sparse_matrix\n"
                "from src.metrics import recall_at_k, ndcg_at_k\n\n"
                "interactions = load_interactions()\n"
                "items = load_item_metadata()\n"
                "train_df, test_df = leave_one_out_split(interactions)\n"
                "n_users = interactions.user_id.max() + 1\n"
                "n_items = interactions.item_id.max() + 1\n"
                "train_matrix = build_sparse_matrix(train_df, n_users, n_items)\n"
                "genre_matrix = get_genre_matrix(items)\n"
                "user_ids = test_df['user_id'].values\n"
                "test_items = test_df['item_id'].values\n"
                "K = 10\n"
                "LEA_ID = 451\n\n"
                "print(f'Genre-matrise: {genre_matrix.shape}')"
            ),
            md(
                "## 🏋️ Oppgave 1 — Innholdsbasert som første personalisering\n\n"
                "Se på Recall-kolonnen under. Endrer metadata noe for Lea?"
            ),
            code(
                "def recommend_content_based(train_matrix, genre_matrix, user_ids, k=10):\n"
                "    genre_norms = np.linalg.norm(genre_matrix, axis=1, keepdims=True)\n"
                "    genre_norms = np.where(genre_norms == 0, 1.0, genre_norms)\n"
                "    item_profiles = genre_matrix / genre_norms\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n\n"
                "    for row_index, user_id in enumerate(user_ids):\n"
                "        seen = train_matrix[user_id].indices\n"
                "        if len(seen) == 0:\n"
                "            recommendations[row_index] = np.arange(k)\n"
                "            continue\n"
                "        user_profile = item_profiles[seen].mean(axis=0)\n"
                "        profile_norm = np.linalg.norm(user_profile)\n"
                "        if profile_norm > 0:\n"
                "            user_profile = user_profile / profile_norm\n"
                "        scores = item_profiles @ user_profile\n"
                "        scores[seen] = -np.inf\n"
                "        recommendations[row_index] = np.argsort(-scores)[:k]\n"
                "    return recommendations\n\n"
                "item_counts = np.asarray(train_matrix.sum(axis=0)).flatten()\n"
                "global_ranking = np.argsort(-item_counts)\n\n"
                "def recommend_popular(train_matrix, user_ids, k=10):\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n"
                "    for row_index, user_id in enumerate(user_ids):\n"
                "        seen = set(train_matrix[user_id].indices)\n"
                "        unseen_popular = [item_id for item_id in global_ranking if item_id not in seen][:k]\n"
                "        recommendations[row_index] = unseen_popular\n"
                "    return recommendations\n\n"
                "recs_pop = recommend_popular(train_matrix, user_ids, k=K)\n"
                "recs_cb = recommend_content_based(train_matrix, genre_matrix, user_ids, k=K)\n\n"
                "print(f'Popularitet:    Recall@{K}={recall_at_k(recs_pop, test_items, K):.4f}  NDCG@{K}={ndcg_at_k(recs_pop, test_items, K):.4f}')\n"
                "print(f'Innholdsbasert: Recall@{K}={recall_at_k(recs_cb, test_items, K):.4f}  NDCG@{K}={ndcg_at_k(recs_cb, test_items, K):.4f}')"
            ),
            code(
                "lea_idx = np.where(user_ids == LEA_ID)[0]\n"
                "if len(lea_idx) > 0:\n"
                "    for name, recs in [('Popularitet', recs_pop), ('Innholdsbasert', recs_cb)]:\n"
                "        lea_recs = recs[lea_idx[0]]\n"
                "        titles = items.set_index('item_id').loc[lea_recs, 'title'].values\n"
                "        print(f'\\n{name}:')\n"
                "        for rank, title in enumerate(titles, 1):\n"
                "            print(f'  {rank:>2}. {title}')"
            ),
            md(
                "> 💬 **Diskuter**\n>\n"
                "> 1. Hjelper metadata Lea mer enn popularitet gjør? Hvordan ser du det?\n"
                "> 2. Når er innholdsbasert filtering spesielt nyttig i praksis?\n"
                "> 3. Hva er den største svakheten ved å bruke bare metadata?"
            ),
            md(
                "### ✏️ Skriveøvelse\n\n"
                "Skriv **én setning** til Marte som forklarer forskjellen mellom popularitet\n"
                "og innholdsbasert filtering — uten å bruke ordene *vektor*, *matrise* eller *cosine*.\n\n"
                "> *«Marte, forskjellen er at ...»*"
            ),
            md(
                "---\n\n"
                "> *Marte:* «Greit. Metadata hjelper, men det er fortsatt for grovt.\n"
                "> Hva skjer når Lea får hjelp av tusenvis av andre brukere som ligner på henne?»\n\n"
                "**Neste steg** → `02_collaborative_filtering.ipynb`"
            ),
            md(
                "## Valgfri appendix — embeddings og ANN\n\n"
                "Denne delen kan tas **etter** notebook 02 hvis dere vil koble content-based thinking\n"
                "til embeddings, visualisering og retrieval i produksjonsskala."
            ),
            code(
                "from implicit.als import AlternatingLeastSquares\n"
                "from sklearn.decomposition import PCA\n"
                "import matplotlib.pyplot as plt\n\n"
                "als = AlternatingLeastSquares(factors=64, regularization=0.01, iterations=15, random_state=42, use_gpu=False)\n"
                "als.fit(train_matrix, show_progress=True)\n"
                "item_emb = als.item_factors\n"
                "pca = PCA(n_components=2, random_state=42)\n"
                "item_2d = pca.fit_transform(item_emb)\n"
                "dominant_genre = genre_matrix.argmax(axis=1)\n\n"
                "fig, ax = plt.subplots(figsize=(10, 8))\n"
                "scatter = ax.scatter(item_2d[:, 0], item_2d[:, 1], c=dominant_genre, cmap='tab20', alpha=0.3, s=5)\n"
                "ax.set_title('ALS-item-embeddings (PCA)')\n"
                "plt.colorbar(scatter, ax=ax, label='Sjanger-indeks')\n"
                "plt.tight_layout()\n"
                "plt.show()"
            ),
            code(
                "try:\n"
                "    import faiss\n"
                "    emb = np.ascontiguousarray(item_emb.copy(), dtype=np.float32)\n"
                "    faiss.normalize_L2(emb)\n"
                "    queries = np.ascontiguousarray(als.user_factors[user_ids], dtype=np.float32)\n"
                "    faiss.normalize_L2(queries)\n\n"
                "    index = faiss.IndexFlatIP(emb.shape[1])\n"
                "    index.add(emb)\n"
                "    _, neighbor_ids = index.search(queries, K)\n"
                "    print(f'FAISS-indeks bygget. Første bruker fikk topp-{K}: {neighbor_ids[0].tolist()}')\n"
                "except ImportError:\n"
                "    print('faiss-cpu er ikke installert i dette miljøet.')"
            ),
        ],
    )


def nb02():
    write_nb(
        "02_collaborative_filtering.ipynb",
        [
            md(
                "# 👥 Notebook 02 — Collaborative filtering og ALS\n\n"
                "**Metadata ser filmene. Men hva om vi ser på *menneskene* i stedet?**\n\n"
                "Tusenvis av brukere har allerede fortalt oss hva de liker — gjennom handlingene sine.\n"
                "Nå lar vi det kollektive mønsteret hjelpe Lea. Vi går fra en enkel item-item-metode\n"
                "til den klassiske arbeidshesten **ALS matrisfaktorisering**."
            ),
            md(
                "## Fra nabolag til latente faktorer\n\n"
                "### Item-item collaborative filtering\n\n"
                "Vi slutter å lese filmomslaget og spør i stedet: *hvem andre så denne filmen,\n"
                "og hva så de etterpå?* Det er lett å forstå og gir en god inngang til\n"
                "collaborative filtering.\n\n"
                "### Matrix factorization\n\n"
                "I stedet for å sammenligne rå item-vektorer direkte, lærer vi latente faktorer:\n\n"
                "$$R \\approx U \\cdot V^T$$\n\n"
                "Her er $U$ brukerfaktorer og $V$ itemfaktorer. ALS er en effektiv måte å lære dette\n"
                "på for store, sparsomme implisitte datasett."
            ),
            md("## Oppsett"),
            code(
                SETUP
                + "\n\nimport numpy as np\n"
                "from sklearn.metrics.pairwise import cosine_similarity\n"
                "from src.data import load_interactions, load_item_metadata, GENRE_COLS\n"
                "from src.split import leave_one_out_split, build_sparse_matrix\n"
                "from src.metrics import recall_at_k, ndcg_at_k, map_at_k\n"
                "from implicit.als import AlternatingLeastSquares\n\n"
                "interactions = load_interactions()\n"
                "items = load_item_metadata()\n"
                "train_df, test_df = leave_one_out_split(interactions)\n"
                "n_users = interactions.user_id.max() + 1\n"
                "n_items = interactions.item_id.max() + 1\n"
                "train_matrix = build_sparse_matrix(train_df, n_users, n_items)\n"
                "user_ids = test_df['user_id'].values\n"
                "test_items = test_df['item_id'].values\n"
                "K = 10\n"
                "LEA_ID = 451\n\n"
                "print(f'Matrise: {train_matrix.shape}, nnz={train_matrix.nnz:,}')"
            ),
            md("## 🏋️ Oppgave 2 — Inspiser item-likhet"),
            code(
                "item_sim = cosine_similarity(train_matrix.T, dense_output=True)\n"
                "np.fill_diagonal(item_sim, 0.0)\n"
                "sample_items = items.sample(3, random_state=42)\n\n"
                "for _, row in sample_items.iterrows():\n"
                "    item_id = row['item_id']\n"
                "    if item_id >= item_sim.shape[0]:\n"
                "        continue\n"
                "    neighbors = np.argsort(-item_sim[item_id])[:5]\n"
                "    print(f'\\n\"{row[\"title\"]}\" ligner på:')\n"
                "    for neighbor_id in neighbors:\n"
                "        neighbor_row = items[items.item_id == neighbor_id]\n"
                "        if len(neighbor_row) > 0:\n"
                "            print(f'  {item_sim[item_id, neighbor_id]:.3f}  {neighbor_row.iloc[0][\"title\"]}')"
            ),
            md(
                "> 💬 **Diskuter**\n>\n"
                "> 1. Ser naboskapet meningsfullt ut?\n"
                "> 2. Hva fanger item-item-likheten som metadata alene ikke så godt viser?\n"
                "> 3. Hvorfor er dette fortsatt begrenset?"
            ),
            md(
                "## 🏋️ Oppgave 3 — Head-to-head: item-item vs ALS\n\n"
                "Nå setter vi de to mot hverandre. Se spesielt på Recall og NDCG —\n"
                "tar ALS et tydelig sprang?"
            ),
            code(
                "def recommend_item_item(item_sim, train_matrix, user_ids, k=10):\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n"
                "    for row_index, user_id in enumerate(user_ids):\n"
                "        user_vector = train_matrix[user_id]\n"
                "        scores = item_sim @ user_vector.T\n"
                "        scores = np.asarray(scores).flatten()\n"
                "        scores[user_vector.indices] = -np.inf\n"
                "        recommendations[row_index] = np.argsort(-scores)[:k]\n"
                "    return recommendations\n\n"
                "recs_item_item = recommend_item_item(item_sim, train_matrix, user_ids, k=K)\n\n"
                "als = AlternatingLeastSquares(factors=64, regularization=0.01, iterations=15, random_state=42, use_gpu=False)\n"
                "als.fit(train_matrix, show_progress=True)\n"
                "recs_als = als.recommend(user_ids, train_matrix[user_ids], N=K, filter_already_liked_items=True)[0]\n\n"
                "for name, recs in [('Item-item', recs_item_item), ('ALS', recs_als)]:\n"
                "    recall_value = recall_at_k(recs, test_items, K)\n"
                "    ndcg_value = ndcg_at_k(recs, test_items, K)\n"
                "    map_value = map_at_k(recs, test_items, K)\n"
                "    print(f'{name:<10} Recall@{K}={recall_value:.4f}  NDCG@{K}={ndcg_value:.4f}  MAP@{K}={map_value:.4f}')"
            ),
            code(
                "lea_idx = np.where(user_ids == LEA_ID)[0]\n"
                "if len(lea_idx) > 0:\n"
                "    for name, recs in [('Item-item', recs_item_item), ('ALS', recs_als)]:\n"
                "        lea_recs = recs[lea_idx[0]]\n"
                "        titles = items.set_index('item_id').loc[lea_recs, 'title'].values\n"
                "        print(f'\\n{name}:')\n"
                "        for rank, title in enumerate(titles, 1):\n"
                "            print(f'  {rank:>2}. {title}')"
            ),
            md(
                "ALS tar et tydelig sprang. Se på Leas lister — ser du forskjellen?\n\n"
                "> 💬 **Diskuter**\n>\n"
                "> 1. Hvorfor vinner ALS ofte over item-item?\n"
                "> 2. Hva er forskjellen på en nabolagsmetode og latente faktorer?\n"
                "> 3. Ser ALS mer ut som et realistisk produksjonsvalg enn item-item? Hvorfor?"
            ),
            md(
                "### 🔄 Refleksjon — sjekk prediksjonen din\n\n"
                "Gå tilbake til gjetningene du skrev ned i notebook 00.\n\n"
                "> 1. Hadde du rett om hva Lea ville like?\n"
                "> 2. Stemte gjetningen din om popularitetslisten?\n"
                "> 3. Hva har overrasket deg mest så langt?"
            ),
            md(
                "---\n\n"
                "> *Marte:* «Bra. Nå ser det ut som Lea kan få bedre anbefalinger.\n"
                "> Men fungerer dette for *alle* — eller bare for mainstream-brukerne?\n"
                "> Og hva skjer når vi må blande signaler og ta fairness på alvor?»\n\n"
                "**Neste steg** → `03_hybrid_systems.ipynb`"
            ),
            md(
                "## Valgfri appendix — faktorsveip og tolkning\n\n"
                "Denne delen er nyttig hvis dere vil grave dypere i hvordan ALS oppfører seg,\n"
                "men den er ikke nødvendig for kjerneflyten."
            ),
            code(
                "import matplotlib.pyplot as plt\n\n"
                "factor_values = [16, 32, 64, 128, 256]\n"
                "recall_per_factor = []\n"
                "for factor_count in factor_values:\n"
                "    model = AlternatingLeastSquares(factors=factor_count, regularization=0.01, iterations=15, random_state=42, use_gpu=False)\n"
                "    model.fit(train_matrix, show_progress=False)\n"
                "    recs = model.recommend(user_ids, train_matrix[user_ids], N=K, filter_already_liked_items=True)[0]\n"
                "    recall_per_factor.append(recall_at_k(recs, test_items, K))\n\n"
                "fig, ax = plt.subplots(figsize=(8, 4))\n"
                "ax.plot(factor_values, recall_per_factor, 'o-', linewidth=2)\n"
                "ax.set_xlabel('Antall faktorer')\n"
                "ax.set_ylabel(f'Recall@{K}')\n"
                "ax.set_title('ALS: Recall vs antall faktorer')\n"
                "plt.tight_layout()\n"
                "plt.show()"
            ),
            code(
                "from sklearn.metrics.pairwise import cosine_similarity as cosine_sim\n\n"
                "user_emb = als.user_factors\n"
                "lea_emb = user_emb[LEA_ID]\n"
                "sims = cosine_sim(lea_emb.reshape(1, -1), user_emb)[0]\n"
                "sims[LEA_ID] = -1\n"
                "top_neighbors = np.argsort(-sims)[:5]\n\n"
                "print('Leas nærmeste naboer i ALS-rommet:')\n"
                "for neighbor_user_id in top_neighbors:\n"
                "    neighbor_items = interactions[interactions.user_id == neighbor_user_id].merge(items, on='item_id')\n"
                "    top_genres = neighbor_items[GENRE_COLS].sum().nlargest(3).index.tolist()\n"
                "    genre_label = ', '.join(top_genres)\n"
                "    print(f'  Bruker {neighbor_user_id} (sim={sims[neighbor_user_id]:.3f}, topp-sjangre: {genre_label})')"
            ),
        ],
    )


def nb03():
    write_nb(
        "03_hybrid_systems.ipynb",
        [
            md(
                "# 🔀 Notebook 03 — Hybrider, kontekst og fairness\n\n"
                "**ALS gir Lea bedre anbefalinger. Men fungerer det for *alle*?**\n\n"
                "Nå går vi fra modell til produkt. Vi kombinerer langtidsprofil med korttidskontekst\n"
                "og sjekker om systemet faktisk er godt nok for flere enn mainstream-brukerne."
            ),
            md(
                "## Hvorfor étt verktøy aldri er nok\n\n"
                "Du bruker ikke bare en hammer til å bygge et hus. Samme med anbefalingssystemer —\n"
                "ingen enkeltmodell løser hele produktproblemet:\n\n"
                "- **Popularitet** er robust, men upersonlig\n"
                "- **Innholdsbasert** hjelper ved nye items og tynne signaler\n"
                "- **ALS** gir sterk personalisering når det finnes data\n"
                "- **Kontekst og reranking** hjelper når brukerens situasjon eller produktkrav endrer seg\n\n"
                "Hybrider lar oss kombinere disse styrkene."
            ),
            md("## Oppsett"),
            code(
                SETUP
                + "\n\nimport numpy as np\nimport matplotlib.pyplot as plt\n"
                "from scipy.sparse import lil_matrix, diags\n"
                "from implicit.als import AlternatingLeastSquares\n"
                "from src.data import load_interactions, load_item_metadata, load_sessions, get_genre_matrix\n"
                "from src.split import leave_one_out_split, build_sparse_matrix, session_train_test_split\n"
                "from src.metrics import recall_at_k, coverage, novelty\n"
                "from src.fairness import popularity_bias_analysis, genre_calibration_score, group_recall_comparison\n"
                "from src.rerank import mmr_rerank\n\n"
                "interactions = load_interactions()\n"
                "items = load_item_metadata()\n"
                "sessions = load_sessions()\n"
                "train_df, test_df = leave_one_out_split(interactions)\n"
                "n_users = interactions.user_id.max() + 1\n"
                "n_items = interactions.item_id.max() + 1\n"
                "train_matrix = build_sparse_matrix(train_df, n_users, n_items)\n"
                "genre_matrix = get_genre_matrix(items)\n"
                "user_ids = test_df['user_id'].values\n"
                "test_items = test_df['item_id'].values\n"
                "K = 10\n"
                "LEA_ID = 451\n\n"
                "als = AlternatingLeastSquares(factors=64, regularization=0.01, iterations=15, random_state=42, use_gpu=False)\n"
                "als.fit(train_matrix, show_progress=True)\n"
                "recs_als = als.recommend(user_ids, train_matrix[user_ids], N=K, filter_already_liked_items=True)[0]\n"
                "item_pop_counts = np.asarray(train_matrix.sum(axis=0)).flatten()\n"
                "item_pop_frac = item_pop_counts / n_users\n\n"
                "print('Oppsett ferdig')"
            ),
            md("## 🏋️ Oppgave 4 — Korttidskontekst som hybridsignal"),
            code(
                "sess_sizes = sessions.groupby('session_id').size()\n"
                "print(f'Antall sesjoner: {len(sess_sizes):,}')\n"
                "print(f'Sesjonslengde — min: {sess_sizes.min()}, median: {sess_sizes.median():.0f}, maks: {sess_sizes.max()}')\n\n"
                "lea_sessions = sessions[sessions.user_id == LEA_ID]\n"
                "lea_session_ids = lea_sessions.session_id.unique()\n"
                "print(f'Lea har {len(lea_session_ids)} sesjoner')"
            ),
            code(
                "train_sessions, test_sessions = session_train_test_split(sessions, interactions)\n"
                "counts = lil_matrix((n_items, n_items), dtype=np.float64)\n"
                "sorted_sessions = train_sessions.sort_values(['session_id', 'position'])\n"
                "prev_item, prev_session = -1, -1\n"
                "for _, row in sorted_sessions.iterrows():\n"
                "    session_id, item_id = row['session_id'], row['item_id']\n"
                "    if session_id == prev_session and prev_item >= 0:\n"
                "        counts[prev_item, item_id] += 1\n"
                "    prev_item, prev_session = item_id, session_id\n"
                "transition = counts.tocsr()\n"
                "row_sums = np.asarray(transition.sum(axis=1)).flatten()\n"
                "row_sums[row_sums == 0] = 1.0\n"
                "transition = diags(1.0 / row_sums) @ transition\n\n"
                "def recommend_session_blend(als_model, transition, test_sessions, train_matrix, k=10, lambda_=0.7):\n"
                "    dense_transition = transition.toarray() if hasattr(transition, 'toarray') else transition\n"
                "    recommendations, ground_truth = [], []\n"
                "    for _, group in test_sessions.groupby('session_id'):\n"
                "        group = group.sort_values('position')\n"
                "        if len(group) < 2:\n"
                "            continue\n"
                "        user_id = group['user_id'].iloc[0]\n"
                "        context_items = group['item_id'].values[:-1].tolist()\n"
                "        target_item = group['item_id'].values[-1]\n\n"
                "        als_scores = als_model.user_factors[user_id] @ als_model.item_factors.T\n"
                "        als_scores = (als_scores - als_scores.min()) / max(als_scores.max() - als_scores.min(), 1e-10)\n\n"
                "        session_scores = np.zeros(dense_transition.shape[0])\n"
                "        weight = 1.0\n"
                "        for item_id in reversed(context_items[-3:]):\n"
                "            if 0 <= item_id < dense_transition.shape[0]:\n"
                "                session_scores += weight * dense_transition[item_id]\n"
                "            weight *= 0.8\n"
                "        if session_scores.max() > 0:\n"
                "            session_scores = session_scores / session_scores.max()\n\n"
                "        blended = lambda_ * als_scores + (1 - lambda_) * session_scores\n"
                "        seen = set(train_matrix[user_id].indices) | set(context_items)\n"
                "        for seen_item in seen:\n"
                "            if 0 <= seen_item < len(blended):\n"
                "                blended[seen_item] = -np.inf\n"
                "        recommendations.append(np.argsort(-blended)[:k])\n"
                "        ground_truth.append(target_item)\n"
                "    return np.array(recommendations), np.array(ground_truth)\n\n"
                "for lambda_value in [0.0, 0.7, 1.0]:\n"
                "    recs, targets = recommend_session_blend(als, transition, test_sessions, train_matrix, k=K, lambda_=lambda_value)\n"
                "    print(f'lambda={lambda_value:.1f}: Recall@{K}={recall_at_k(recs, targets, K):.4f}')"
            ),
            md(
                "> 💬 **Diskuter**\n>\n"
                "> 1. Hvorfor kan en kombinasjon av langtidsprofil og sesjon være bedre enn bare én av delene?\n"
                "> 2. Hvem hjelper korttidskontekst mest?\n"
                "> 3. Hva sier dette om hvorfor ekte systemer blir hybride?"
            ),
            md(
                "## 🏋️ Oppgave 5 — Fairness og reranking\n\n"
                "Høy gjennomsnittlig Recall betyr ikke at alle brukere er fornøyde.\n"
                "Se på grafen under — hvem tjener, og hvem taper?"
            ),
            code(
                "bias_df = popularity_bias_analysis(recs_als, item_pop_counts, k=K)\n"
                "group_df = group_recall_comparison(recs_als, test_items, train_matrix, item_pop_counts, K)\n\n"
                "print(bias_df)\n\n"
                "fig, ax = plt.subplots(figsize=(10, 5))\n"
                "width = 0.35\n"
                "x = range(len(bias_df))\n"
                "ax.bar([idx - width / 2 for idx in x], bias_df['share_catalogue'], width, label='Andel i katalog')\n"
                "ax.bar([idx + width / 2 for idx in x], bias_df['share_recommended'], width, label='Andel i anbefalinger')\n"
                "ax.set_xticks(list(x))\n"
                "ax.set_xticklabels(bias_df['bin'], rotation=20, ha='right')\n"
                "ax.set_ylabel('Andel')\n"
                "ax.set_title('Popularitetsbias: katalog vs anbefalinger')\n"
                "ax.legend()\n"
                "plt.tight_layout()\n"
                "plt.show()\n\n"
                "print('Recall@K per brukergruppe (ALS):')\n"
                "print(group_df.to_string(index=False))"
            ),
            code(
                "def apply_mmr(als_model, user_ids, train_matrix, genre_matrix, k=10, lambda_=0.6, n_cand=50):\n"
                "    candidate_ids, candidate_scores = als_model.recommend(user_ids, train_matrix[user_ids], N=n_cand, filter_already_liked_items=True)\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n"
                "    for row_index in range(len(user_ids)):\n"
                "        recommendations[row_index] = mmr_rerank(candidate_ids[row_index], candidate_scores[row_index], genre_matrix, k=k, lambda_=lambda_)\n"
                "    return recommendations\n\n"
                "recs_mmr = apply_mmr(als, user_ids, train_matrix, genre_matrix, k=K, lambda_=0.6)\n\n"
                "rows = []\n"
                "for name, recs in [('ALS', recs_als), ('ALS+MMR', recs_mmr)]:\n"
                "    rows.append((name, recall_at_k(recs, test_items, K), coverage(recs, n_items, K), novelty(recs, item_pop_frac, K)))\n\n"
                "print(f\"{'Modell':<10} {'Recall@10':>10} {'Coverage':>10} {'Novelty':>10}\")\n"
                "print('-' * 46)\n"
                "for name, recall_value, coverage_value, novelty_value in rows:\n"
                "    print(f'{name:<10} {recall_value:>10.4f} {coverage_value:>10.4f} {novelty_value:>10.2f}')"
            ),
            md(
                "Recall går litt ned. Coverage og novelty går opp. Det er en **eksplisitt tradeoff** — ikke en feil.\n\n"
                "> 💬 **Diskuter**\n>\n"
                "> 1. Hvem taper på en ren ALS-modell?\n"
                "> 2. Hva vinner vi og hva taper vi når vi re-rangerer for mangfold?\n"
                "> 3. Hva ville du fortalt Amira om systemets styrker og svakheter akkurat nå?"
            ),
            md(
                "---\n\n"
                "> *Amira:* «Bra. Nå har dere vist at hybrider kan hjelpe, og at fairness må måles.\n"
                "> Men det er én ting vi ikke har testet: hva skjer med alt dette når brukeren er helt ny?\n"
                "> Og hva anbefaler dere faktisk at StreamNord shipper?»\n\n"
                "**Neste steg** → `04_ship_decision.ipynb`"
            ),
            md(
                "## Valgfri appendix — kalibrering\n\n"
                "Hvis dere vil gå dypere i fairness, kan dere måle om anbefalingene matcher\n"
                "brukerens faktiske sjangerprofil."
            ),
            code(
                "cal_als, cal_mmr = [], []\n"
                "for row_index, user_id in enumerate(user_ids[:500]):\n"
                "    cal_als.append(genre_calibration_score(user_id, recs_als[row_index], train_matrix, genre_matrix))\n"
                "    cal_mmr.append(genre_calibration_score(user_id, recs_mmr[row_index], train_matrix, genre_matrix))\n\n"
                "print('Kalibrerings-KL (lavere = bedre):')\n"
                "print(f'  ALS:     {np.mean(cal_als):.4f}')\n"
                "print(f'  ALS+MMR: {np.mean(cal_mmr):.4f}')"
            ),
        ],
    )


def nb04():
    write_nb(
        "04_ship_decision.ipynb",
        [
            md(
                "# 🚀 Notebook 04 — Sluttanbefaling\n\n"
                "**Det er møtetid. Marte venter på svaret ditt.**\n\n"
                "Popularitet ga oss en baseline, metadata ga oss cold-start-støtte, ALS ga oss styrke,\n"
                "og hybridtenkningen ga oss produktrealismen. Nå samler vi trådene og svarer:\n"
                "**hva bør StreamNord faktisk shippe?**"
            ),
            md("## Oppsett"),
            code(
                SETUP
                + "\n\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport pandas as pd\n"
                "from scipy.sparse import lil_matrix\n"
                "from src.data import load_interactions, load_item_metadata, get_genre_matrix\n"
                "from src.split import leave_one_out_split, build_sparse_matrix\n"
                "from src.metrics import recall_at_k, ndcg_at_k, map_at_k, coverage, novelty\n"
                "from src.rerank import mmr_rerank\n"
                "from src.recommenders.popularity import PopularityRecommender\n"
                "from src.recommenders.item_item import ItemItemRecommender\n"
                "from src.recommenders.als import ALSRecommender\n"
                "from src.recommenders.content_based import ContentBasedRecommender\n\n"
                "interactions = load_interactions()\n"
                "items = load_item_metadata()\n"
                "train_df, test_df = leave_one_out_split(interactions)\n"
                "n_users = interactions.user_id.max() + 1\n"
                "n_items = interactions.item_id.max() + 1\n"
                "train_matrix = build_sparse_matrix(train_df, n_users, n_items)\n"
                "genre_matrix = get_genre_matrix(items)\n"
                "user_ids = test_df['user_id'].values\n"
                "test_items = test_df['item_id'].values\n"
                "K = 10\n"
                "item_pop = np.asarray(train_matrix.sum(axis=0)).flatten() / n_users\n"
                "LEA_ID = 451\n\n"
                "print('Oppsett ferdig')"
            ),
            md(
                "## 🏋️ Oppgave 6 — Leaderboard for modellfamiliene\n\n"
                "Alle modellene side om side. Se ikke bare på Recall —\n"
                "sjekk coverage og novelty. Hva forteller de?"
            ),
            code(
                "pop = PopularityRecommender().fit(train_matrix)\n"
                "item_item = ItemItemRecommender().fit(train_matrix)\n"
                "als = ALSRecommender(factors=64).fit(train_matrix)\n"
                "content = ContentBasedRecommender().fit(genre_matrix)\n\n"
                "models = {\n"
                "    'Popularitet': pop.recommend(user_ids, train_matrix, K),\n"
                "    'Innholdsbasert': content.recommend(user_ids, train_matrix, K),\n"
                "    'Item-item': item_item.recommend(user_ids, train_matrix, K),\n"
                "    'ALS': als.recommend(user_ids, train_matrix, K),\n"
                "}\n\n"
                "cand_ids, cand_scores = als.model.recommend(user_ids, train_matrix[user_ids], N=50, filter_already_liked_items=True)\n"
                "recs_mmr = np.zeros((len(user_ids), K), dtype=np.int32)\n"
                "for row_index in range(len(user_ids)):\n"
                "    recs_mmr[row_index] = mmr_rerank(cand_ids[row_index], cand_scores[row_index], genre_matrix, k=K, lambda_=0.6)\n"
                "models['ALS+MMR'] = recs_mmr\n\n"
                "results = {}\n"
                "for name, recs in models.items():\n"
                "    results[name] = {\n"
                "        f'recall@{K}': recall_at_k(recs, test_items, K),\n"
                "        f'ndcg@{K}': ndcg_at_k(recs, test_items, K),\n"
                "        f'map@{K}': map_at_k(recs, test_items, K),\n"
                "        f'coverage@{K}': coverage(recs, n_items, K),\n"
                "        f'novelty@{K}': novelty(recs, item_pop, K),\n"
                "    }\n\n"
                "leaderboard = pd.DataFrame(results).T.sort_values(f'ndcg@{K}', ascending=False)\n"
                "print(leaderboard.to_string(float_format=lambda value: f'{value:.4f}'))"
            ),
            md(
                "## 📋 Beslutningsmal\n\n"
                "Fyll inn malen nedenfor før du skriver anbefalingen til Marte.\n"
                "Ta den med deg etter workshopen — den er gjenbrukbar."
            ),
            code(
                "# BESLUTNINGSMAL — Anbefalingssystem\n"
                "#\n"
                "# 1. SIGNALTYPE\n"
                "#    Hovedsakelig eksplisitt / implisitt / begge: \n"
                "#\n"
                "# 2. ANBEFALT MODELLFAMILIE\n"
                "#    Kjernemodell: \n"
                "#    Hvorfor denne: \n"
                "#\n"
                "# 3. COLD-START-STRATEGI\n"
                "#    For nye brukere: \n"
                "#    For nye items: \n"
                "#\n"
                "# 4. FAIRNESS OG MANGFOLD\n"
                "#    Hovedrisiko: \n"
                "#    Tiltak: \n"
                "#\n"
                "# 5. PRODUKSJONSARKITEKTUR\n"
                "#    Kandidatgenerering: \n"
                "#    Rangering: \n"
                "#    Re-rangering: \n"
                "#\n"
                "# 6. KJENTE RISIKOER\n"
                "#    Hva kan gå galt: \n"
                "#    Hva mangler vi data for: \n"
            ),
            md(
                "## 🏋️ Oppgave 7 — Hva anbefaler du å shippe?\n\n"
                "Bruk malen du nettopp fylte ut. Skriv en kort anbefaling til Marte — ikke tenk bare\n"
                "på hva som vinner én metrikk, men på hvilket system som faktisk er mest realistisk."
            ),
            md(
                "> **Skriv din anbefaling her**\n>\n"
                "> *«Marte, basert på analysen anbefaler jeg ... fordi ...»*"
            ),
            md(
                "## 🏋️ Oppgave 8 — Cold start\n\n"
                "Hva skjer når en ny bruker dukker opp — og ALS har *ingenting* å jobbe med?"
            ),
            code(
                "def evaluate_cold_start(als_rec, train_matrix, test_df, history_sizes=(1, 3, 5, 10, 20, 50), k=10):\n"
                "    rng = np.random.default_rng(42)\n"
                "    user_ids = test_df['user_id'].values\n"
                "    test_items = test_df['item_id'].values\n"
                "    rows = []\n"
                "    for history_size in history_sizes:\n"
                "        masked = lil_matrix(train_matrix.shape, dtype=np.float32)\n"
                "        for user_id in user_ids:\n"
                "            seen = train_matrix[user_id].indices\n"
                "            keep = seen if len(seen) <= history_size else rng.choice(seen, size=history_size, replace=False)\n"
                "            masked[user_id, keep] = 1.0\n"
                "        masked_csr = masked.tocsr()\n"
                "        recs = als_rec.model.recommend(user_ids, masked_csr[user_ids], N=k, filter_already_liked_items=True, recalculate_user=True)[0]\n"
                "        rows.append({'history_size': history_size, f'recall@{k}': recall_at_k(recs, test_items, k)})\n"
                "    return rows\n\n"
                "cold_start_rows = evaluate_cold_start(als, train_matrix, test_df)\n"
                "cold_start_df = pd.DataFrame(cold_start_rows)\n"
                "print(cold_start_df.to_string(index=False))\n\n"
                "fig, ax = plt.subplots(figsize=(8, 5))\n"
                "ax.plot(cold_start_df['history_size'], cold_start_df[f'recall@{K}'], 'o-', linewidth=2)\n"
                "ax.set_xlabel('Antall interaksjoner i historikk')\n"
                "ax.set_ylabel(f'Recall@{K}')\n"
                "ax.set_title('Cold-start: ALS-ytelse vs historikkstørrelse')\n"
                "plt.tight_layout()\n"
                "plt.show()"
            ),
            md(
                "## Produksjonsarkitektur\n\n"
                "```\n"
                "Kandidatgenerering  ->  Rangering  ->  Re-rangering\n"
                "  (enkle signaler)      (sterk modell)     (fairness/regler)\n"
                "```\n\n"
                "### En realistisk anbefaling\n\n"
                "- bruk **ALS** eller en tilsvarende sterk collaborative modell som hovedmotor\n"
                "- bruk **innholdsbaserte signaler** for cold start og forklarbarhet\n"
                "- bruk **reranking** for mangfold, fairness og produktkrav\n"
                "- legg til **kontekst** når det gir tydelig verdi"
            ),
            md("## 🎬 Leas reise gjennom workshopen"),
            code(
                "lea_idx = np.where(user_ids == LEA_ID)[0]\n"
                "if len(lea_idx) > 0:\n"
                "    print('Leas anbefalinger gjennom workshopen:')\n"
                "    print('=' * 50)\n"
                "    for name in ['Popularitet', 'Innholdsbasert', 'ALS', 'ALS+MMR']:\n"
                "        lea_recs = models[name][lea_idx[0]]\n"
                "        titles = items.set_index('item_id').loc[lea_recs[:5], 'title'].values\n"
                "        print(f'\\n{name}:')\n"
                "        for rank, title in enumerate(titles, 1):\n"
                "            print(f'  {rank}. {title}')\n"
                "    print('\\n-> Fra mainstream-spam til en mer personlig og balansert liste.')"
            ),
            md(
                "### 🔄 Refleksjon — sjekk gjetningene fra starten\n\n"
                "Gå tilbake til notebook 00 og les gjetningene du skrev ned.\n\n"
                "> 1. Hva hadde du rett i?\n"
                "> 2. Hva tok du feil om?\n"
                "> 3. Hva overrasket deg mest gjennom hele workshopen?"
            ),
            md(
                "## 🔑 Oppsummering\n\n"
                "| # | Lærdom |\n"
                "|---|--------|\n"
                "| 1 | **Signalet betyr noe** — implisitt data må tolkes annerledes enn eksplisitt feedback |\n"
                "| 2 | **Baselines er viktige** — popularitet er enkel, sterk og utilstrekkelig |\n"
                "| 3 | **Metadata hjelper tidlig** — content-based filtering er nyttig, men begrenset |\n"
                "| 4 | **Collaborative filtering skaper et hopp** — ALS lærer struktur metadata ikke ser |\n"
                "| 5 | **Hybrider vinner i praksis** — produktkrav tvinger frem flere signaler |\n"
                "| 6 | **Fairness må måles** — høy gjennomsnittlig relevans er ikke nok |\n\n"
                "### Ressurser\n\n"
                "- Hu, Koren & Volinsky (2008): *Collaborative Filtering for Implicit Feedback*\n"
                "- Koren, Bell & Volinsky (2009): *Matrix Factorization Techniques*\n"
                "- Sarwar et al. (2001): *Item-based Collaborative Filtering Recommendation Algorithms*\n"
                "- He et al. (2017): *Neural Collaborative Filtering*\n"
                "- Steck (2018): *Calibrated Recommendations*\n"
                "- Abdollahpouri et al. (2020): *Popularity Bias in Recommendation*"
            ),
        ],
    )


if __name__ == "__main__":
    clear_notebooks()
    nb00()
    nb01()
    nb02()
    nb03()
    nb04()
    print("\nAll 5 notebooks generated!")