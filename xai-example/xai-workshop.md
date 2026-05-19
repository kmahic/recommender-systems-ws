---
marp: true
theme: default
paginate: true
backgroundColor: #1a1a2e
color: #e0e0e0
style: |
  section {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  }
  h1, h2, h3 {
    color: #f5c542;
  }
  section.lead h1 {
    font-size: 1.25em;
    text-align: center;
  }
  section.lead h2 {
    text-align: center;
    color: #c0c0c0;
  }
  section.lead p {
    text-align: center;
  }
  section.invert {
    background-color: #16213e;
  }
  table {
    font-size: 0.6em;
  }
  blockquote {
    border-left: 4px solid #f5c542;
    padding-left: 1em;
    color: #c0c0c0;
    font-style: italic;
  }
  code {
    background-color: #2a2a4a;
    color: #f5c542;
    padding: 1px 2px;
    border-radius: 2px;
  }
  em {
    color: #8ecae6;
  }
  strong {
    color: #f5c542;
  }
  .emoji {
    font-size: 1.5em;
  }
---

<!-- _class: lead -->

# XAI Detektiv-Workshop

## Tolkbar og forklarbar AI — En praktisk etterforskning

<br>

*12.02.2026*

<!-- 
SPEAKER NOTES:
Velkommen til XAI Detektiv-Workshop! I dag skal vi bli datadetektiver.

Hva handler dette om?
Vi har en maskinlæringsmodell — en XGBoost-klassifiserer — som brukes av et forsikringsselskap
til å avgjøre om krav skal godkjennes eller avslås. Men modellen oppfører seg mistenkelig:
en lojal kunde blir avslått, mens en risikokunde blir godkjent. Vår jobb er å bruke
verktøy fra feltet "Explainable AI" (XAI) til å etterforske hva modellen egentlig gjør.

Hvorfor dette formatet?
Detektiv-metaforen er bevisst: XAI handler om å stille spørsmål, samle bevis, og trekke
konklusjoner — akkurat som en etterforskning. Vi starter med hypoteser, tester dem med data,
og reviderer underveis.

Praktisk info:
- Workshopen er ~4 timer med pause
- Hoveddelen er selvgående notatbøker — dere kjører kode og svarer på øvelser
- Mellom notatbøkene samles vi for korte diskusjoner
- Det finnes fasiter i solutions/-mappen, men prøv selv først!
-->

---

# Agenda

| Tid | Aktivitet |
|-----|-----------|
| 0:00 | **Introduksjon** — denne presentasjonen |
| 0:20 | **Notatbok 01** — Saksmappen: data, modell, mysterium |
| 0:45 | **Notatbok 02** — Undersøk åstedet: globale forklaringer |
| 1:00 | ☕ Pause (15 min) |
| 1:15 | **Notatbok 03** — Avhør av mistenkte: lokale forklaringer |
| 1:35 | **Notatbok 04** — Når forklaringer lyver: kritisk tenkning |

<!--
SPEAKER NOTES:
Gå gjennom tidsplanen og pek på strukturen:
- Vi starter med denne intro-presentasjonen (~25 min) for å gi dere det teoretiske
  grunnlaget før dere går hands-on.
- Notatbok 01-03 bygger opp forståelsen gradvis: data → globalt → lokalt.
- Etter pausen kommer den kritiske vendingen (NB04) der vi avslører at forklaringer
  kan lyve — dette er den viktigste leksjonen i workshopen.
- NB05 handler om å omsette alt til en konkret beslutning og kommunisere den.

Brodiskusjonene (5 min mellom notatbøker) er viktige — de sørger for at gruppen
reflekterer sammen, ikke bare koder individuelt. Still åpne spørsmål og la
deltakerne dele hypoteser.
-->

---

<!-- _class: lead -->

# Del 1
## Hvorfor trenger vi forklarbar AI?

---

# AI er overalt — men hva skjer inni?

<br>

```
  
                ┌───────────────┐
                │               │
   Inndata  →   │   BLACK BOX   │ →  Beslutning
                │       ?       │ 
                │               │
                └───────────────┘
```

<br>

Maskinlæringsmodeller kan være svært nøyaktige, men **ingen forstår hvorfor** de tar beslutningene de gjør.

<!--
SPEAKER NOTES:
Dette er kjerneproblemet i moderne ML:

Enkle modeller (lineær regresjon, beslutningstrær) kan du lese og forstå direkte.
Men de beste modellene — XGBoost, nevrale nettverk, random forests — er for komplekse.
En XGBoost-modell kan ha hundrevis av trær med tusenvis av splits. Ingen mennesker
kan lese det og forstå hva som skjer.

Men noen MÅ forstå modellen. Hvorfor?
1. Regulatorer krever det (EU AI Act, GDPR art. 22)
2. Brukere fortjener å vite hvorfor de ble avslått
3. Utviklere trenger å finne og fikse feil
4. Ledelsen må kunne stå inne for beslutningene

Det er her XAI kommer inn — verktøy som lar oss "åpne" svartboksen
og forstå hva som foregår inni, uten å måtte lese hvert eneste tre.

Still gjerne spørsmålet til gruppen: "Har noen av dere jobbet med modeller
der dere IKKE forsto hvorfor den ga et bestemt svar?"
-->

---

# Når svartboksen svikter


**Virkelige eksempler på AI som gikk galt:**

- **Amazon-rekruttering (2018):** Modellen diskriminerte kvinner fordi historiske data favoriserte menn
- **COMPAS (USA):** Algoritme for straffutmåling hadde systematisk bias mot afroamerikanere
- **Helsekostnader (2019):** Brukt 'historiske kostnader' som proxy — fanger opp ulikhet, ikke sykdom
- **Kredittvurdering:** GDPR og EU AI Act gir borgere *rett til forklaring*


> Uten forklaring — ingen tillit, ingen rettferdighet, ingen debugging.

<!--
SPEAKER NOTES:
Gå gjennom hvert eksempel kort — dette motiverer hele workshopen:

Amazon (2018):
- Amazon bygde et internt rekrutteringsverktøy som scoret CVer automatisk.
- Modellen ble trent på 10 års historiske ansettelsesdata — der de fleste ansatte var menn.
- Resultatet: den straffet CVer som inneholdt ordet "women's" (f.eks. "women's chess club").
- Uten forklaring hadde dette gått i produksjon uten at noen oppdaget det.

COMPAS (USA):
- Brukt i rettssystemet for å vurdere risiko for tilbakefall.
- ProPublica viste i 2016 at algoritmen systematisk ga høyere risikoscore til
  afroamerikanere, selv med lik kriminell historikk.
- Modellen var en svartboks — dommere stolte blindt på den.

Helsekostnader (Obermeyer et al., 2019):
- En algoritme brukt av amerikanske sykehus til å prioritere pasienter.
- Den brukte "historiske helsekostnader" som proxy for helsebehov.
- Men: svarte pasienter hadde historisk lavere kostnader (pga. systemisk ulikhet
  i tilgang til helsevesenet), så algoritmen undervurderte deres behov.
- Forklarbarhet avslørte at proxyen fanget opp ulikhet, ikke sykdom.

EU AI Act:
- Trådte i kraft 2024, full implementering 2026.
- Høyrisiko-systemer (kreditt, forsikring, ansettelse, helse) KREVER forklarbarhet.
- GDPR art. 22 gir allerede rett til å ikke bli utsatt for helautomatiserte beslutninger.
- For norske konsulenter: dette er ikke fremtid — det er NÅ.
-->

---

# Hva er XAI?

**Explainable AI (XAI)** = teknikker som gjør maskinlæringsbeslutninger **tolkbare for mennesker**.


Tre hovedgrunner til å bruke XAI:

| | Grunn | Eksempel |
|---|-------|---------|
| 1 | **Tillit** | Kan vi stole på modellen i produksjon? |
| 2 | **Debugging** | Hvorfor feiler modellen på denne gruppen? |
| 3 | **Rettferdighet** | Behandler den alle grupper likt? |

<br>

> *«Forklaringer forklarer **modellen**, ikke virkeligheten.»*
> En perfekt forklaring av en ødelagt modell er perfekt ødelagt.

<!--
SPEAKER NOTES:
De tre grunnene utdypet:

1. TILLIT: Før du setter en modell i produksjon, må du kunne forklare til stakeholders
   (ledelse, jurister, kunder) hvorfor den tar de beslutningene den gjør. Uten forklaring
   er det umulig å bygge tillit — og uten tillit blir modellen aldri tatt i bruk.

2. DEBUGGING: Modeller feiler på uventede måter. Kanskje den fungerer bra overordnet,
   men katastrofalt dårlig for en bestemt kundegruppe eller region. XAI-verktøy hjelper
   deg å finne HVOR og HVORFOR den feiler — mye mer effektivt enn å bare se på accuracy.

3. RETTFERDIGHET: Modeller kan arve bias fra treningsdata uten at du vet det.
   XAI gjør det mulig å oppdage om modellen diskriminerer basert på kjønn, etnisitet,
   geografi, eller andre sensitive attributter — selv indirekte.

DEN GYLNE REGELEN — les sitatet høyt:
"Forklaringer forklarer MODELLEN, ikke virkeligheten."

Dette er det viktigste poenget i hele workshopen. En forklaring sier deg hva modellen
vektlegger — men det betyr IKKE at modellen har rett. Hvis modellen er feilkalibrert,
biased, eller trent på lekkende data, vil forklaringen trofast beskrive modellens feil.

Analogi: Tenk på en forklaring som et røntgenbilde av modellen. Røntgenbildet viser
nøyaktig hva som er der — men det er opp til deg som "lege" å vurdere om det du ser
er sunt eller sykt.

Vi kommer tilbake til denne regelen i NB04 — der den virkelig synker inn.
-->

---

<!-- _class: lead -->

# Del 2
## Taksonomi — Typer forklaringer

---

# Globalt vs. lokalt

```
┌──────────────────────────────────────┐
│       GLOBALE FORKLARINGER           │
│  «Hvordan tenker modellen OVERORDNET?»│
│                                      │
│  Permutation    PDP/ICE    SHAP      │
│  Importance     plott      opps.     │
└──────────────────────────────────────┘
                    ↕
┌──────────────────────────────────────┐
│        LOKALE FORKLARINGER           │
│  «Hvorfor DENNE prediksjonen?»       │
│                                      │
│  SHAP           LIME       DiCE      │
│  waterfall                 kontrafakt.│
└──────────────────────────────────────┘
```

<!--
SPEAKER NOTES:
Dette er den viktigste taksonomien i XAI — og den dere trenger å forstå:

GLOBALE FORKLARINGER:
- Svarer på: "Hvordan oppfører modellen seg generelt, på tvers av ALLE data?"
- Analogi: Et fugleperspektiv — du ser hele landskapet.
- Eksempel: "claim_amount er den viktigste featuren for modellen" (Permutation Importance)
- Eksempel: "Jo høyere kravbeløp, desto lavere sannsynlighet for godkjenning" (PDP)
- Bruksområde: Modellvalidering, stakeholder-rapportering, bias-deteksjon.

LOKALE FORKLARINGER:
- Svarer på: "Hvorfor ga modellen DETTE svaret for DENNE ene personen?"
- Analogi: Et forstørrelsesglass — du zoomer inn på én enkelt sak.
- Eksempel: "For Kari bidro region=Trondheim med -0.15 til prediksjonen" (SHAP waterfall)
- Eksempel: "Hadde Kari bodd i Oslo, ville kravet blitt godkjent" (DiCE kontrafaktisk)
- Bruksområde: Klagebehandling, individuell forklaring, "Hvorfor ble JEG avslått?"

Viktig poeng: Du trenger BEGGE.
- Globalt uten lokalt = du forstår systemet, men kan ikke forklare enkeltsaker.
- Lokalt uten globalt = du kan forklare enkeltsaker, men aner ikke hva modellen
  gjør som helhet (kanskje den er fundamentalt feil).

I workshopen: NB02 = globalt, NB03 = lokalt. Rekkefølgen er bevisst — vi starter
med det store bildet før vi zoomer inn.
-->

---

# Andre dimensjoner

<br>

| Dimensjon | Alternativ A | Alternativ B |
|-----------|-------------|-------------|
| **Modellagnostisk** vs. **Modellspesifikk** | Fungerer på *alle* modeller (LIME, SHAP Kernel) | Utnytter modellstruktur (SHAP TreeExplainer) |
| **Post-hoc** vs. **Ante-hoc** | Forklarer *etter* trening | Innebygd tolkbarhet (lineær regresjon, beslutningstre) |
| **Feature-attribusjon** vs. **Kontrafaktisk** | «Feature X bidro med +0.3» | «Hadde claim_amount vært 15k → godkjent» |

<br>

I dag bruker vi **post-hoc, modellagnostiske** teknikker på en **XGBoost-svartboks**.

<!--
SPEAKER NOTES:
Tre viktige dimensjoner å forstå:

1. MODELLAGNOSTISK vs. MODELLSPESIFIKK:
   - Modellagnostiske metoder (LIME, SHAP KernelExplainer, Permutation Importance)
     behandler modellen som en svartboks — de sender inn data og observerer output.
     Fordel: fungerer på ALT. Ulempe: kan være trege.
   - Modellspesifikke metoder (SHAP TreeExplainer) utnytter modellens interne struktur.
     Fordel: mye raskere og mer nøyaktig. Ulempe: fungerer bare på bestemte modelltyper.
   - I dag: Vi bruker TreeExplainer for SHAP (fordi vi har XGBoost), men LIME og DiCE
     er modellagnostiske.

2. POST-HOC vs. ANTE-HOC:
   - Post-hoc: Du trener modellen først, og forklarer den etterpå.
     Det er dette vi gjør i dag — modellen er allerede trent.
   - Ante-hoc: Modellen er designet for å være tolkbar fra starten
     (f.eks. lineær regresjon, GAM, beslutningstre). Koeffisientene ER forklaringen.
   - Trade-off: Ante-hoc-modeller er enklere å tolke, men ofte mindre nøyaktige.
     Post-hoc lar deg bruke kraftige modeller OG forklare dem.

3. FEATURE-ATTRIBUSJON vs. KONTRAFAKTISK:
   - Feature-attribusjon: "Feature X bidro med +0.3 til beslutningen." (SHAP, LIME)
     Svarer på: HVORFOR?
   - Kontrafaktisk: "Hadde du endret X fra A til B, ville utfallet blitt annerledes." (DiCE)
     Svarer på: HVA KAN ENDRES?
   - Begge er verdifulle — for ulike brukere. Tekniske folk liker attribusjon,
     sluttbrukere liker kontrafaktiske.

I dag bruker vi post-hoc, hovedsakelig modellagnostiske teknikker på XGBoost.
Vi trener bevisst en svartboks for å simulere en realistisk situasjon.
-->

---

<!-- _class: lead -->

# Del 3
## Verktøykassen — Metodene vi bruker i dag

---

# Permutation Importance

**Idé:** Stokk verdiene til én feature og mål hvor mye nøyaktigheten *faller*.

<br>

```
  Original            Stokket «region»
┌──────────────┐    ┌──────────────┐
│ alder: 45    │    │ alder: 45    │
│ region: Oslo │    │ region: Bodø │  ← tilfeldig
│ beløp: 50k   │    │ beløp: 50k   │
│ ...          │    │ ...          │
└──────────────┘    └──────────────┘
   accuracy: 92%       accuracy: 84%  → Importance = 8%
```

<br>

✅ Rask, intuitiv, modellagnostisk
⚠️ Kan gi misvisende resultat med *korrelerte* features

<!--
SPEAKER NOTES:
Permutation Importance — mer detaljert forklaring:

HVORDAN DET FUNGERER:
1. Tren modellen som vanlig og mål baseline-ytelse (f.eks. accuracy = 92%).
2. Ta én feature — f.eks. "region" — og stokk (permuter) verdiene tilfeldig.
   Det betyr at hver rad får en tilfeldig region fra en annen rad.
   Alle andre features beholder sine ekte verdier.
3. Kjør modellen på nytt med den stokkede featuren og mål ny ytelse (f.eks. 84%).
4. Differansen (92% - 84% = 8%) er feature importance for "region".
5. Gjenta for alle features.

INTUISJON:
Hvis en feature er viktig for modellen, vil det å stokke den ødelegge
prediksjonsevnen. Hvis en feature er uviktig, vil det å stokke den
ikke gjøre nevneverdig forskjell.

FORDELER:
- Enkel å forstå og forklare til ikke-tekniske folk
- Rask å beregne
- Fungerer på ALLE modelltyper (modellagnostisk)
- Innebygd i scikit-learn

FALLGRUVER (som dere oppdager i NB04):
- Korrelerte features: Hvis "age" og "years_as_customer" er høyt korrelerte,
  vil det å stokke den ene ikke ødelegge mye — fordi den andre "tar over".
  Begge features kan da fremstå som lite viktige, selv om de samlet er veldig viktige.
- Permutation Importance måler viktighet for MODELLEN, ikke i virkeligheten.
  En lekkende feature vil rangeres som viktigst.

I NB02 bruker dere sklearn.inspection.permutation_importance.
-->

---

# PDP og ICE

**Partial Dependence Plot (PDP):** Gjennomsnittlig effekt av feature X på prediksjonen.

**Individual Conditional Expectation (ICE):** Én linje *per observasjon*.

```
  Prediksjon
    ↑
    │     ╱── ICE (individ A)
    │   ╱──── ICE (individ B)              ICE-linjene viser
    │ ╱────── PDP (gjennomsnitt)  ←──      at individer kan
    └──────────────────────→
              claim_amount
```
✅ Viser *retning* og *form* på effekten
⚠️ PDP kan skjule motstridende undergrupper (Simpsons paradoks!)

<!--
SPEAKER NOTES:
PDP og ICE — mer detaljert forklaring:

PARTIAL DEPENDENCE PLOT (PDP) — slik fungerer det:
1. Velg en feature, f.eks. "claim_amount".
2. Lag et grid av verdier (f.eks. 10k, 20k, 30k, ..., 200k).
3. For HVER verdi i gridet:
   a. Sett claim_amount = den verdien for ALLE rader i datasettet.
   b. Kjør modellen og beregn gjennomsnittlig prediksjon.
4. Plott gjennomsnittlig prediksjon mot claim_amount-verdiene.

Dette gir deg én kurve som viser: "Hva skjer med den gjennomsnittlige prediksjonen
når claim_amount varierer fra lav til høy?"

ICE (Individual Conditional Expectation) — samme prosess, men:
- I stedet for å ta gjennomsnittet i steg 3, plotter du HVER rad separat.
- Du får én linje per observasjon i datasettet.
- PDP = gjennomsnittet av alle ICE-linjene.

HVORFOR ICE ER VIKTIG:
Hvis noen ICE-linjer går OPP og andre går NED, kan PDP-gjennomsnittet
være en flat linje — som ser ut som "denne featuren betyr ingenting".
Men i virkeligheten betyr den mye, bare i MOTSATT RETNING for ulike grupper.

Dette er Simpsons paradoks i praksis — og dere vil oppleve det i NB02.
Globalt kan PDP si "region har liten effekt", mens ICE avslører at effekten
er positiv for noen grupper og negativ for andre.

I NB02 bruker dere sklearn.inspection.PartialDependenceDisplay.
-->

---

# SHAP (SHapley Additive exPlanations)

**Idé fra spillteori:** Fordel «kreditt» rettferdig mellom alle features.

```
  Base value (gjennomsnittlig prediksjon)
     │  + region: Oslo       → +0.12        Hvert feature
     │  + claim_amount: 80k  → -0.08   ←── dytter prediksjonen
     │  + years_customer: 2  → -0.03        opp eller ned
     │  + ...
     ▼
  Endelig prediksjon for denne raden
```

✅ Matematisk solid, kan brukes globalt *og* lokalt
✅ Rask for tremodeller (TreeExplainer)
⚠️ Kan fordele kreditt uforutsigbart mellom *korrelerte* features

<!--
SPEAKER NOTES:
SHAP — mer detaljert forklaring:

BASIS I SPILLTEORI:
Shapley-verdier ble introdusert av Lloyd Shapley i 1953 (Nobel i økonomi 2012).
Opprinnelig problem: Hvis et lag med spillere samarbeider og skaper en gevinst,
hvordan fordeler vi gevinsten RETTFERDIG mellom spillerne?

Svar: For hver spiller, beregn marginalbidraget i alle mulige koalisjoner.
Gjennomsnittlig marginalbidrag = Shapley-verdi.

FOR ML:
- "Spillere" = features (alder, region, kravbeløp, ...)
- "Gevinst" = differansen mellom prediksjon og gjennomsnittlig prediksjon (base value)
- SHAP-verdi for feature X = gjennomsnittlig marginalbidrag av X
  når vi vurderer alle mulige kombinasjoner av features.

EKSEMPEL:
Base value (gjennomsnittlig prediksjon) = 0.65 (65% sannsynlighet for godkjenning).
For Kari:
  + region: Trondheim → -0.15 (drar ned)
  + years_customer: 12 → +0.08 (drar opp)
  + claim_amount: 50k → -0.05 (drar litt ned)
  + _internal_score → -0.20 (drar kraftig ned)
  = Endelig prediksjon: 0.33 → Avslått.

Summen av SHAP-verdier + base value = eksakt prediksjon. Alltid.
Dette er den unike egenskapen som skiller SHAP fra andre metoder.

GLOBALT vs. LOKALT:
- Lokalt (waterfall): Viser nedbryting for ÉN prediksjon (som eksempelet over).
- Globalt (beeswarm/bar): Viser absolutte SHAP-verdier aggregert over alle data.
  Gir en rangering av hvilke features som er viktigst globalt.

TreeExplainer vs. KernelExplainer:
- TreeExplainer: Utnytter trestruktur. Eksakt og VELDIG rask for XGBoost/RF.
  I praksis: sekunder for tusenvis av prediksjoner.
- KernelExplainer: Modellagnostisk, men TREG. Approksimerer med sampling.
  Kan ta minutter-timer for store datasett.
- I dag bruker vi TreeExplainer fordi vi har XGBoost.

FALLGRUVER:
- Korrelerte features: SHAP kan fordele kreditt vilkårlig mellom korrelerte features.
  Eksempel: Hvis feature A og B er 95% korrelerte, kan SHAP gi all kreditt til A
  i én kjøring og til B i en annen. Samlet bidrag er riktig, men fordelingen er ustabil.

Dere bruker shap-biblioteket i NB02 (globalt) og NB03 (lokalt).
-->

---

# LIME (Local Interpretable Model-agnostic Explanations)

**Idé:** Tren en *enkel* modell (lineær) som etterligner den svarte boksen *lokalt*.

```
                    ┌─ Generer naboer rundt punktet
  Observasjon X  ───┤─ Spør svartboksen om prediksjon for hver nabo
                    └─ Tren lineær modell på naboene
                         ▼
                    "region = Oslo → +0.15"
```

✅ Rask, intuitiv, fungerer på *alle* modelltyper
⚠️ **Ustabil** — kan gi ulike svar med ulike tilfeldige frø
⚠️ Avhenger av hvordan naboer genereres

<!--
SPEAKER NOTES:
LIME — mer detaljert forklaring:

HVORDAN DET FUNGERER:
1. Velg en observasjon du vil forklare (f.eks. Karis forsikringskrav).
2. Generer "naboer": Lag hundrevis av syntetiske datapunkter i nærheten
   av originalen ved å legge til tilfeldig støy.
3. For hver nabo: Kjør svartboks-modellen og få en prediksjon.
4. Vekt naboene: De som er nærmest originalen får høyest vekt.
5. Tren en enkel, tolkbar modell (lineær regresjon) på de vektede naboene.
6. Koeffisientene i den lineære modellen = "forklaring" for dette punktet.

INTUISJON:
Svartboksen er for kompleks til å forstå globalt. Men LOKALT — i et lite
område rundt ett datapunkt — er den kanskje tilnærmet lineær.
LIME finner denne lokale lineære tilnærmingen.

Analogi: Jordoverflaten er krum (kompleks), men lokalt ser den flat ut.
LIME finner "det flate kartet" rundt ett punkt.

NAVNET FORKLART:
- Local: Forklarer kun ÉN prediksjon, ikke hele modellen.
- Interpretable: Bruker en enkel modell (lineær regresjon) som IS tolkbar.
- Model-agnostic: Trenger bare å kunne kalle predict() — fungerer på alt.
- Explanations: Resultatet er en forklaring.

HOVEDPROBLEM — USTABILITET:
Fordi naboene genereres tilfeldig, kan du få ULIKE forklaringer hver gang
du kjører LIME med et nytt tilfeldig frø. Eksempel:
  Kjøring 1: "region er viktigst"
  Kjøring 2: "claim_amount er viktigst"
  Kjøring 3: "years_as_customer er viktigst"

Dette er et reelt problem. I NB04 demonstrerer vi dette ved å kjøre LIME
5 ganger med ulike frø og vise at resultatene spriker.

PRAKTISK ANBEFALING:
- Bruk LIME som et raskt førsteutkast, men valider alltid med SHAP.
- Hvis LIME og SHAP er enige: økt tillit.
- Hvis de er uenige: SHAP er vanligvis mer pålitelig (matematisk garantier).

Dere bruker lime-biblioteket i NB03.
-->

---

# DiCE — Kontrafaktiske forklaringer

**Idé:** Finn den *minste* endringen som flipper beslutningen.

```
  NÅVÆRENDE situasjon:              KONTRAFAKTISK:
  ┌─────────────────────┐          ┌─────────────────────┐
  │ region: Trondheim   │   ──→    │ region: Oslo    ✏️  │
  │ claim_amount: 50k   │          │ claim_amount: 35k ✏️│
  │ prior_claims: 0     │          │ prior_claims: 0     │
  │ → AVSLÅTT ❌        │         │ → GODKJENT ✅       │
  └─────────────────────┘          └─────────────────────┘
```

✅ Svarer på «Hva kan jeg *gjøre*?» — handlingsrettet
✅ Forståelig for ikke-tekniske interessenter
⚠️ Flere mulige kontrafaktiske svar — ikke alltid realistiske

<!--
SPEAKER NOTES:
DiCE (Diverse Counterfactual Explanations) — mer detaljert forklaring:

HVORDAN DET FUNGERER:
1. Start med en observasjon der modellen ga et bestemt utfall (f.eks. "avslått").
2. Søk etter det MINSTE settet med endringer som flipper prediksjonen til "godkjent".
3. Optimaliser for:
   a. Nærhet: Endringene skal være så små som mulig.
   b. Diversitet: Gi FLERE ulike kontrafaktiske svar, ikke bare ett.
   c. Realisme: Endringene bør være realistiske (ikke "sett alder til -5").

EKSEMPEL FOR KARI:
"Kari ble avslått. Hva måtte vært annerledes?"
- Kontrafaktisk 1: Endre region fra Trondheim til Oslo → godkjent.
- Kontrafaktisk 2: Reduser claim_amount fra 50k til 30k → godkjent.
- Kontrafaktisk 3: Endre _internal_score fra lav til høy → godkjent.

HVORFOR ER DETTE NYTTIG?
- For KUNDEN: "Hva kan jeg gjøre annerledes neste gang?" (handlingsrettet)
- For REGULATORER: "Er det rimelig at region alene snur beslutningen?" (rettferdighet)
- For UTVIKLERE: "Modellen er veldig sensitiv for region — er det tilsiktet?" (debugging)

VIKTIG BEGRENSNING:
- Kontrafaktiske forklaringer sier IKKE at endringen ville fungert i virkeligheten.
  De sier bare: "Ifølge modellen ville dette endret utfallet."
  Men modellen KAN være feil (tilbake til den gylne regelen).
- Noen endringer er ikke realistiske: "Bli 10 år yngre" er ikke handlingsrettet.
  DiCE lar deg sette restriksjoner på hvilke features som kan endres.

DiCE vs. andre kontrafaktiske metoder:
- DiCE gir DIVERSE kontrafaktiske svar (flere alternativer), ikke bare det nærmeste.
  Dette er mer nyttig fordi det gir brukeren valgmuligheter.

Dere bruker dice-ml-biblioteket i NB03.
-->

---

# Metodeoversikt

| Metode | Globalt/Lokalt | Hastighet | Stabilitet | Best for |
|--------|---------------|-----------|------------|----------|
| **Permutation Importance** | Globalt | Rask | Høy | Feature-rangering |
| **PDP / ICE** | Globalt | Middels | Høy | Feature-effekter |
| **SHAP** | Begge | Rask* | Høy | Omfattende analyse |
| **LIME** | Lokalt | Rask | **Lav** | Rask lokal tilnærming |
| **DiCE** | Lokalt | Middels | Middels | Handlingsrettede svar |

_*Rask for tremodeller (TreeExplainer), treg for andre_

<br>

> **Tommelfingerregel:** Bruk alltid **≥ 2 metoder** og sammenlign.
> Enighet styrker tilliten — uenighet avslører problemer.

<!--
SPEAKER NOTES:
Denne tabellen oppsummerer metodene — pek på noen nøkkelpunkter:

1. STABILITET er avgjørende:
   - SHAP og PI er stabile — kjør dem 10 ganger, få samme svar.
   - LIME er USTABIL — ulike kjøringer kan gi motstridende svar.
   - DiCE er middels — du får ulike kontrafaktiske svar, men det er ved design
     (diversitet er en feature, ikke en bug).

2. HASTIGHET varierer enormt:
   - PI og LIME: Sekunder.
   - SHAP TreeExplainer: Sekunder for tremodeller.
   - SHAP KernelExplainer: Minutter til timer.
   - PDP: Sekunder til minutter avhengig av grid-størrelse.

3. TOMMELFINGERREGELEN — denne er viktig:
   Bruk ALLTID minst 2 metoder og sammenlign.
   - Hvis de er enige: Sterk indikasjon på at forklaringen er pålitelig.
   - Hvis de er uenige: Det er et rødt flagg — undersøk nærmere.
   Eksempel fra workshopen: LIME og SHAP kan gi ulike rangering av features
   for enkeltobservasjoner. Det betyr ikke at én er feil — det betyr at
   du trenger å forstå HVORFOR de er uenige.

Tabellen finnes også i templates/xai_cheatsheet.md — oppfordre deltakerne
til å ha den åpen som referanse mens de jobber.
-->

---

<!-- _class: lead -->

# Del 4
## Fallgruver — Det som kan gå galt

---

# Fire feller som lurer

<br>

Du vil møte alle disse i **Notatbok 04**. Her er en forsmak:

<br>

| # | Felle | Hva skjer? |
|---|-------|-----------|
| 1 | **Korrelerte features** | To features som måler «det samme» — SHAP fordeler kreditt tilfeldig mellom dem |
| 2 | **Datalekkasje** | En feature som «jukser» — gir perfekt forklaring av et meningsløst mønster |
| 3 | **Ustabilitet** | Kjør samme forklaring to ganger, få ulikt svar |
| 4 | **Subgruppeeffekter** | Det globale gjennomsnittet skjuler at undergrupper oppfører seg *motsatt* |

<br>

> Disse er ikke edge cases — de er **vanlige** i ekte prosjekter.

<!--
SPEAKER NOTES:
Dette er en TEASER — ikke avslør detaljene! NB04 har den store aha-opplevelsen.
Men forklar konseptene kort så de gjenkjenner dem når de møter dem:

1. KORRELERTE FEATURES:
   Teoretisk: Når to features er høyt korrelerte (f.eks. r > 0.8), bærer de
   overlappende informasjon. Permutation Importance undervurderer begge
   (fordi den andre "tar over"), og SHAP fordeler kreditt vilkårlig mellom dem.
   I praksis: Du kan ikke stole på individuelle feature-importance-verdier
   for korrelerte features. Du må vurdere dem som en gruppe.

2. DATALEKKASJE:
   Teoretisk: En feature som er avledet fra (eller korrelert med) målvariabelen
   på en måte som ikke ville vært tilgjengelig ved prediksjonstidspunkt.
   Klassisk: predicted_label brukt som feature. Subtilt: en intern score
   som er beregnet basert på utfallet.
   Konsekvens: Modellen bruker "juksekoden" og forklaringene viser at den
   gjør det — men det er ikke en nyttig forklaring.
   HINT: Det finnes en mistenkelig feature i datasettet vårt... 🤔

3. USTABILITET:
   LIME-spesifikt: Kjør LIME 5 ganger med ulike random seeds og sammenlign.
   Hvis topp-3-featurene bytter plass mellom kjøringer, er forklaringen ikke til å stole på.

4. SUBGRUPPEEFFEKTER (Simpsons paradoks):
   Teoretisk: Et mønster som er sant for hele populasjonen, men som reverseres
   når du deler opp i undergrupper. Klassisk eksempel: Berkeley-opptak 1973.
   Globalt: Det så ut som universitetet diskriminerte kvinner.
   Per avdeling: Kvinner hadde høyere accept rate — men de søkte til mer
   kompetitive avdelinger.
   I vår kontekst: En PDP kan vise "region har liten effekt", men for
   undergrupper kan effekten være sterk og motstridende.

Si til gruppen: "Husk disse fire — dere møter dem alle i NB04.
-->

---

<!-- _class: lead -->

# Del 5
## Caset: Forsikringskrav

---

# Scenariet

Du er ansatt som **datadetektiv** hos et norsk forsikringsselskap.

Selskapet bruker en ML-modell (XGBoost) til å avgjøre om forsikringskrav skal **godkjennes** eller **avslås**.

<br>

Men noe stemmer ikke.

Kunder klager. Ledelsen er bekymret. Datatilsynet banker på døren.

<br>

**Din oppgave:** Bruk XAI-verktøy for å etterforske modellen — og skriv din dom.

<!--
SPEAKER NOTES:
Dette er den narrative rammen — bruk den dramatisk:

"Dere er ansatt som datadetektiver. Forsikringsselskapet har fått klager fra kunder
som mener de ble urettferdig behandlet. Datatilsynet har begynt å spørre spørsmål.
Ledelsen vil vite: Kan vi stole på modellen? Er den rettferdig? Hva driver beslutningene?"

Dataene er syntetiske (generert med et Python-skript), men scenariet er realistisk.
I den virkelige verden bruker forsikringsselskaper ML-modeller til å:
- Vurdere risiko og prise forsikringer
- Flagge potensielt svindel
- Avgjøre om krav skal godkjennes automatisk eller sendes til manuell vurdering

Disse modellene er under intenst regulatorisk press:
- Finanstilsynet (norsk) stiller krav til modellstyring
- EU AI Act klassifiserer forsikring som høyrisiko
- Kundene har krav på begrunnelse

Så scenariet er ikke hypotetisk — det er dagen til mange av dere om ikke lenge.

XGBoost-modellen vi bruker er trent i NB01. Den er bevisst designet med noen
"feil" som deltakerne skal oppdage gjennom XAI-verktøyene.
-->

---

# Datasettet
**~5 000 forsikringskrav** med følgende egenskaper:

| Feature | Beskrivelse | Eksempel |
|---------|-------------|---------|
| `claimant_age` | Alder på forsikringstaker | 45 |
| `region` | Geografisk region | Oslo, Bergen, Trondheim, Stavanger, Bodø |
| `policy_type` | Type forsikring | bolig, bil, reise, helse |
| `years_as_customer` | År som kunde | 12 |
| `prior_claims` | Antall tidligere krav | 0 |
| `claim_amount` | Kravbeløp (NOK) | 50 000 |
| `vehicle_value` | Kjøretøyverdi | 250 000 |
| `sum_insured` | Forsikringssum | 500 000 |
| `fraud_flag` | Svindelflagg | 0 |
| `_internal_score` | Intern score | 🤔 |

**Målvariabel:** `approved` (1 = godkjent, 0 = avslått)

<!--
SPEAKER NOTES:
Gå gjennom tabellen og fremhev:

- Features er en blanding av numeriske (alder, beløp, år som kunde) og kategoriske
  (region, policy_type). XAI-metoder håndterer disse ulikt — SHAP kan håndtere
  begge, men LIME krever encoding.

- Pek SPESIELT på _internal_score og si:
  "Hm, dette er en intern score. Vi vet ikke helt hva den representerer ennå.
  Legg merke til den — og kom tilbake til meg hvis dere finner ut noe."
  (Tonefall: mystisk, plantet hint.)

- IKKE avslør at _internal_score er en lekkende feature. Det er den store
  avsløringen i NB04. Men PLANTE frøet her, slik at deltakere som er
  oppmerksomme husker det når de ser den dominere i forklaringene.

- Hvis noen spør: "Er _internal_score korrelert med target?" — svar:
  "Godt observert! Finn ut av det i notatbøkene."

- Datasettet har ~5000 rader, nok til å trene en XGBoost-modell med
  rimelig ytelse. Det er bevisst designet med:
  1. Regionale forskjeller (Oslo vs. Trondheim)
  2. En lekkende feature (_internal_score)
  3. Korrelerte features
  4. Subgruppeeffekter
  Alt dette oppdages gjennom XAI-verktøyene.
-->

---

# Møt de mistenkte


### Kari (rad 42)

| | |
|---|---|
| **Alder** | 52 år |
| **Region** | Trondheim |
| **Kundeforhold** | 12 år |
| **Tidligere krav** | 0 |
| **Kravbeløp** | ~50 000 NOK |
| **Resultat** | ❌ **AVSLÅTT** |

En lojal kunde med null historikk — hvorfor ble hun avslått?

<!--
SPEAKER NOTES:
Kari er bevisst valgt for å vekke sympati og rettferdighetsfølelse:

Presenter henne dramatisk:
"Møt Kari. 52 år. Har vært kunde i 12 år. Aldri sendt inn et eneste krav.
Nå sender hun inn sitt FØRSTE krav — 50 000 kroner. Modellen sier: AVSLÅTT."

"Hva tenker dere? Er dette rettferdig?"

La gruppen reagere. De fleste vil si: "Nei! En lojal kunde med null historikk
burde absolutt få kravet godkjent!"

Poenget: Intuisjonen deres er riktig — men å BEVISE det krever XAI-verktøy.
"Magefølelse" er ikke nok for å klage til Datatilsynet eller rapportere
til ledelsen. Vi trenger evidens.

En annen viktig detalj: Kari er fra Trondheim. Husk det.
Hvis noen spør "Er regionen relevant?" — si: "Godt spørsmål. Vi finner ut."
-->

---

# Møt de mistenkte

### Erik (rad 7)

| | |
|---|---|
| **Alder** | 28 år |
| **Region** | Oslo |
| **Kundeforhold** | 2 år |
| **Tidligere krav** | 2 |
| **Kravbeløp** | ~175 000 NOK |
| **Resultat** | ✅ **GODKJENT** |

En ny kunde med flere tidligere krav og høyt beløp — hvorfor ble han godkjent?

<br>

> **Noe stemmer ikke. Din jobb er å finne ut hva.**

<!--
SPEAKER NOTES:
Kontrasten mellom Kari og Erik er selve mysteriet:

"Nå møter dere Erik. 28 år. Kunde i bare 2 år. HAR allerede 2 tidligere krav.
Og nå sender han inn et krav på 85 000 kroner — nesten dobbelt så mye som Kari.
Modellen sier: GODKJENT."

"Kari: lojal, null historikk, lavt beløp → AVSLÅTT."
"Erik: ny, flere krav, høyt beløp → GODKJENT."
"Noe stemmer ikke. Og det er DIN jobb å finne ut hva."

Dette er det sentrale mysteriet i workshopen. La det synke inn.

Hvis noen spør "Er det fordi Erik er fra Oslo?" — si:
"Interessant hypotese. Test den."

Hvis noen spør "Er det _internal_score?" — si:
"Veldig godt observert. Hold den tanken."

De vil gjennom NB02 og NB03 gradvis bygge opp evidens, og i NB04
får de den fulle forklaringen: datalekkasje (_internal_score) og
regionale bias-effekter.

Det viktige pedagogiske poenget: XAI-verktøy hjelper deg å gå fra
"dette føles feil" til "her er det kvantitative beviset på at det er feil,
og her er årsaken."
-->

---

# Etterforskningen — 5 notatbøker

```
  📁 01 Saksmappen          → Last data, tren modell, still hypotese
       │
  🔍 02 Undersøk åstedet    → Globale forklaringer (PI, PDP, SHAP)
       │
  🔦 03 Avhør av mistenkte  → Lokale forklaringer (SHAP, LIME, DiCE)
       │
  💥 04 Når forklaringer     → Kritisk tenkning — 4 feller
       │    lyver                (den store avsløringen!)
```


Hver notatbok har **øvelser** (markert med ✏️) som dere fyller ut.

<!--
SPEAKER NOTES:
Forklar strukturen:

- NB01 (Saksmappen, 30 min): Last data, gjør grunnleggende EDA, tren XGBoost-modellen,
  og møt Kari og Erik. Formålet er å danne hypoteser.
  Etter NB01, stilll spørsmålet: "Hva er magefølelsen din?"

- NB02 (Undersøk åstedet, 40 min): Globale forklaringer — Permutation Importance,
  PDP/ICE, SHAP beeswarm/bar. Dere ser det store bildet.
  Etter NB02: "Stemte det globale bildet med hypotesen din?"

- NB03 (Avhør av mistenkte, 55 min): Lokale forklaringer for Kari og Erik.
  SHAP waterfall, LIME, DiCE. Den lengste notatboken.
  Etter NB03: "Hvorfor ble Erik godkjent? Har du en teori?"

- NB04 (Når forklaringer lyver, 50 min): DEN VIKTIGE NOTATBOKEN.
  Her avslører vi 4 feller: korrelerte features, datalekkasje,
  LIME-ustabilitet, og Simpsons paradoks. Deltakerne oppdager at
  _internal_score er en lekkende feature og at region-effekten
  reverseres i undergrupper.
  Etter NB04: "Hva overrasket deg mest?"

- NB05 (Skriv dommen, 25 min): Omsett analysen til en strukturert
  beslutning ved hjelp av beslutningsmalen. Kommuniser funnene.

Hver notatbok har ✏️-øvelser som deltakerne fyller ut.
Fasiter i solutions/-mappen — men oppfordre folk til å prøve selv først.
-->

---

<!-- _class: lead -->

# Del 6
## Praktisk informasjon

---

# Oppsett

<br>

**Alternativ 1 — Lokalt (anbefalt)**
```bash
# Klone repoet
git clone <repo-url> && cd xAI

# Installer avhengigheter med uv
make setup

# Generer data
make data

# Start JupyterLab
make lab
```

<br>

--- 
#

**Alternativ 2 — Google Colab**
Hver notatbok har en Colab-kompatibilitetscelle øverst.

<!--
SPEAKER NOTES:
Sjekk at alles miljø fungerer NÅ. Vanligste problem: stifeil ved datalasting.
Hvis noen har problemer, Colab er plan B.
-->

---

# Ressurser


**I dette repoet:**

| Fil | Innhold |
|-----|---------|
| 📋 `templates/xai_cheatsheet.md` | Jukseark med metodeoversikt og beslutningsflyt |
| 📝 `templates/xai_decision_template.md` | Gjenbrukbar mal for XAI-prosjekter (brukes i NB05) |
| 📖 `solutions/` | Fasiter for alle øvelser |
| 📘 `slides/facilitator_guide.md` | Fasilitatorguide |

**Anbefalt videre lesing:**
- Christoph Molnar: *Interpretable Machine Learning* (gratis bok)
- SHAP-dokumentasjon: shap.readthedocs.io
- Ribeiro et al. (2016): *"Why Should I Trust You?" — LIME*
- Mothilal et al. (2020): *DiCE — Diverse Counterfactual Explanations*

<!--
SPEAKER NOTES:
Juksearket er en enside-referanse dere kan ha ved siden av notebooken hele tiden.
Beslutningsmalen bruker dere i NB05 — den er gjenbrukbar i egne prosjekter.
-->

---

<!-- _class: lead -->

# La oss begynne!

<br>

## Åpne `notebooks/01_the_case_file.ipynb`

<br>

*Saksmappen venter. Kari trenger din hjelp.*

<!--
SPEAKER NOTES:
Åpne NB01. Første celle laster avhengigheter — sjekk at det fungerer.
Gi deltakerne 30 minutter. Gå rundt og hjelp med eventuelle oppsettproblemer.
Etter NB01, samle gruppen for en 5-minutters diskusjon:
"Hva er magefølelsen din? Hvorfor ble Kari avslått — og Erik godkjent?"
-->
