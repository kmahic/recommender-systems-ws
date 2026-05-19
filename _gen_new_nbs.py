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
                "### Hva betyr sparsiteten?\n\n"
                "Over 99 % av matrisen er tom. Det betyr at en gjennomsnittlig bruker har sett\n"
                "kanskje 50 av 10 000 filmer. Det meste vi *ikke* ser er ukjent — ikke mislikt.\n"
                "Denne forskjellen er viktig: modellene våre må lære av det lille vi har,\n"
                "uten å anta at fravær av klikk betyr avvisning."
            ),
            md(
                "## 4. 📊 Møt Lea og Jonas\n\n"
                "Lea (bruker 451) er en av StreamNords mest trofaste brukere — men de siste\n"
                "ukene har hun nesten sluttet å klikke. La oss se hva hun faktisk har sett.\n\n"
                "Jonas (bruker 102) elsker blockbustere — alt fra Marvel til Star Wars.\n"
                "Han klikker på det meste som ligger på forsiden. Disse to representerer\n"
                "ytterpunktene av brukerbasens vår: **nisjesmak vs mainstream**."
            ),
            code(
                "LEA_ID = 451\n"
                "JONAS_ID = 102\n\n"
                "lea_items = interactions[interactions.user_id == LEA_ID].merge(items, on='item_id')\n"
                "jonas_items = interactions[interactions.user_id == JONAS_ID].merge(items, on='item_id')\n"
                "print(f'Lea har sett {len(lea_items)} filmer. Jonas har sett {len(jonas_items)} filmer.')\n"
                "print(f'\\nLeas siste 10 filmer:')\n"
                "lea_items.tail(10)[['title'] + GENRE_COLS[:6]]"
            ),
            code(
                "print('Jonas sine siste 10 filmer:')\n"
                "jonas_items.tail(10)[['title'] + GENRE_COLS[:6]]"
            ),
            code(
                "import matplotlib.pyplot as plt\n\n"
                "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n\n"
                "lea_genre_dist = lea_items[GENRE_COLS].sum().sort_values(ascending=True)\n"
                "lea_genre_dist.plot.barh(ax=axes[0], color='coral')\n"
                "axes[0].set_xlabel('Antall filmer')\n"
                "axes[0].set_title('Lea — sjangerfordeling')\n\n"
                "jonas_genre_dist = jonas_items[GENRE_COLS].sum().sort_values(ascending=True)\n"
                "jonas_genre_dist.plot.barh(ax=axes[1], color='steelblue')\n"
                "axes[1].set_xlabel('Antall filmer')\n"
                "axes[1].set_title('Jonas — sjangerfordeling')\n\n"
                "plt.tight_layout()\n"
                "plt.show()"
            ),
            md(
                "## 🏋️ Før vi kjører noen modell\n\n"
                "Skriv ned gjetningene dine **før** du ser resultatene.\n"
                "Vi kommer tilbake til disse i notebook 04 for å se om du hadde rett.\n\n"
                "Vær så spesifikk du kan — det er lærerikt å ta feil."
            ),
            code(
                "# DINE GJETNINGER — fyll inn før du kjører neste celle\n"
                "#\n"
                "# 1. Hva slags filmer tror du Lea vil ha anbefalt?\n"
                "#    Svar: \n"
                "#\n"
                "# 2. Hva tror du popularitetslisten vil inneholde?\n"
                "#    Svar: \n"
                "#\n"
                "# 3. Vil popularitet fungere bedre for Lea eller Jonas? Hvorfor?\n"
                "#    Svar: \n"
                "#\n"
                "# 4. Hvor sikker er du på gjetning 3? (1 = ren gjetning, 5 = helt sikker)\n"
                "#    Sikkerhet: \n"
                "#\n"
                "# Tips: Kom tilbake hit i notebook 04 og sammenlign."
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
                "Vi løser et **topp-N-rangeringsproblem**: gitt en bruker, ranger alle filmer\n"
                "slik at det brukeren *faktisk* vil se havner blant topp K.\n\n"
                "### Leave-one-out-splitt\n\n"
                "Vi gjemmer den siste filmen hver bruker så, og spør: ville modellen funnet den?\n"
                "Vi bruker *siste*, ikke tilfeldig, fordi vi vil teste om modellen kan forutsi\n"
                "hva som skjer *neste* — akkurat som i et ekte produkt.\n\n"
                "### Metrikker\n\n"
                "- **Recall@K**: var den gjemte filmen blant topp-K? (traff vi i det hele tatt?)\n"
                "- **NDCG@K**: lå treffet høyt i listen, eller måtte brukeren scrolle?\n"
                "- **MAP@K**: belønner modeller som konsekvent plasserer treff tidlig\n\n"
                "Vi bruker K=10 — en typisk forsidelengde i en strømmetjeneste."
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
                "jonas_idx = np.where(user_ids == JONAS_ID)[0][0]\n\n"
                "overlap_lea_jonas = len(set(recs_pop[lea_idx]) & set(recs_pop[jonas_idx])) / K\n"
                "print(f'Overlapp Lea vs Jonas: {overlap_lea_jonas:.0%}')\n"
                "print('  → Begge får nesten identiske anbefalinger.\\n')\n\n"
                "for name, uid, idx in [('Lea', LEA_ID, lea_idx), ('Jonas', JONAS_ID, jonas_idx)]:\n"
                "    titles = items.set_index('item_id').loc[recs_pop[idx]]\n"
                "    print(f'Popularitetsanbefalinger til {name} (bruker {uid}):')\n"
                "    for rank, (_, row) in enumerate(titles.iterrows(), 1):\n"
                "        genres = [g for g in GENRE_COLS if row.get(g, 0) == 1]\n"
                "        print(f'  {rank:>2}. {row[\"title\"]}  [{\", \".join(genres[:3])}]')\n"
                "    print()"
            ),
            md(
                "> *Marte ser på listene:* «Vent — Lea og Jonas får *nesten det samme*?\n"
                "> Hun ser indie-drama, han ser blockbustere, men vi anbefaler identisk?\n"
                "> **Noe stemmer ikke.**»"
            ),
            code(
                "# Sjangermismatch-visualisering: hva Lea liker vs hva hun får anbefalt\n"
                "rec_items_lea = items.set_index('item_id').loc[recs_pop[lea_idx]]\n"
                "rec_genres_lea = rec_items_lea[GENRE_COLS].sum()\n\n"
                "fig, ax = plt.subplots(figsize=(10, 5))\n"
                "x = np.arange(len(GENRE_COLS))\n"
                "width = 0.35\n"
                "lea_profile = lea_items[GENRE_COLS].sum()\n"
                "lea_norm = lea_profile / lea_profile.sum()\n"
                "rec_norm = rec_genres_lea / rec_genres_lea.sum()\n"
                "ax.barh(x - width/2, lea_norm, width, label='Leas faktiske smak', color='coral')\n"
                "ax.barh(x + width/2, rec_norm, width, label='Popularitetsanbefalinger', color='gray')\n"
                "ax.set_yticks(x)\n"
                "ax.set_yticklabels(GENRE_COLS)\n"
                "ax.set_xlabel('Andel')\n"
                "ax.set_title('Sjangermismatch: hva Lea liker vs hva hun får')\n"
                "ax.legend()\n"
                "plt.tight_layout()\n"
                "plt.show()"
            ),
            md(
                "> ✅ **Sjekk gjetningene dine**\n>\n"
                "> Gå tilbake til gjetningene du skrev ned. Stemte de?\n"
                "> Hva overrasket deg med sjangergrafen?"
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
                "### Hvordan fungerer det?\n\n"
                "1. Hver film beskrives som en sjangerfordeling (en rad med tall: 1 for action, 0 for drama, osv.)\n"
                "2. Vi normaliserer radene slik at lange og korte vektorer kan sammenlignes rettferdig\n"
                "3. **Brukerprofilen** er gjennomsnittet av sjangerfordelingen til filmene brukeren har sett —\n"
                "   har Lea sett mye drama og lite action, peker profilen hennes i \u00abdrama-retningen\u00bb\n"
                "4. Vi scorer hver usett film med **cosine similarity**: hvor mye overlapper filmens\n"
                "   sjangervektor med Leas profil? Jo mer overlapp, jo høyere score\n\n"
                "Les gjennom koden under og kjør den. Se spesielt på Recall — endrer metadata noe for Lea?"
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
                "    return recommendations"
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
                "    return recommendations"
            ),
            code(
                "recs_pop = recommend_popular(train_matrix, user_ids, k=K)\n"
                "recs_cb = recommend_content_based(train_matrix, genre_matrix, user_ids, k=K)\n\n"
                "print(f'Popularitet:    Recall@{K}={recall_at_k(recs_pop, test_items, K):.4f}  NDCG@{K}={ndcg_at_k(recs_pop, test_items, K):.4f}')\n"
                "print(f'Innholdsbasert: Recall@{K}={recall_at_k(recs_cb, test_items, K):.4f}  NDCG@{K}={ndcg_at_k(recs_cb, test_items, K):.4f}')"
            ),
            code(
                "LEA_ID = 451\n"
                "JONAS_ID = 102\n"
                "lea_idx = np.where(user_ids == LEA_ID)[0]\n"
                "jonas_idx = np.where(user_ids == JONAS_ID)[0]\n\n"
                "for uid, name, idx in [(LEA_ID, 'Lea', lea_idx), (JONAS_ID, 'Jonas', jonas_idx)]:\n"
                "    if len(idx) > 0:\n"
                "        for model_name, recs in [('Popularitet', recs_pop), ('Innholdsbasert', recs_cb)]:\n"
                "            rec_items = recs[idx[0]]\n"
                "            titles = items.set_index('item_id').loc[rec_items, 'title'].values\n"
                "            print(f'\\n{name} — {model_name}:')\n"
                "            for rank, title in enumerate(titles, 1):\n"
                "                print(f'  {rank:>2}. {title}')"
            ),
            md(
                "> 💬 **Diskuter**\n>\n"
                "> 1. Hjelper metadata Lea mer enn Jonas? Hvorfor gjør den det?\n"
                "> 2. Når er innholdsbasert filtering spesielt nyttig i praksis?\n"
                "> 3. Hva er den største svakheten ved å bruke bare metadata?"
            ),
            md(
                "## 🏋️ Oppgave 1b — Eksperimenter med vekting\n\n"
                "Innholdsbasert-modellen bruker `mean` over alle filmene brukeren har sett.\n"
                "Hva skjer om vi vekter nyere filmer høyere? Fyll inn `???` under og kjør."
            ),
            code(
                "def recommend_cb_weighted(train_matrix, genre_matrix, user_ids, interactions, k=10):\n"
                "    \"\"\"Innholdsbasert med recency-vekting. Fyll inn koden som mangler.\"\"\"\n"
                "    genre_norms = np.linalg.norm(genre_matrix, axis=1, keepdims=True)\n"
                "    genre_norms = np.where(genre_norms == 0, 1.0, genre_norms)\n"
                "    item_profiles = genre_matrix / genre_norms\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n\n"
                "    for row_index, user_id in enumerate(user_ids):\n"
                "        seen = train_matrix[user_id].indices\n"
                "        if len(seen) == 0:\n"
                "            recommendations[row_index] = np.arange(k)\n"
                "            continue\n\n"
                "        # --- FYLL INN ---\n"
                "        # I stedet for ren mean, vekt de siste N filmene høyere.\n"
                "        # Hint: bruk interactions for å finne rekkefølge,\n"
                "        # og gi de siste 10 filmene dobbel vekt.\n"
                "        user_profile = item_profiles[seen].mean(axis=0)  # ← erstatt med vektet versjon\n"
                "        # ----------------\n\n"
                "        profile_norm = np.linalg.norm(user_profile)\n"
                "        if profile_norm > 0:\n"
                "            user_profile = user_profile / profile_norm\n"
                "        scores = item_profiles @ user_profile\n"
                "        scores[seen] = -np.inf\n"
                "        recommendations[row_index] = np.argsort(-scores)[:k]\n"
                "    return recommendations\n\n"
                "recs_cb_w = recommend_cb_weighted(train_matrix, genre_matrix, user_ids, interactions, k=K)\n"
                "print(f'CB vektet: Recall@{K}={recall_at_k(recs_cb_w, test_items, K):.4f}')\n"
                "print('Hint: resultatet er likt som vanlig CB akkurat nå — det er meningen.')"
            ),
            md(
                "### 💡 Fasit — Oppgave 1b\n\n"
                "> **Prøv selv først.** Rull ned kun når du har gjort et forsøk.\n\n"
                "---"
            ),
            code(
                "# FASIT — recency-vektet brukerprofil\n"
                "#\n"
                "# Idé: finn de siste 10 filmene brukeren så (sortert på timestamp)\n"
                "# og gi dem dobbel vekt i gjennomsnittet.\n\n"
                "def recommend_cb_weighted_fasit(train_matrix, genre_matrix, user_ids, interactions, k=10):\n"
                "    genre_norms = np.linalg.norm(genre_matrix, axis=1, keepdims=True)\n"
                "    genre_norms = np.where(genre_norms == 0, 1.0, genre_norms)\n"
                "    item_profiles = genre_matrix / genre_norms\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n\n"
                "    for row_index, user_id in enumerate(user_ids):\n"
                "        seen = train_matrix[user_id].indices\n"
                "        if len(seen) == 0:\n"
                "            recommendations[row_index] = np.arange(k)\n"
                "            continue\n\n"
                "        # Finn de siste 10 filmene sortert på timestamp\n"
                "        user_history = interactions[interactions.user_id == user_id].sort_values('timestamp')\n"
                "        recent_items = set(user_history['item_id'].values[-10:])\n\n"
                "        # Gi nylige filmer dobbel vekt\n"
                "        weights = np.array([2.0 if item_id in recent_items else 1.0 for item_id in seen])\n"
                "        weights = weights / weights.sum()\n\n"
                "        user_profile = (item_profiles[seen] * weights[:, None]).sum(axis=0)\n"
                "        profile_norm = np.linalg.norm(user_profile)\n"
                "        if profile_norm > 0:\n"
                "            user_profile = user_profile / profile_norm\n"
                "        scores = item_profiles @ user_profile\n"
                "        scores[seen] = -np.inf\n"
                "        recommendations[row_index] = np.argsort(-scores)[:k]\n"
                "    return recommendations\n\n"
                "recs_cb_fasit = recommend_cb_weighted_fasit(train_matrix, genre_matrix, user_ids, interactions, k=K)\n"
                "print(f'CB uvektet: Recall@{K}={recall_at_k(recs_cb, test_items, K):.4f}')\n"
                "print(f'CB vektet:  Recall@{K}={recall_at_k(recs_cb_fasit, test_items, K):.4f}')\n"
                "print('\\n→ Recency-vekting hjelper ikke alltid på Recall — smaken endrer seg sjelden drastisk.')\n"
                "print('  Men for brukere i transisjon (ny sjanger) kan det gi bedre treff.')"
            ),
            md(
                "### ✏️ Skriveøvelse\n\n"
                "Marte spør: *«Hva er egentlig forskjellen på de to modellene vi har testet?»*\n\n"
                "Skriv **to-tre setninger** til Marte som forklarer forskjellen mellom popularitet\n"
                "og innholdsbasert filtering. Regler:\n\n"
                "- Bruk gjerne ord som *profil* og *likhet*, men forklar dem som om Marte aldri har tatt et mattekurs\n"
                "- Forklar hvorfor den ene hjelper Lea mer enn den andre\n"
                "- Nevn én situasjon der den innholdsbaserte modellen er spesielt nyttig\n\n"
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
                "I notebook 01 sammenlignet vi filmer basert på sjangeretiketter. Nå snur vi\n"
                "perspektivet: i stedet for å lese filmomslaget spør vi *hvem andre så denne filmen,\n"
                "og hva så de etterpå?*\n\n"
                "Teknisk gjør vi dette ved å transponere interaksjonsmatrisen: rader blir filmer,\n"
                "kolonner blir brukere. Cosine similarity mellom to filmer måler da hvor mye\n"
                "de deler publikum — uavhengig av sjanger. To filmer kan være like fordi\n"
                "de *samme menneskene* liker dem, selv om én er en thriller og den andre er drama.\n\n"
                "### Matrix factorization\n\n"
                "I stedet for å sammenligne rå item-vektorer direkte, lærer vi latente faktorer:\n\n"
                "$$R \\approx U \\cdot V^T$$\n\n"
                "Her er $U$ brukerfaktorer og $V$ itemfaktorer. ALS er en effektiv måte å lære dette\n"
                "på for store, sparsomme implisitte datasett. Mer om dette etter Oppgave 2."
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
            md("## 🏋️ Oppgave 2 — Inspiser item-likhet\n\n"
                "La oss se hvordan co-view-basert likhet fungerer. Først noen eksempler:"),
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
                "### 🏋️ Oppgave 2b — Velg din egen film\n\n"
                "Finn en film du kjenner i katalogen og se hvem naboene er.\n"
                "Gir resultatet mening? Hva fanger likheten som sjanger alene ikke ser?"
            ),
            code(
                "# Fyll inn en tittel du kjenner (eller del av tittelen)\n"
                "SEARCH_TITLE = 'Matrix'  # <-- endre dette\n\n"
                "matches = items[items['title'].str.contains(SEARCH_TITLE, case=False, na=False)]\n"
                "if len(matches) == 0:\n"
                "    print(f'Fant ingen filmer med \"{SEARCH_TITLE}\" i tittelen.')\n"
                "else:\n"
                "    chosen = matches.iloc[0]\n"
                "    chosen_id = chosen['item_id']\n"
                "    neighbors = np.argsort(-item_sim[chosen_id])[:5]\n"
                "    print(f'Naboer til \"{chosen[\"title\"]}\":')\n"
                "    for neighbor_id in neighbors:\n"
                "        nb_row = items[items.item_id == neighbor_id]\n"
                "        if len(nb_row) > 0:\n"
                "            print(f'  {item_sim[chosen_id, neighbor_id]:.3f}  {nb_row.iloc[0][\"title\"]}')"
            ),
            md(
                "> 💬 **Diskuter**\n>\n"
                "> 1. Ser naboskapet meningsfullt ut?\n"
                "> 2. Hva fanger item-item-likheten som metadata alene ikke så godt viser?\n"
                "> 3. Hvorfor er dette fortsatt begrenset?"
            ),
            md(
                "## 🏋️ Oppgave 3 — Head-to-head: item-item vs ALS\n\n"
                "### Hva er ALS, og hvorfor fungerer det?\n\n"
                "Tenk deg at hver bruker har en skjult smaksprofil med ~64 dimensjoner —\n"
                "kanskje «liker spenning», «foretrekker visuelt vakre filmer», «liker komplekse plott».\n"
                "Hver film har en tilsvarende profil. **ALS prøver å gjette disse profilene**\n"
                "slik at brukerprofil · filmprofil ≈ hvor mye brukeren likte filmen.\n\n"
                "Vi kaller dem *latente* faktorer fordi vi ikke velger dem — de læres\n"
                "automatisk fra data. De trenger ikke tilsvare sjangre; de kan fange\n"
                "subtile mønstre som «stemning» eller «regi-stil».\n\n"
                "**ALS (Alternating Least Squares)** veksler mellom å oppdatere brukerprofiler\n"
                "og filmprofiler — litt som å løse et puslespill fra to sider samtidig.\n"
                "Det gjør den i 15 runder, og når det er ferdig har vi en komprimert\n"
                "representasjon som fanger sammenhenger item-item ikke ser.\n\n"
                "La oss se om det gjør en forskjell. Se spesielt på Recall og NDCG —\n"
                "tar ALS et tydelig sprang?"
            ),
            code(
                "def recommend_item_item(item_sim, train_matrix, user_ids, k=10):\n"
                "    # Compute all user scores in one vectorized BLAS call:\n"
                "    # sparse (n_users × n_items) @ dense (n_items × n_items) → (n_users × n_items)\n"
                "    all_scores = train_matrix[user_ids].dot(item_sim)  # shape: (n_users, n_items)\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n"
                "    for row_index, user_id in enumerate(user_ids):\n"
                "        scores = all_scores[row_index].A1 if hasattr(all_scores[row_index], 'A1') else all_scores[row_index]\n"
                "        scores[train_matrix[user_id].indices] = -np.inf\n"
                "        recommendations[row_index] = np.argsort(-scores)[:k]\n"
                "    return recommendations\n\n"
                "recs_item_item = recommend_item_item(item_sim, train_matrix, user_ids, k=K)"
            ),
            code(
                "als = AlternatingLeastSquares(factors=64, regularization=0.01, iterations=15, random_state=42, use_gpu=False)\n"
                "als.fit(train_matrix, show_progress=True)\n"
                "recs_als = als.recommend(user_ids, train_matrix[user_ids], N=K, filter_already_liked_items=True)[0]"
            ),
            code(
                "for name, recs in [('Item-item', recs_item_item), ('ALS', recs_als)]:\n"
                "    recall_value = recall_at_k(recs, test_items, K)\n"
                "    ndcg_value = ndcg_at_k(recs, test_items, K)\n"
                "    map_value = map_at_k(recs, test_items, K)\n"
                "    print(f'{name:<10} Recall@{K}={recall_value:.4f}  NDCG@{K}={ndcg_value:.4f}  MAP@{K}={map_value:.4f}')"
            ),
            code(
                "LEA_ID = 451\n"
                "JONAS_ID = 102\n"
                "lea_idx = np.where(user_ids == LEA_ID)[0]\n"
                "jonas_idx = np.where(user_ids == JONAS_ID)[0]\n\n"
                "for uid, name, idx in [(LEA_ID, 'Lea', lea_idx), (JONAS_ID, 'Jonas', jonas_idx)]:\n"
                "    if len(idx) > 0:\n"
                "        for model_name, recs in [('Item-item', recs_item_item), ('ALS', recs_als)]:\n"
                "            rec_items = recs[idx[0]]\n"
                "            titles = items.set_index('item_id').loc[rec_items, 'title'].values\n"
                "            print(f'\\n{name} — {model_name}:')\n"
                "            for rank, title in enumerate(titles, 1):\n"
                "                print(f'  {rank:>2}. {title}')"
            ),
            md(
                "> *Marte ser på tallene:* «Recall gikk opp — men ser Lea **faktisk** bedre filmer?\n"
                "> Og hva med Jonas — forandret det noe for ham?»\n\n"
                "ALS tar et tydelig sprang. Se på listene — ser du forskjellen?\n\n"
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
                "> Og hva skjer når vi må blande signaler og ta fairness på alvor?\n"
                "> Amira spør allerede.»\n\n"
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
                "from src.metrics import recall_at_k, coverage, novelty, intra_list_similarity\n"
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
            md(
                "## 🏋️ Oppgave 4 — Korttidskontekst som hybridsignal\n\n"
                "### Hva er en sesjon?\n\n"
                "En sesjon er en sammenhengende rekke handlinger — for eksempel filmene Lea ser\n"
                "i løpet av en kveld. Rekkefølgen betyr noe: hvis hun ser en thriller og deretter\n"
                "en annen thriller, sier det noe om hva hun er i humør for *akkurat nå*.\n\n"
                "### Hvorfor trenger vi sesjonskontekst?\n\n"
                "ALS kjenner Leas langtidsprofil — hvem hun er generelt. Men den vet ikke\n"
                "at hun akkurat nå sitter i sofaen og vil ha spenning, ikke drama.\n"
                "Sesjonskontekst fanger opp dette korttidshumøret.\n\n"
                "### Hvordan fungerer det?\n\n"
                "Vi teller: etter film A, hva ser folk typisk etterpå? Det gir oss en\n"
                "**overgangsmatrise** — en slags «hva kommer neste»-tabell. Kombinert\n"
                "med ALS-profilen gir den oss det beste fra to verdener."
            ),
            code(
                "sess_sizes = sessions.groupby('session_id').size()\n"
                "print(f'Antall sesjoner: {len(sess_sizes):,}')\n"
                "print(f'Sesjonslengde — min: {sess_sizes.min()}, median: {sess_sizes.median():.0f}, maks: {sess_sizes.max()}')\n\n"
                "lea_sessions = sessions[sessions.user_id == LEA_ID]\n"
                "lea_session_ids = lea_sessions.session_id.unique()\n"
                "print(f'Lea har {len(lea_session_ids)} sesjoner')"
            ),
            md(
                "### Bygg overgangsmatrise fra sesjoner\n\n"
                "Vi teller hvor ofte item A etterfølges av item B i samme sesjon,\n"
                "og normaliserer til sannsynligheter."
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
                "transition = diags(1.0 / row_sums) @ transition\n"
                "print(f'Overgangsmatrise: {transition.shape}, nnz={transition.nnz:,}')"
            ),
            md(
                "### Blend ALS-profil med sesjonskontekst\n\n"
                "Vi blander to signaler: ALS sin langtidsprofil (hvem er Lea generelt?)\n"
                "med sesjonens korttidssignal (hva ser hun akkurat nå?).\n\n"
                "`lambda_` styrer blandingen: 1.0 = bare ALS, 0.0 = bare sesjon.\n"
                "Ingen av delene alene er nok — bare ALS ignorerer øyeblikket,\n"
                "bare sesjon glemmer hvem brukeren er."
            ),
            code(
                "def recommend_session_blend(als_model, transition, test_sessions,\n"
                "                           train_matrix, k=10, lambda_=0.7):\n"
                "    dense_transition = transition.toarray()\n"
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
                "    return np.array(recommendations), np.array(ground_truth)"
            ),
            code(
                "for lambda_value in [0.0, 0.7, 1.0]:\n"
                "    recs, targets = recommend_session_blend(als, transition, test_sessions,\n"
                "                                           train_matrix, k=K, lambda_=lambda_value)\n"
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
                "Til nå har vi målt Recall som et gjennomsnitt over alle brukere. Men et gjennomsnitt\n"
                "kan skjule at modellen fungerer bra for mainstream-brukere og dårlig for nisjeprofiler.\n"
                "Fairness handler om å måle *hvem* som tjener — og hvem som taper.\n\n"
                "> *Amira (CTO):* «Høy gjennomsnittlig Recall er fint for en rapport.\n"
                "> Men fortell meg dette: fungerer systemet like godt for brukerne\n"
                "> som ser obskure dokumentarer som for dem som ser alt på forsiden?»\n\n"
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
            md(
                "### MMR — Maximal Marginal Relevance\n\n"
                "MMR er en re-rankeringsalgoritme som balanserer **relevans** mot **mangfold**.\n\n"
                "Tenk på det som å lage en spilleliste: du vil ikke ha 10 like sanger på rad,\n"
                "selv om de alle scorer høyt. MMR velger den neste filmen som er både relevant\n"
                "*og* forskjellig fra det du allerede har valgt.\n\n"
                "**Prosessen steg for steg:**\n\n"
                "1. Start med en tom liste og et sett kandidater (f.eks. topp 100 fra ALS)\n"
                "2. For hver gjenværende kandidat, beregn: λ · relevans − (1−λ) · likhet med det du allerede valgte\n"
                "3. Velg kandidaten med høyest score, legg den til listen\n"
                "4. Gjenta til listen har K filmer\n\n"
                "`lambda_` styrer tradeoffet: λ = 1.0 betyr «bare relevans» (ingen diversitet),\n"
                "λ = 0.3 betyr «prioriter mangfold tungt». Vi tester flere verdier:"
            ),
            code(
                "def apply_mmr(als_model, user_ids, train_matrix, genre_matrix, k=10, lambda_=0.5, n_cand=100):\n"
                "    candidate_ids, candidate_scores = als_model.recommend(user_ids, train_matrix[user_ids], N=n_cand, filter_already_liked_items=True)\n"
                "    recommendations = np.zeros((len(user_ids), k), dtype=np.int32)\n"
                "    for row_index in range(len(user_ids)):\n"
                "        recommendations[row_index] = mmr_rerank(candidate_ids[row_index], candidate_scores[row_index], genre_matrix, k=k, lambda_=lambda_)\n"
                "    return recommendations\n\n"
                "# Vis tradeoff-gradienten: lambda_ styrer balansen relevans ↔ diversitet\n"
                "print(f\"{'Modell':<16} {'Recall@10':>10} {'ILS (↓=bedre)':>14}\")\n"
                "print('-' * 44)\n"
                "for lam in [1.0, 0.7, 0.5, 0.3]:\n"
                "    if lam == 1.0:\n"
                "        recs = recs_als\n"
                "        label = 'ALS (ingen MMR)'\n"
                "    else:\n"
                "        recs = apply_mmr(als, user_ids, train_matrix, genre_matrix, k=K, lambda_=lam)\n"
                "        label = f'ALS+MMR \u03bb={lam}'\n"
                "    r = recall_at_k(recs, test_items, K)\n"
                "    ils = intra_list_similarity(recs, genre_matrix, K)\n"
                "    print(f'{label:<16} {r:>10.4f} {ils:>14.4f}')\n\n"
                "recs_mmr = apply_mmr(als, user_ids, train_matrix, genre_matrix, k=K, lambda_=0.5)"
            ),
            md(
                "**ILS** (intra-list similarity) måler gjennomsnittlig genre-likhet *innenfor* en brukers topp-10.\n"
                "Lavere ILS = listene inneholder mer sjangermessig variasjon.\n\n"
                "`coverage` og `novelty` er katalog-aggregater på tvers av alle brukere — de fanger ikke\n"
                "within-user diversitet. ILS er det riktige målet her, og det beveger seg tydelig med \u03bb.\n\n"
                "Re-ranking for mangfold er en **eksplisitt tradeoff**: litt lavere Recall mot\n"
                "lister brukeren faktisk opplever som bredere. `lambda_` er parameteren du skrur på.\n\n"
                "> 💬 **Diskuter**\n>\n"
                "> 1. Hvem taper på en ren ALS-modell?\n"
                "> 2. Hvilken `lambda_`-verdi ville du valgt for StreamNord? Hvorfor?\n"
                "> 3. Hva ville du fortalt Amira om tradeoffet?"
            ),
            md(
                "## 🔍 Når modeller feiler\n\n"
                "Til nå har hver modell vært strengt bedre enn den forrige.\n"
                "Men det er ikke hele sannheten. La oss se nærmere."
            ),
            code(
                "# Finnes det brukere der ALS gjør det VERRE enn popularitet?\n"
                "from src.recommenders.popularity import PopularityRecommender\n\n"
                "pop_rec = PopularityRecommender().fit(train_matrix)\n"
                "recs_pop = pop_rec.recommend(user_ids, train_matrix, K)\n\n"
                "pop_hits = np.array([1 if test_items[i] in recs_pop[i] else 0 for i in range(len(user_ids))])\n"
                "als_hits = np.array([1 if test_items[i] in recs_als[i] else 0 for i in range(len(user_ids))])\n\n"
                "pop_wins = np.sum((pop_hits == 1) & (als_hits == 0))\n"
                "als_wins = np.sum((als_hits == 1) & (pop_hits == 0))\n"
                "print(f'Brukere der popularitet finner riktig, men ALS bommer: {pop_wins}')\n"
                "print(f'Brukere der ALS finner riktig, men popularitet bommer: {als_wins}')\n"
                "print(f'\\n→ ALS er bedre i gjennomsnitt, men popularitet vinner for {pop_wins} brukere.')"
            ),
            md(
                "> *Amira:* «Så ingen modell er universelt best.\n"
                "> Det er derfor vi trenger hybrider — og det er derfor vi måler på grupper, ikke bare gjennomsnitt.»\n\n"
                "### Lærdom\n\n"
                "- En modell med høyere gjennomsnittlig Recall kan likevel **tape** for spesifikke brukersegmenter\n"
                "- Popularitet vinner ofte for brukere med mainstream-smak og lite historikk\n"
                "- ALS kan overfit til majoritetsmønstre og bomme på nisjeprofiler\n"
                "- **Tradeoffs er uunngåelige** — spørsmålet er hvem du prioriterer"
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
            # --- INTRO ---
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
                "from src.metrics import recall_at_k, ndcg_at_k, map_at_k, coverage, novelty, intra_list_similarity\n"
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
            # --- PART 1: EVIDENCE ---
            md(
                "## 🏋️ Oppgave 6 — Leaderboard for modellfamiliene\n\n"
                "Alle modellene side om side. Se ikke bare på Recall —\n"
                "sjekk coverage, novelty og ILS. Hva forteller de?"
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
                "        f'ILS@{K}': intra_list_similarity(recs, genre_matrix, K),\n"
                "    }\n\n"
                "leaderboard = pd.DataFrame(results).T.sort_values(f'ndcg@{K}', ascending=False)\n"
                "print(leaderboard.to_string(float_format=lambda value: f'{value:.4f}'))"
            ),
            md(
                "## 🏋️ Oppgave 7 — Cold start\n\n"
                "Leaderboardet viser hvem som vinner med nok data.\n"
                "Men hva skjer når en ny bruker dukker opp — og ALS har *ingenting* å jobbe med?"
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
                "print(cold_start_df.to_string(index=False))"
            ),
            code(
                "# Popularitetsbaseline for sammenligning\n"
                "pop_recall = recall_at_k(pop.recommend(user_ids, train_matrix, K), test_items, K)\n\n"
                "fig, ax = plt.subplots(figsize=(8, 5))\n"
                "ax.plot(cold_start_df['history_size'], cold_start_df[f'recall@{K}'], 'o-', linewidth=2, label='ALS')\n"
                "ax.axhline(y=pop_recall, color='gray', linestyle='--', label=f'Popularitet ({pop_recall:.4f})')\n"
                "ax.set_xlabel('Antall interaksjoner i historikk')\n"
                "ax.set_ylabel(f'Recall@{K}')\n"
                "ax.set_title('Cold-start: når blir ALS bedre enn popularitet?')\n"
                "ax.legend()\n"
                "plt.tight_layout()\n"
                "plt.show()\n"
                "print('→ Under stiplet linje er popularitet faktisk bedre enn ALS.')"
            ),
            # --- PART 2: REFLECTION ---
            md("## 🎬 Lea og Jonas gjennom workshopen\n\n"
                "Før vi tar en beslutning — la oss se reisen. Hvordan har anbefalingene\n"
                "til Lea og Jonas endret seg fra modell til modell?"
            ),
            code(
                "LEA_ID = 451\n"
                "JONAS_ID = 102\n"
                "lea_idx = np.where(user_ids == LEA_ID)[0]\n"
                "jonas_idx = np.where(user_ids == JONAS_ID)[0]\n\n"
                "for uid, name, idx in [(LEA_ID, 'Lea', lea_idx), (JONAS_ID, 'Jonas', jonas_idx)]:\n"
                "    if len(idx) > 0:\n"
                "        print(f'\\n{name}s anbefalinger gjennom workshopen:')\n"
                "        print('=' * 50)\n"
                "        for model_name in ['Popularitet', 'Innholdsbasert', 'ALS', 'ALS+MMR']:\n"
                "            rec_items = models[model_name][idx[0]]\n"
                "            titles = items.set_index('item_id').loc[rec_items[:5], 'title'].values\n"
                "            print(f'\\n  {model_name}:')\n"
                "            for rank, title in enumerate(titles, 1):\n"
                "                print(f'    {rank}. {title}')\n"
                "print('\\n→ Lea gikk fra mainstream-spam til personlig. Jonas fikk bedre, men mindre dramatisk.')"
            ),
            md(
                "### 🔄 Sjekk gjetningene fra starten\n\n"
                "Gå tilbake til notebook 00 og les gjetningene du skrev ned.\n"
                "Fyll inn tabellen under:\n\n"
                "| # | Din gjetning | Hva som skjedde | Overrasket? |\n"
                "|---|---|---|---|\n"
                "| 1 | Hva Lea ville like: | | |\n"
                "| 2 | Hva popularitetslisten inneholdt: | | |\n"
                "| 3 | Popularitet for Lea vs Jonas: | | |\n"
                "| 4 | Sikkerhet (1–5) — hadde du rett? | | |"
            ),
            # --- PART 3: FRAMEWORK ---
            md(
                "## Produksjonsarkitektur\n\n"
                "Hvorfor ikke bare én modell? Fordi hvert steg har en jobb:\n\n"
                "```\n"
                "Kandidatgenerering  ->  Rangering  ->  Re-rangering\n"
                "  (enkle signaler)      (sterk modell)     (fairness/regler)\n"
                "```\n\n"
                "- **Kandidatgenerering** siler ned fra 10 000 filmer til ~100 med raske, grove modeller (f.eks. popularitet eller enkel CF)\n"
                "- **Rangering** scorer de ~100 nøyaktig med en tyngre modell (f.eks. ALS)\n"
                "- **Re-rangering** justerer for mangfold, fairness og forretningsregler (f.eks. MMR)\n\n"
                "Denne arkitekturen finnes i nesten alle store anbefalingssystemer — fra Netflix til Spotify.\n"
                "Poenget er at ingen enkeltmodell kan gjøre alt: noen er raske men unøyaktige,\n"
                "andre er nøyaktige men for trege til å kjøre på hele katalogen.\n\n"
                "### En realistisk anbefaling\n\n"
                "- bruk **ALS** eller en tilsvarende sterk collaborative modell som hovedmotor\n"
                "- bruk **innholdsbaserte signaler** for cold start og forklarbarhet\n"
                "- bruk **reranking** for mangfold, fairness og produktkrav\n"
                "- legg til **kontekst** når det gir tydelig verdi"
            ),
            # --- PART 4: DECISION ---
            md(
                "## 📋 Beslutningsmal\n\n"
                "Nå har du sett bevisene (leaderboard + cold start), reisen (Lea og Jonas),\n"
                "og rammeverket (produksjonsarkitektur). Fyll inn malen nedenfor.\n"
                "Ta den med deg etter workshopen — den er gjenbrukbar.\n\n"
                "**Eksempel** (seksjon 1): *«Hovedsakelig implisitt: vi har klikk og\n"
                "avspillinger, men ingen ratings eller likes.»*"
            ),
            code(
                "# BESLUTNINGSMAL — Anbefalingssystem\n"
                "#\n"
                "# 1. SIGNALTYPE\n"
                "#    Hovedsakelig eksplisitt / implisitt / begge: \n"
                "#    Hva betyr det for modellvalget?\n"
                "#\n"
                "# 2. ANBEFALT MODELLFAMILIE\n"
                "#    Kjernemodell: \n"
                "#    Hvorfor denne (maks 2 setninger): \n"
                "#\n"
                "# 3. COLD-START-STRATEGI\n"
                "#    For nye brukere (< 5 interaksjoner): \n"
                "#    For nye items (0 interaksjoner): \n"
                "#    Hint: se cold-start-kurven over\n"
                "#\n"
                "# 4. FAIRNESS OG MANGFOLD\n"
                "#    Hvem risikerer å få dårlige anbefalinger? \n"
                "#    Hva gjør vi med det? \n"
                "#\n"
                "# 5. PRODUKSJONSARKITEKTUR\n"
                "#    Kandidatgenerering (rask, grovfiltrering): \n"
                "#    Rangering (sterk modell): \n"
                "#    Re-rangering (produktregler): \n"
                "#\n"
                "# 6. KJENTE RISIKOER\n"
                "#    Hva kan gå galt i produksjon? \n"
                "#    Hva mangler vi data for? \n"
            ),
            md(
                "## 🏋️ Oppgave 8 — Hva anbefaler du å shippe?\n\n"
                "Bruk malen du nettopp fylte ut. Skriv en kort anbefaling til Marte — ikke tenk bare\n"
                "på hva som vinner én metrikk, men på hvilket system som faktisk er mest realistisk."
            ),
            md(
                "> **Skriv din anbefaling her**\n>\n"
                "> *«Marte, basert på analysen anbefaler jeg ... fordi ...»*"
            ),
            # --- PART 5: COMMUNICATION ---
            md(
                "### ✏️ Skriveøvelse — Forklar uten fagspråk\n\n"
                "Amira ber deg forklare anbefalingen i et avsnitt til styret.\n\n"
                "**Teknisk versjon** (IKKE send denne):\n"
                "> *«Vi anbefaler ALS med 64 latente faktorer som oppnår Recall@10=0.12\n"
                "> og NDCG@10=0.08. Re-ranking med MMR (λ=0.6) øker coverage fra 14% til 38%\n"
                "> med akseptabelt Recall-tap på 0.01.»*\n\n"
                "**Din oppgave:** Skriv dette om til **3–4 setninger** uten å bruke:\n"
                "*faktorer, matrise, vektor, recall, coverage, lambda, re-ranking*\n\n"
                "> *«Til styret: Vi anbefaler ... fordi ...»*"
            ),
            # --- PART 6: SUMMARY ---
            md(
                "## 🔑 Oppsummering\n\n"
                "| # | Lærdom |\n"
                "|---|--------|\n"
                "| 1 | **Signalet betyr noe** — implisitt data må tolkes annerledes enn eksplisitt feedback |\n"
                "| 2 | **Baselines er viktige** — popularitet er enkel, sterk og utilstrekkelig |\n"
                "| 3 | **Metadata hjelper tidlig** — content-based filtering er nyttig, men begrenset |\n"
                "| 4 | **Collaborative filtering skaper et hopp** — ALS lærer struktur metadata ikke ser |\n"
                "| 5 | **Hybrider vinner i praksis** — produktkrav tvinger frem flere signaler |\n"
                "| 6 | **Fairness må måles** — høy gjennomsnittlig relevans er ikke nok |\n"
                "| 7 | **Ingen modell er best for alle** — tradeoffs er uunngåelige, og kommunikasjon er en del av jobben |\n\n"
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