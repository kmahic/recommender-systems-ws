# StreamNord — Anbefalingssystemer Workshop

En narrativ workshop på rundt 4 timer der deltakerne bruker **StreamNord-caset**
til å forstå de viktigste modellfamiliene i anbefalingssystemer

Workshopen følger to spor samtidig:

- et **narrativt spor**: Lea mister tillit til produktet, Marte trenger en plan, og Amira presser på fairness
- et **konseptuelt spor**: eksplisitt vs implisitt feedback, evaluering, content-based filtering, collaborative filtering, matrix factorization og hybridsystemer

## Hurtigstart

```bash
# Forutsetninger: Python 3.10+, uv
make all        # installer avhengigheter, last ned data, generer notebooks/slides
make lab        # start JupyterLab
```

Kjør `make help` for å se alle tilgjengelige mål.

## Konsolidert Workshopløp

| Notebook | Rolle | Tid (ca.) |
|----------|-------|-----------|
| `00_velkommen.ipynb` | Case, signalforståelse, metrikker og popularitetsbaseline | 60 min |
| `01_content_based.ipynb` | Innholdsbasert filtering som første personaliserte modell | 30 min |
| `02_collaborative_filtering.ipynb` | Item-item CF og matrix factorization med ALS | 45 min |
| `03_hybrid_systems.ipynb` | Hybrider, kontekst, fairness og reranking | 60 min |
| `04_ship_decision.ipynb` | Leaderboard, cold start og sluttanbefaling | 30 min |

Den tunge delen av materialet er ikke fjernet. Den er flyttet inn som **valgfri appendix**
inne i de relevante notebookene i stedet for å ligge som egne hovedmoduler.

## Notebookoversikt

| Notebook | Kjerneinnhold | Valgfri appendix |
|----------|---------------|------------------|
| `00_velkommen.ipynb` | Lea, data, eksplisitt vs implisitt feedback, metrikker, popularitet | Tilfeldig baseline |
| `01_content_based.ipynb` | Content-based filtering | Embeddings og ANN |
| `02_collaborative_filtering.ipynb` | Item-item CF, ALS | Faktorsveip og embedding-tolkning |
| `03_hybrid_systems.ipynb` | Sesjonssignal, fairness, MMR | Kalibrering |
| `04_ship_decision.ipynb` | Produksjonsvalg, cold start, hybrid anbefaling | — |

## Teori Dekket

- eksplisitt vs implisitt feedback
- vurderingsprediksjon vs topp-N-rangering
- innholdsbasert filtering
- collaborative filtering fra item-item til matrix factorization
- ALS for implisitt feedback
- hybridsystemer og blending
- fairness, popularitetsbias og reranking
- cold start og produksjonsarkitektur
- embeddings og ANN-søk som appendixstoff

## Deltageraktiviteter

Den konsoliderte workshopen er bygget rundt noen få tydelige aktiviteter i stedet for
mange små notebookskifter:

- etablere baseline og vise hvorfor popularitet feiler for Lea
- bygge den første personaliserte modellen med content-based filtering
- sammenligne item-item CF mot ALS som eksempel på matrix factorization
- vise hvorfor ekte systemer blir hybride når kontekst, fairness og reranking kommer inn
- ende i en eksplisitt produksjonsanbefaling til Marte

## Repostruktur

```text
README.md
Makefile
pyproject.toml
data/
  sample_ml25m.py        # laster ned ML-25M, sampler subset, lagrer parquet
  ml-25m-sample/         # (generert) parquet-filer
notebooks/
  00_velkommen.ipynb
  01_content_based.ipynb
  02_collaborative_filtering.ipynb
  03_hybrid_systems.ipynb
  04_ship_decision.ipynb
src/
  data.py
  split.py
  metrics.py
  eval.py
  rerank.py
  fairness.py
  recommenders/
    popularity.py
    item_item.py
    als.py
    content_based.py
    embedding_retrieval.py
    session.py
outputs/
```

## Forutsetninger

| Verktøy | Installasjon |
|---------|--------------|
| Python >= 3.10 | [python.org](https://www.python.org/) |
| uv | `curl -LsSf https://astral.sh/uv/install.sh | sh` |
| Node.js *(valgfritt, for slides)* | [nodejs.org](https://nodejs.org/) |

## Datasett-referanse

> F. Maxwell Harper and Joseph A. Konstan. 2015. *The MovieLens Datasets:
> History and Context.* ACM Transactions on Interactive Intelligent
> Systems (TiiS) 5, 4, Article 19.
> DOI: <http://dx.doi.org/10.1145/2827872>

MovieLens 100k leveres av [GroupLens Research](https://grouplens.org/)
ved University of Minnesota.
