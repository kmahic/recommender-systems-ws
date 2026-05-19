# StreamNord Workshop — Facilitatorguide

> Internt dokument for kursholder. Denne versjonen følger den **konsoliderte**
> workshopen med fem hovednotebooks og appendixstoff inne i notebookene.

## Oversikt

| Notebook | Rolle | Tid (ca.) | Appendix |
|----------|-------|-----------|----------|
| `00_velkommen.ipynb` | Case, signal, metrikker og baseline | 60 min | Tilfeldig baseline |
| `01_content_based.ipynb` | Første personaliserte modell | 30 min | Embeddings og ANN |
| `02_collaborative_filtering.ipynb` | CF og ALS | 45 min | Faktorsveip og tolkning |
| `03_hybrid_systems.ipynb` | Hybrider, fairness og reranking | 60 min | Kalibrering |
| `04_ship_decision.ipynb` | Sluttanbefaling og cold start | 30 min | — |

Alle hoveddelene følger mønsteret **kjør → observer → diskuter → beslutning**.

## Didaktisk prinsipp

Workshopen følger to spor samtidig.

- **Narrativt spor:** Lea er brukerhistorien, Marte er forretningspresset, og Amira er fairness- og risikoperspektivet.
- **Konseptuelt spor:** eksplisitt vs implisitt feedback, evaluering, baselines, content-based filtering, collaborative filtering, matrix factorization og hybridsystemer.

Målet er at deltakerne både skal kunne forklare **hva StreamNord bør bygge** og
**hvorfor ulike modellfamilier eksisterer**.

## Notebook 00 — Velkommen

### Mål

- etablere caset og hvorfor Lea er viktig
- forklare eksplisitt vs implisitt feedback
- forklare topp-N-evaluering og leave-one-out-splitt
- vise at popularitet er en sterk baseline, men et dårlig produkt for Lea

### Kjerneflyt

- kjør miljøsjekk og datalasting
- vis nøkkeltall: brukere, filmer, interaksjoner, sparsitet
- stopp ved Lea og spør hva slags innhold deltakerne selv ville anbefalt henne
- gå gjennom eksplisitt vs implisitt feedback før metrikker
- kjør popularitetsbaseline og vis listene til Lea

### Det viktigste å si høyt

- sparsitet er grunnproblemet i anbefalingssystemer
- implisitt feedback er rikelig, men vanskelig å tolke
- ranking er viktigere enn rating-prediksjon for dette caset
- en baseline kan være både sterk og utilstrekkelig samtidig

### Appendix

- tilfeldig baseline kan brukes hvis du vil vise en eksplisitt nedre grense
- hopp over appendix hvis gruppen allerede forstår hvorfor popularitet er vanskelig å slå

## Notebook 01 — Content-based Filtering

### Mål

- introdusere den første personlige modellen i workshopen
- vise hva metadata alene kan og ikke kan gjøre
- gjøre det tydelig hvorfor content-based filtering fortsatt er viktig i praksis

### Kjerneflyt

- kjør setup og sammenlign popularitet mot content-based filtering
- vis Leas anbefalinger fra begge modellene
- stopp ved diskusjonen om når metadata er nyttig og hva som mangler

### Det viktigste å si høyt

- content-based filtering er ofte den enkleste inngangen til personalisering
- modellen er spesielt nyttig ved **nye items** og **tynne brukerprofiler**
- metadata gir ofte bedre sjangermatch enn popularitet, men ikke nødvendigvis best relevans

### Appendix

- embeddings og ANN skal behandles som produksjonsutvidelse, ikke som nødvendig kjerneinnhold
- appendix kan tas etter notebook 02 når deltakerne har sett ALS

## Notebook 02 — Collaborative Filtering og ALS

### Mål

- forklare collaborative filtering via item-item som intuitiv start
- introdusere matrix factorization som det store konseptuelle hoppet
- bruke ALS som den klassiske arbeidshesten for implisitt feedback

### Kjerneflyt

- kjør item-similarity-eksemplet og diskuter hva naboskapene egentlig betyr
- kjør head-to-head mellom item-item og ALS
- vis Lea-anbefalinger fra begge modeller
- stopp ved diskusjonen om hvorfor latente faktorer generaliserer bedre

### Det viktigste å si høyt

- collaborative filtering bruker mønstre i mange brukeres atferd, ikke bare metadata
- item-item er pedagogisk nyttig fordi det er konkret og tolkbart
- ALS introduserer latent struktur og blir ofte sterkere enn rene nabolagsmetoder

### Appendix

- faktorsveip og naboanalyse er nyttig for avanserte grupper
- dette stoffet kan kuttes uten å svekke den grunnleggende forståelsen av matrix factorization

## Notebook 03 — Hybrid Systems

### Mål

- vise hvorfor ekte produkter sjelden bruker én ren modell
- introdusere kontekst som et ekstra signal
- vise at fairness og reranking er produktkrav, ikke pynt

### Kjerneflyt

- bruk sesjoner som et konkret eksempel på hvordan en hybrid kan kombinere langtidsprofil og korttidskontekst
- kjør den kompakte sammenligningen mellom ren sesjon, blanding og ren ALS
- kjør popularitetsbias-analysen og gruppesammenligningen
- kjør ALS vs ALS+MMR og diskuter tradeoff mellom relevans og mangfold

### Det viktigste å si høyt

- hybrider oppstår fordi produktkrav trekker i forskjellige retninger
- kontekst hjelper ikke alltid alle like mye, men kan være avgjørende for enkelte situasjoner
- fairness må observeres på gruppenivå, ikke bare i et gjennomsnittstall
- reranking er ofte stedet der produktkrav faktisk implementeres

### Appendix

- kalibrering ligger som valgfri utdypning for grupper som vil dykke dypere i fairness-måling

## Notebook 04 — Ship Decision

### Mål

- samle modellfamiliene i én eksplisitt sluttbeslutning
- vise hvordan cold start påvirker anbefalingen til Marte
- lande på en hybrid anbefaling med tydelige begrunnelser

### Kjerneflyt

- kjør leaderboardet for modellfamiliene
- la deltakerne skrive eller diskutere en anbefaling til Marte
- kjør cold-start-analysen og knytt den tilbake til innholdsbasert filtering
- bruk Leas reise gjennom workshopen som oppsummering

### Det viktigste å si høyt

- workshopen skal ikke ende med “ALS vinner”, men med “et hybridoppsett er mest realistisk”
- cold start er grunnen til at content-based filtering og produktgrep fortsatt er viktige
- fairness og reranking er en del av produksjonsdesignet, ikke et ekstra vedheng

## Cheat Sheet — Oppgaver og diskusjonsspørsmål

Strukturen nedenfor matcher oppgavenumrene i notebookene nøyaktig.
For hvert spørsmål deltakerne ser vises fasilitatorsvaret rett under.

---

### Notebook 00 — Velkommen *(ingen nummerert oppgave)*

#### Gjetning — Før vi kjører noen modell

Deltakerne skriver 3 gjetninger i en kodecelle: hva Lea vil like, hva popularitetslisten vil inneholde, og om popularitet vil fungere for henne.

**Fasilitatoroppgave:** gi dem 2–3 minutter til å skrive. Ikke diskuter gjetningene ennå — de skal sammenlignes etter baselinen.

#### Etter popularitetsbaselinen — Sjekk gjetningene

En markdown-celle ber deltakerne sammenligne gjetningene sine med det de faktisk ser.

**Obs:** Leas popularitetsliste ligner veldig på listen til en tilfeldig bruker. Vis overlappet eksplisitt.

**Hvis det stopper:** «Hva vet vi faktisk om Lea, og hva antar vi bare fordi hun har sett noe?»

**Valgfri appendix — tilfeldig baseline:** hopp over hvis gruppen allerede forstår at popularitet er vanskelig å slå.

---

### Notebook 01 — Innholdsbasert filtering

#### Oppgave 1 — Innholdsbasert som første personalisering

> *Slik spørsmålene står i notebooken:*
> 1. Hjelper metadata Lea mer enn popularitet gjør? Hvordan ser du det?
> 2. Når er innholdsbasert filtering spesielt nyttig i praksis?
> 3. Hva er den største svakheten ved å bruke bare metadata?

**1.** Pek dem mot Leas liste, ikke bare tallene. Innholdsbasert gir ofte bedre sjangermatch, men metrikken er ikke alltid dramatisk bedre.

**2.** Nye items uten interaksjonshistorikk. Situasjoner der forklarbarhet eller sjangermatch er viktigere enn rå nøyaktighet.

**3.** Modellen ser bare metadata — den fanger ikke «alle som liker X liker også Y» hvis Y ikke deler metadata med X. Ingen kollektiv intelligens.

**Hvis det stopper:** minn dem på at brukerprofilen bygges ved å gjennomsnittberegne sjangervektorene til det Lea allerede har sett.

#### Skriveøvelse — Forklar forskjellen uten fagsjargong

Deltakerne skriver én setning til Marte som forklarer forskjellen mellom popularitet og innholdsbasert — uten ordene *vektor*, *matrise* eller *cosine*.

**Fasilitatoroppgave:** gi dem 1–2 minutter. Be 2–3 personer lese høyt. Poenget er at de øver på å oversette teknikk til produktspråk tidlig, ikke bare i sluttanbefalingen.

**God retning:** «Popularitet gir alle den samme listen. Innholdsbasert bruker hva Lea allerede liker til å finne lignende innhold.»

**Valgfri appendix — embeddings og ANN:** kan tas etter notebook 02 for å koble content-based-tenkning til produksjonsskala.

---

### Notebook 02 — Collaborative filtering og ALS

#### Oppgave 2 — Inspiser item-likhet

> *Slik spørsmålene står i notebooken:*
> 1. Ser naboskapet meningsfullt ut?
> 2. Hva fanger item-item-likheten som metadata alene ikke så godt viser?
> 3. Hvorfor er dette fortsatt begrenset?

**1.** Noen naboer bør virke riktige basert på franchise, stemning eller målgruppe — det er et godt tegn.

**2.** Atferdsmønstre som ikke er synlige i metadata: filmer som ses i samme stemning, av samme type brukere, på tvers av sjangere.

**3.** Metoden er lokal og sårbar for sparsitet. Populære items dominerer naboskapene fordi de har flest interaksjoner.

**Hvis det stopper:** be deltakerne lese naboene som «hvilke filmer ses av samme type brukere?» heller enn «hvilke filmer har samme metadata?»

#### Oppgave 3 — Head-to-head: item-item vs ALS

> *Slik spørsmålene står i notebooken:*
> 1. Hvorfor vinner ALS ofte over item-item?
> 2. Hva er forskjellen på en nabolagsmetode og latente faktorer?
> 3. Ser ALS mer ut som et realistisk produksjonsvalg enn item-item? Hvorfor?

**1.** ALS komprimerer signal fra hele matrisen og generaliserer bedre — det hjelper særlig for sparsom data og kalde brukere.

**2.** Nabolag bruker rå likhet mellom items direkte. Latente faktorer er lærte representasjoner som fanger underliggende struktur på tvers av hele datasettet.

**3.** ALS skalerer bedre og er mer robust. Item-item er pedagogisk nyttig, men sjelden tilstrekkelig alene i produksjon.

#### Refleksjon — Sjekk prediksjonen din

Deltakerne går tilbake til gjetningene fra notebook 00 og sammenligner med det de har sett så langt.

**Fasilitatoroppgave:** gi dem 1–2 minutter. Spør kort: «Hva hadde dere rett i? Hva overrasket?» Dette lukker sløyfen fra starten og gjør at Lea føles mer som en reell bruker, ikke bare en datapunkt.

**Valgfri appendix — faktorsveip og tolkning:** nyttig for grupper som vil forstå hyperparametervalg eller inspisere Leas nærmeste naboer i ALS-rommet.

---

### Notebook 03 — Hybrider, kontekst og fairness

#### Oppgave 4 — Korttidskontekst som hybridsignal

> *Slik spørsmålene står i notebooken:*
> 1. Hvorfor kan en kombinasjon av langtidsprofil og sesjon være bedre enn bare én av delene?
> 2. Hvem hjelper korttidskontekst mest?
> 3. Hva sier dette om hvorfor ekte systemer blir hybride?

**1.** Langtidsprofilen sier «hvem du er». Sesjonssignalet sier «hva du vil akkurat nå». De to fanger ulike dimensjoner av behov.

**2.** Brukere med bred smak, og situasjoner der intensjonen endrer seg raskt fra økt til økt.

**3.** Ingen enkeltmodell løser hele produktproblemet. Hybrider oppstår fordi ulike signaler er sterke i ulike situasjoner, og fordi produktkrav trekker i flere retninger.

**Hvis det stopper:** «Når kan Lea ønske noe annet akkurat nå enn det historikken hennes vanligvis sier?»

#### Oppgave 5 — Fairness og reranking

> *Slik spørsmålene står i notebooken:*
> 1. Hvem taper på en ren ALS-modell?
> 2. Hva vinner vi og hva taper vi når vi re-rangerer for mangfold?
> 3. Hva ville du fortalt Amira om systemets styrker og svakheter akkurat nå?

**1.** Brukere med smak for long-tail-innhold. Vis `share_recommended` mot `share_catalogue`-grafen — skjevheten er vanligvis tydelig.

**2.** Bedre coverage og novelty, men som regel noe lavere Recall@K. Det er en eksplisitt produkttradeoff, ikke en feil.

**3.** Modellen fungerer godt i snitt, men mainstream-brukere drar opp gjennomsnittet. Fairness må styres aktivt, ikke antas.

**Hvis det stopper:** pek dem til to konkrete sammenligninger: `share_catalogue` vs `share_recommended` i grafen og `Recall` vs `Coverage/Novelty` i tabellen.

**Valgfri appendix — kalibrering:** mål KL-divergens mellom brukerens faktiske sjangerprofil og anbefalingene. Nyttig hvis gruppen vil kvantifisere fairness dypere.

---

### Notebook 04 — Sluttanbefaling

#### Oppgave 6 — Leaderboard for modellfamiliene

Ingen diskusjonsspørsmål i notebooken. Leaderboardet er input til neste oppgave.

**Fasilitatoroppgave:** la deltakerne peke ut to ting: hvilken modell som er best på ren nøyaktighet, og hvilken som virker mest realistisk som produktkomponent. Disse er sjelden den samme.

#### Beslutningsmal

Deltakerne fyller inn en strukturert mal (signal, modell, cold start, fairness, arkitektur, risiko) **før** de skriver fritekstanbefalingen.

**Fasilitatoroppgave:** gi dem 3–5 minutter for malen. Malen er gjenbrukbar — minn dem på at de kan ta den med seg etter workshopen.

#### Oppgave 7 — Hva anbefaler du å shippe?

Deltakerne bruker malen som grunnlag og skriver: *«Marte, basert på analysen anbefaler jeg … fordi …»*

**Fem ting anbefalingen bør adressere** *(fra notebooken)*:
1. nøyaktighet — hvilken modell presterer best?
2. mangfold og fairness — hvem hjelpes og hvem hjelpes ikke?
3. cold start — hva skjer med nye brukere?
4. forklarbarhet — kan vi forklare valget til Lea?
5. produksjonskostnad — hva er realistisk å drifte?

**God retning:** ALS som kjerne, content-based som cold-start-støtte, reranking for mangfold og fairness, kontekst der det gir tydelig verdi.

**Hvis det stopper:** «Hva ville dere gjort for Lea på dag 1, og hva ville dere gjort etter at hun har sett 50 filmer?»

#### Oppgave 8 — Cold start

Ingen diskusjonsspørsmål i notebooken. Kurven er konklusjonen.

**Fasilitatoroppgave:** be deltakerne lese kurven og si med egne ord hva den betyr for produksjonsvalget.

**God retning:** ytelsen faller raskt ved kortere historikk, noe som betyr at en ren collaborative modell ikke er nok alene. Cold start er det sterkeste argumentet for å beholde content-based-signaler og onboarding-grep i arkitekturen.

#### Refleksjon — Sjekk gjetningene fra starten

Etter Leas reise gjennom workshopen ber en siste markdown-celle deltakerne gå tilbake til notebook 00 og reflektere: hva hadde de rett i, hva tok de feil om, og hva overrasket mest.

**Fasilitatoroppgave:** dette er den siste refleksjonsøvelsen. Be 2–3 personer dele kort. Poenget er at workshopen ikke bare lærte dem teknikker, men endret forståelsen de startet med.

---

### Korte oppfølgingsspørsmål som virker gjennom hele workshopen

- «Hva ser dere i Leas liste som metrikken alene ikke forteller?»
- «Hvis dette skulle vært i produksjon neste måned, hva hadde dere beholdt og hva hadde dere kuttet?»
- «Hvem tjener på denne modellen, og hvem taper på den?»
- «Hva er den billigste forbedringen som faktisk hjelper produktet?»
- «Hvilken komponent ville dere vært mest nervøse for å drifte?»

## Anbefalt Sluttanbefaling

Hvis gruppen trenger en referanse, er dette en god standardkonklusjon:

1. Bruk en sterk collaborative modell som ALS som hovedmotor når det finnes nok interaksjonsdata.
2. Bruk content-based signaler som støtte ved cold start og for forklarbarhet.
3. Bruk reranking for mangfold, fairness og produktpolitikk.
4. Legg til kontekst der det faktisk gir bruker- eller forretningsverdi.

## Hvis Tiden Blir Presset

- kutt appendixstoff først
- behold alltid popularity baseline, content-based filtering, ALS og sluttanbefalingen
- behold fairness-diskusjonen selv om du kutter kalibrering og dypere visualiseringer
- hvis du må korte ytterligere ned, gjør notebook 03 mer diskusjonsdrevet og mindre eksperimenttung