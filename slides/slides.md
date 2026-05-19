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
  section.lead {
    background: linear-gradient(135deg, #f5f7fa 0%, #e8edf5 100%);
  }
  h1 { color: #1a1a2e; }
  h2 { color: #16213e; }
  blockquote { border-left: 4px solid #e94560; padding-left: 1em; }
---

<!-- _class: lead -->

# StreamNord

### En introduksjon til anbefalingssystemer

På én workshop skal dere både forstå de viktigste modellfamiliene og anbefale hva StreamNord faktisk bør sette i produksjon.

<!--
SPEAKER NOTES:
Åpne med produktspenning, ikke modellteori: "I morgen skal dere anbefale hva som faktisk går i produksjon."
Spørsmål til rommet: "Hva er verst for et streamingprodukt: feil film i topp 1, eller 10 like filmer i topp 10?"
Mål: Deltakerne skal forstå at dette er en beslutnings-workshop, ikke en ren algoritmegjennomgang.
-->

---

<!-- _class: lead -->

# Del 1
## Case, mål og beslutningsramme

---

## Caset

- **Lea** er en av de mest aktive brukerne våre.
- Hun elsker nordisk indie-drama, thriller og mørkere katalogtitler.
- I dag får hun stort sett de samme blockbusterne som alle andre.
- **Marte** vil ha en anbefaling klar til produktmøtet i morgen.
- **Amira** spør om systemet systematisk favoriserer mainstream-smak.

> Dette er ikke bare en modelløvelse. Det er en produktbeslutning.

<!--
SPEAKER NOTES:
Etabler de tre perspektivene tidlig:
- Lea: brukeropplevelse og relevans.
- Marte: leveransepress og tid.
- Amira: fairness, eksponering og bredde.
Misforståelse å avklare: "best offline score" er ikke automatisk best produktvalg.
-->

---

## To Spor Gjennom Workshopen

| Case | Konsepter |
|---|---|
| Hvorfor mister vi Lea? | Hvilke signaler finnes i anbefalingssystemer? |
| Hvorfor popularitet ikke nok? | Hvordan evaluerer vi topp-N-anbefalinger? |
| Hva kan vi gjøre bedre? | Hva er content-based, collaborative og matrix factorization? |
| Hva bør vi shippe? | Hvorfor ender ekte systemer som hybrider? |

<!--
SPEAKER NOTES:
Forklar at case-sporet og konseptsporet må holdes sammen hele veien.
Intervensjon ved fastlåsing: Hvis gruppen blir for teknisk tidlig, trekk tilbake til Lea-spørsmålet.
-->


---

## Læringsmål

Etter workshopen skal deltakerne kunne forklare:

- forskjellen på **eksplisitt** og **implisitt** feedback
- hvorfor **rangering** ofte er viktigere enn rating-prediksjon
- når **content-based filtering** fungerer godt
- hva **collaborative filtering** fanger som innhold alene ikke ser
- hvorfor **matrix factorization** ble den klassiske arbeidshesten
- hvorfor modne produkter ofte lander på **hybride systemer**

<!--
SPEAKER NOTES:
Be deltakerne lese første og siste punkt høyt.
Poeng: vi starter i signalforståelse og ender i systemdesign/produksjon.
-->

---

## Beslutningskriterier (brukes gjennom hele dagen)

Vi evaluerer alle forslag mot de samme kriteriene:

| Kriterium | Praktisk spørsmål |
|---|---|
| Relevans | Treffer vi faktisk brukerens smak i topp-N? |
| Personalisering | Blir listen vesentlig annerledes for ulike brukere? |
| Fairness og mangfold | Eksponerer vi mer enn bare mainstream? |
| Latens og kost | Kan dette kjøres stabilt i produksjon? |
| Operasjonell risiko | Forstår vi failure modes og fallback? |

> En modell "vinner" ikke før den også er driftsbar.

<!--
SPEAKER NOTES:
Dette er anker-sliden for beslutning.
Bruk den som referanse i hver notebook-overgang: "Hva lærte vi nå om kriterium X?"
-->

---

<!-- _class: lead -->

# Del 2
## Flyt gjennom notebooks

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

<!--
SPEAKER NOTES:
Mikro-overganger:
- Etter baseline: "Nå vet vi hva vi slår."
- Etter content-based: "Nå har vi første personalisering."
- Etter CF/ALS: "Nå lærer systemet av kollektive mønstre."
-->

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

<!--
SPEAKER NOTES:
Pek tydelig på at appendix er for fordypning, ikke blokkering.
Rescue prompt ved tidspress: "Kjør kjerneceller først, appendix etterpå."
-->

---

## Metodetaksonomi (for denne workshopen)

| Familie | Hva den er best på | Typisk svakhet |
|---|---|---|
| Popularitetsbaseline | Robust start, enkel drift | Ingen ekte personalisering |
| Innholdsbasert | Cold-start på nye items, forklarbarhet | Smale anbefalinger |
| Collaborative / ALS | Sterk personalisering fra mønstre | Cold-start og sparsitet |
| Hybrid + reranking | Balanserer relevans, fairness og policy | Mer kompleks drift |

> Tommelfingerregel: bruk minst to signaltyper før produksjonsvalg.

<!--
SPEAKER NOTES:
Denne sliden spiller samme rolle som metodeoversikten i XAI-decket.
Mål: gi deltakerne et mentalt kart før de dykker i detaljer.
-->

---

<!-- _class: lead -->

# Del 3
## Signal, metrikker og baseline

---

## Hvilket signal har vi?

| Type | Eksempler | Fordel | Problem |
|---|---|---|---|
| **Eksplisitt feedback** | Ratings, likes, tommel opp | Tydelig preferanse | Sjeldent i virkelige produkter |
| **Implisitt feedback** | Klikk, visning, avspilling, kjøp | Finnes i store mengder | Manglende data er tvetydig |

For StreamNord er hovedsignalet **implisitt**: vi ser at Lea så noe, men ikke sikkert hvorfor.

> Manglende interaksjon betyr ikke nødvendigvis avvisning.

<!--
SPEAKER NOTES:
Kritisk avklaring: "No-click" kan bety både irrelevans, manglende synlighet eller tidsmangel.
Spørsmål til rommet: "Hva mister vi når vi behandler manglende interaksjon som negativ feedback?"
-->

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

<!--
SPEAKER NOTES:
Fremhev at metrikker er produktnære når de matcher UI-overflate (topp-N).
Vanlig misforståelse: "høy RMSE" betyr ikke nødvendigvis dårlig listekvalitet.
-->

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

<!--
SPEAKER NOTES:
Be gruppen formulere ett scenario der popularitet faktisk er riktig valg (f.eks. ny markedslansering).
Så kontrastér med Lea-caset for å tydeliggjøre begrensningen.
-->

---

## Checkpoint 1: Hva har vi lært så langt?

- Vi har et tvetydig, implisitt signal.
- Vi må evaluere topp-N, ikke bare predikere rating.
- Popularitet er nødvendig baseline, men utilstrekkelig for Lea.

**Spørsmål til gruppen:** Hva må neste modell gjøre bedre enn popularitet for å være verdt kompleksiteten?

<!--
SPEAKER NOTES:
Bruk 2-3 minutter til plenumsoppsummering før dere går videre til modellfamilier.
-->

---

<!-- _class: lead -->

# Del 4
## Modellfamilier i praksis

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

<!--
SPEAKER NOTES:
Foreslå en konkret failure mode: overfitting til sjangeretiketter gir lite serendipity.
Intervensjon: spør hvordan man kan utvide feature-sett (metadata, embeddings, tekst).
-->

---

## Modellfamilie 2: Collaborative Filtering

Idé:

- bruk mønstre i **andre brukeres atferd** til å anbefale for deg
- «brukere som liker det Lea liker, liker også dette»

To nyttige innganger:

- **item-item** som intuitiv start
- **user/item mønstre** som går utover eksplisitte features

Dette er ofte punktet der systemet begynner å oppdage smak som metadata alene ikke fanger.

<!--
SPEAKER NOTES:
Forklar intuitivt: "andre brukere fungerer som signalforsterkere."
Misforståelse: CF er ikke magi; uten nok interaksjoner blir signalet svakt.
-->

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

<!--
SPEAKER NOTES:
Knytt latente faktorer til produktspråk: "smaksdimensjoner vi ikke har navngitt."
Spørsmål: "Hva kan gå galt hvis vi kun optimaliserer for historisk engasjement?"
-->

---

## Hvorfor Ekte Systemer Ender Som Hybrider

Ingen enkeltmodell løser hele produktproblemet:

- **Popularitet** er robust, men upersonlig
- **Innholdsbasert** hjelper med cold start og forklarbarhet
- **Collaborative / ALS** gir sterk personalisering
- **Regler og reranking** håndterer fairness, mangfold og policy

Det realistiske sluttpunktet er derfor ofte et **hybridsystem**.

<!--
SPEAKER NOTES:
Dette er broen fra modell til system.
Gjør det tydelig at hybrid ikke er "nice to have", men vanligvis nødvendig i produksjon.
-->

---

## Checkpoint 2: Lea, Marte, Amira

| Rolle | Hva trenger de nå? |
|---|---|
| Lea | Reell personalisering uten repetisjon |
| Marte | En anbefaling som kan implementeres raskt |
| Amira | Synlig kontroll på bias, eksponering og mangfold |

> Hvis en løsning ignorerer én av disse, er den ikke produksjonsklar.

<!--
SPEAKER NOTES:
Bruk denne til å få gruppen ut av ren modelltenkning og inn i produktbalanse.
-->

---

<!-- _class: lead -->

# Del 5
## Begrensninger og beslutning

---

## De Virkelige Begrensningene

- **Cold start** — hva gjør vi når brukeren eller itemet er nytt?
- **Popularitetsbias** — blir alt dratt mot de samme hittene?
- **Latens** — kan modellen svare raskt nok i produktet?
- **Feedback-løkker** — trener vi bare på konsekvensene av egne anbefalinger?
- **Fairness og mangfold** — hvem taper når vi maksimerer gjennomsnittlig relevans?

Dette er der Amira kommer inn i historien.

<!--
SPEAKER NOTES:
Ramme inn som risikoregister, ikke bare "ulemper".
Be gruppen velge én risiko de ville monitorert fra dag 1 etter launch.
-->

---

## Beslutningsmatrise før ship

Skår hvert alternativ 1-5 på kriteriene under:

| Alternativ | Relevans | Personalisering | Fairness | Latens/kost | Driftbarhet | Sum |
|---|---:|---:|---:|---:|---:|---:|
| Popularitet |  |  |  |  |  |  |
| Content-based |  |  |  |  |  |  |
| CF/ALS |  |  |  |  |  |  |
| Hybrid + reranking |  |  |  |  |  |  |

> Fylles ut i siste del av workshopen som grunnlag for anbefalingen.

<!--
SPEAKER NOTES:
Insister på at de begrunner hver score med observasjoner fra notebooks.
Mål: gjøre sluttrådet etterprøvbart, ikke intuitivt.
-->

---

## Sluttleveransen

Ved slutten av workshopen skal deltakerne kunne si:

- hva slags signal StreamNord har
- hvilken modellfamilie som løser hva
- hvorfor Lea fortsatt er en nyttig stresstest
- hvorfor den endelige anbefalingen sannsynligvis er **hybrid**

> Åpne `notebooks/00_velkommen.ipynb` — vi begynner med Lea, dataene og signalet vi faktisk har.

<!--
SPEAKER NOTES:
Avslutt med tydelig forventning: "I dag skal dere ikke bare lære modeller, men forsvare et produksjonsvalg."
-->
