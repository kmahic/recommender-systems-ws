---
marp: true
theme: default
paginate: true
header: "Anbefalingssystemer i praksis"
footer: "StreamNord workshop"
style: |
  section {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  }
  h1 { color: #1a1a2e; }
  h2 { color: #16213e; }
  blockquote { border-left: 4px solid #e94560; padding-left: 1em; }
---

# StreamNord

### En introduksjon til anbefalingssystemer

På én workshop skal dere både forstå de viktigste modellfamiliene og anbefale hva StreamNord faktisk bør sette i produksjon.

---

## Caset

- **Lea** er en av de mest aktive brukerne våre.
- Hun elsker nordisk indie-drama, thriller og mørkere katalogtitler.
- I dag får hun stort sett de samme blockbusterne som alle andre.
- **Marte** vil ha en anbefaling klar til produktmøtet i morgen.
- **Amira** spør om systemet systematisk favoriserer mainstream-smak.

> Dette er ikke bare en modelløvelse. Det er en produktbeslutning.

---

## To Spor Gjennom Workshopen

| Case | Konsepter |
|---|---|
| Hvorfor mister vi Lea? | Hvilke signaler finnes i anbefalingssystemer? |
| Hvorfor popularitet ikke nok? | Hvordan evaluerer vi topp-N-anbefalinger? |
| Hva kan vi gjøre bedre? | Hva er content-based, collaborative og matrix factorization? |
| Hva bør vi shippe? | Hvorfor ender ekte systemer som hybrider? |


---

## Læringsmål

Etter workshopen skal deltakerne kunne forklare:

- forskjellen på **eksplisitt** og **implisitt** feedback
- hvorfor **rangering** ofte er viktigere enn rating-prediksjon
- når **content-based filtering** fungerer godt
- hva **collaborative filtering** fanger som innhold alene ikke ser
- hvorfor **matrix factorization** ble den klassiske arbeidshesten
- hvorfor modne produkter ofte lander på **hybride systemer**

---

## Workshop Arc

| Tid | Del | Hovedspørsmål |
|---|---|---|
| 0:00-0:45 | Signal og evaluering | Hva vet vi egentlig om brukerne? |
| 0:45-1:10 | Popularitet | Hvorfor er baseline både sterk og utilstrekkelig? |
| 1:10-1:40 | Innholdsbasert | Kan vi personalisere fra features alene? |
| 1:40-2:20 | CF + ALS | Hva lærer vi når brukere hjelper hverandre? |
| 2:30-3:00 | Hybrid og cold start | Hvorfor vinner kombinasjoner i praksis? |
| 3:00-3:25 | Fairness og reranking | Er anbefalingene gode for flere enn mainstream? |
| 3:25-3:50 | Sluttanbefaling | Hva bør StreamNord faktisk shippe? |

---

## Notebooksett

| Notebook | Kjerne | Appendix |
|---|---|---|
| `00_velkommen` | Case, signal, metrikker, baseline | Tilfeldig baseline |
| `01_content_based` | Første personaliserte modell | Embeddings og ANN |
| `02_collaborative_filtering` | Item-item og ALS | Faktorsveip og tolkning |
| `03_hybrid_systems` | Kontekst, fairness, reranking | Kalibrering |
| `04_ship_decision` | Produksjonsvalg og cold start | — |

Det tyngste stoffet er flyttet til appendix i stedet for å være egne hovednotebooks.

---

## Hvilket signal har vi?

| Type | Eksempler | Fordel | Problem |
|---|---|---|---|
| **Eksplisitt feedback** | Ratings, likes, tommel opp | Tydelig preferanse | Sjeldent i virkelige produkter |
| **Implisitt feedback** | Klikk, visning, avspilling, kjøp | Finnes i store mengder | Manglende data er tvetydig |

For StreamNord er hovedsignalet **implisitt**: vi ser at Lea så noe, men ikke sikkert hvorfor.

> Manglende interaksjon betyr ikke nødvendigvis avvisning.

---

## Rangering slår ofte rating-prediksjon

| Spørsmål | Klassisk svar | Praktisk produktspørsmål |
|---|---|---|
| «Blir denne filmen 4.2 eller 4.5?» | Rating-prediksjon | Ofte mindre viktig |
| «Er riktig film i topp 10?» | Rangering | Ofte det produktet faktisk trenger |

Derfor bruker vi metrikker som:

- **Recall@K** — fant vi relevant innhold i topp-K?
- **NDCG@K** — lå det høyt nok i listen?
- **MAP@K** — hvor tidlig dukket treffene opp?

---

## Popularitet: Sterk Baseline, svak Personalisering

Hvorfor popularitet alltid må med:

- den er enkel å forklare og billig å kjøre
- den er ofte vanskeligere å slå enn folk tror
- den avslører raskt om en «smart» modell faktisk hjelper

Hvorfor den ikke løser Leas problem:

- alle ser omtrent den samme listen
- nisje-smak drukner i mainstream-signaler
- høy gjennomsnittsscore kan skjule dårlige brukeropplevelser

---

## Modellfamilie 1: Innholdsbasert Filtering

Idé:

- bygg en brukerprofil fra item-features, som sjangre eller metadata
- anbefal nytt innhold som ligner på det brukeren allerede liker

Styrker:

- fungerer godt for **nye items**
- lett å forklare og inspisere

Svakheter:

- begrenset av kvaliteten på features
- kan bli smalt og forutsigbart

For Lea er dette det første naturlige steget bort fra global popularitet.

---

## Modellfamilie 2: Collaborative Filtering

Idé:

- bruk mønstre i **andre brukeres atferd** til å anbefale for deg
- «brukere som liker det Lea liker, liker også dette»

To nyttige innganger:

- **item-item** som intuitiv start
- **user/item mønstre** som går utover eksplisitte features

Dette er ofte punktet der systemet begynner å oppdage smak som metadata alene ikke fanger.

---

## Modellfamilie 3: Matrix Factorization

Kjerneidé:

- dekomponer bruker-item-matrisen i latente faktorer
- lær skjulte smaksmønstre i stedet for å kode dem manuelt

Hvorfor dette ble den klassiske arbeidshesten:

- bedre generalisering enn rene nabolagsmetoder
- fanger struktur som ikke står eksplisitt i sjangerdata
- fungerer godt med store, sparsomme implisitte datasett

I workshopen bruker vi **ALS** som den klareste introduksjonen til denne familien.

---

## Hvorfor Ekte Systemer Ender Som Hybrider

Ingen enkeltmodell løser hele produktproblemet:

- **Popularitet** er robust, men upersonlig
- **Innholdsbasert** hjelper med cold start og forklarbarhet
- **Collaborative / ALS** gir sterk personalisering
- **Regler og reranking** håndterer fairness, mangfold og policy

Det realistiske sluttpunktet er derfor ofte et **hybridsystem**.

---

## De Virkelige Begrensningene

- **Cold start** — hva gjør vi når brukeren eller itemet er nytt?
- **Popularitetsbias** — blir alt dratt mot de samme hittene?
- **Latens** — kan modellen svare raskt nok i produktet?
- **Feedback-løkker** — trener vi bare på konsekvensene av egne anbefalinger?
- **Fairness og mangfold** — hvem taper når vi maksimerer gjennomsnittlig relevans?

Dette er der Amira kommer inn i historien.

---

## Sluttleveransen

Ved slutten av workshopen skal deltakerne kunne si:

- hva slags signal StreamNord har
- hvilken modellfamilie som løser hva
- hvorfor Lea fortsatt er en nyttig stresstest
- hvorfor den endelige anbefalingen sannsynligvis er **hybrid**

> Åpne `notebooks/00_velkommen.ipynb` — vi begynner med Lea, dataene og signalet vi faktisk har.
