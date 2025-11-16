# BORING MARKETING — Document Tehnic complet (MVP v1.0)

## 0. Viziune
BORING MARKETING este o aplicație AI care automatizează complet marketingul organic al unei companii. Întreabă. Analizează. Gândește. Creează. Postează. Răspunde. Convertește. Un sistem făcut să înlocuiască o agenție întreagă.

### În MVP
- short-form video
- imagini
- text
- strategie completă automatizată
- DM automation
- lead management
- posting automation

### În viitor
- landing pages
- paid ads
- outreach B2B
- generative video avansat
- integrări CRM profunde

## 1. Structura documentului
1. Viziune & scop
2. Onboarding inteligent
3. Analiza automată
4. Strategia automată
5. Generarea de conținut
6. Feedback loop & învățare
7. Programare & postare
8. DM automation
9. Lead pipeline
10. Necesare media
11. Dashboard
12. Agentul Central (AI Brain)
13. Arhitectură tehnică
14. Baza de date
15. API endpoints
16. UI Wireframes (textuale)
17. Roadmap MVP → V2 → V3
18. Definirea rolurilor sistemului
19. Costuri și resurse
20. Riscuri + soluții

## 2. Onboarding inteligent
### 2.1 Scop
Transformă minimalul oferit de user în informație clară, structurată, acționabilă. Userul poate începe doar cu numele brandului și o descriere simplă („vând suc de mere”). Aplicația duce conversația până la:
- scop marketing
- industria exactă
- tip client
- ton brand
- capacitate producție
- diferențiatori
- resurse media
- canale existente
- obiective reale

### 2.2 Flow-ul Onboarding
**Pasul 1: Identitate minimă**
- Numele brandului
- Ce vinde? (input liber + sugestii AI)

**Pasul 2: Ipoteze inteligente**
- AI analizează industria și generează 3–5 ipoteze de scop.
- Userul selectează/ignoră/adaugă.

**Pasul 3: Întrebări ghidate (max 7)**
- Selecție, multi-selecție, interval, slider, text, modele generate AI.

**Pasul 4: Resurse media**
- AI cere logo, poze produs, video, link-uri existente, prezentări, pdf-uri.
- Dacă nu există → AI generează propuneri.

**Pasul 5: Confirmare Profil Brand**
- Rezumat vizual editabil: obiectiv, industrie, persona preliminară, canale, diferențiatori, ton, resurse media.

## 3. Analiza automată
AI colectează date din site, Instagram, Facebook, TikTok, YouTube, LinkedIn, articole media, forumuri.

### 3.1 Elemente analizate
- tonul actual
- engagement
- tipuri postări
- culori brand
- logo detectat
- mesajele brandului
- puncte slabe/tari
- lucruri lipsă
- competitori direcți/indirecți
- trenduri industrie
- costuri de achiziție estimate
- comportamentul consumatorilor
- best practices globale

### 3.2 Output analiză
- „În industria X, contentul care funcționează este Y.”
- „Brandul dvs. folosește prea puțin Z.”
- „Aveți potențial în segmentul A, dar lipsă în segmentul B.”

## 4. Strategia automată
### 4.1 Componente
- Structura lunară/săptămânală
- Tipuri de conținut
- Platforme recomandate
- Volum postări
- Intensitatea DM/outreach
- Propuneri conturi suplimentare
- Ton, stil, limbaj

### 4.2 Niveluri buget
- 150 € / 500 € / 1000 € / slider liber
- Ajustează număr postări, platforme, calitatea media, DM-uri zilnice, adâncimea strategiei, tipurile de conținut.

### 4.3 Platforme analizate
TikTok, Instagram (Feed, Stories, Reels), Facebook, YouTube Shorts, LinkedIn, Email, WhatsApp Broadcast.

## 5. Generarea de conținut
Sistemul produce complet text, titlu, descriere, hook, poveste, CTA, copy lung/scurt, hashtags, prompt imagine/video, mockup vizual.

### 5.1 Short-form video
Hook → problemă → agitație → soluție → CTA.

### 5.2 Carusel
Titlu + 5–8 slide-uri + final slide CTA.

### 5.3 Story
1–3 cadre + CTA ușor + mesaj scurt.

### 5.4 Prompt video generativ
Integrare Veo3 / Runway / alt model.

## 6. Feedback loop & învățare
- Userul vede fiecare postare ca mockup.
- Poate accepta/modifica/respinge.
- Motive presetate (prea agresiv, prea slab, prea lung etc.).
- Sistemul reînvață preferințele și ajustează postările viitoare.

## 7. Programare & postare
Integrări Meta, TikTok, YouTube Shorts, LinkedIn, Mailchimp/SendGrid. Scheduler intern cu queue, fallback, retry, log errors, notificări.

## 8. DM automation
Orice interacțiune devine lead. Flow automat: mesaj inițial → întrebări → identificare nevoie → livrare material → cerere date → booking → follow-up → închidere. Adaptat industriei.

## 9. Lead pipeline
Stadii: New, Cold, Warm, Hot, Booked Call, No-Show, Sale, Lost. Pentru fiecare lead vezi discuția, statusul, sursa.

## 10. Necesare media
AI cere poze, video, testimoniale, clip fondator, catalog PDF, raport, text brut, culoare brand, logo. Dacă nu există, AI generează logo-uri, imagini, intro video, postări „fake UGC”.

## 11. Dashboard — Lumina de pe date
Secțiuni: Content Calendar, Lead Pipeline, DM Inbox, Postări viitoare, Analytics, Booking Calendar, Integrări, Setări AI.

## 12. Agentul Central (AI Brain)
Funcții: „Refă strategia.”, „Optimizează funnelul.”, „Propune 30 idei.”, „Explică-mi performanța.”, „Analizează competitorii.”, „Creează un nou persona.”

Integrează LLM, Vector DB, memorie persistentă.

## 13. Arhitectură tehnică
### 13.1 Backend
Python / Node.js; orchestrator, worker (scheduler), webhook handler, model chaining, DB layer.

### 13.2 Frontend
Next.js, UI minimalist (alb, negru, frost, blur, organic), animații line, 3-click rule.

### 13.3 AI Microservices
Persona Generator, Strategy Builder, Content Generator, Visual Prompt Engine, Feedback Learner, DM Engine, Lead Scoring Engine, Analytics Interpreter.

### 13.4 Database
PostgreSQL, Vector DB (Weaviate/Pinecone), Redis pentru caching.

## 14. Baza de date (structură simplificată)
- users(id, name, email, password hash, role)
- businesses(id, owner_id, name, industry, objective, brand_tone, resources_status)
- content_posts(id, business_id, platform, text, media_prompt, status, scheduled_at)
- leads(id, business_id, name, source, pipeline_stage, conversation_history JSON)
- strategy(id, business_id, content_plan, platforms, posting_frequency)

## 15. API endpoints
POST /onboarding/start; POST /onboarding/answer; GET /analysis/run; POST /strategy/generate; POST /content/generate; PUT /content/update-status; POST /schedule/post; POST /dm/trigger; POST /dm/send; GET /pipeline; POST /brain/query.

## 16. UI wireframes (textuale)
- **Onboarding:** card + input + sugestii + butoane select.
- **Strategie:** sidebar (Platforms / Budget / Tone) + panel cu plan vizual săptămânal.
- **Content Review:** grid mockup, Accept / Modify / Reject.
- **Lead Pipeline:** coloane Cold | Warm | Hot.

## 17. Roadmap
### MVP (0–3 luni)
Onboarding inteligent, generare strategie, generare content, DM automation basic, lead pipeline, posting scheduler.

### V2 (3–8 luni)
Generare landing pages, outreach B2B, A/B testing automat, template marketplace.

### V3 (8–18 luni)
Paid ads automation, generative video profesional, CRM complet, learning global.

## 18. Roluri în sistem
Proprietar business, Manager cont, AI Brain, DM Engine, Strateg Engine, Content Engine, Scheduler, Admin.

## 19. Resurse necesare
1 AI engineer, 1 fullstack dev, 1 designer, 1 UX, 1 QA, 1 devops.

## 20. Riscuri + soluții
- Rate limit la platforme → fallback queue
- DM restrictions → pacing + throttling
- User overwhelm → UI minimalist
- Cost AI → caching, low token usage
- Feedback complex → vector memory

---

# Capitolul 1 — Prima pagină: Login / Signup
## 1.1 Login page
UI minimalist (alb + negru + frost). Elemente: Email, Parolă, buton Login, link „Create account”, link „Forgot password”. Micro-interacțiuni: border frost-white la input, mesaj poetic la parolă greșită, animație loading (cerc care pulsează).

## 1.2 Signup page
Câmpuri: Nume, Email, Parolă, Confirm parolă, accept terms & privacy, buton “Create account”. Micro logică: mesaj pentru email existent; AI sugerează parolă puternică cu metafore; după signup → direct în Onboarding.

# Capitolul 2 — Onboarding (7 ecrane)
## 2.1 Ecran 1 — Identitate minimă
Titlu: „Hai să începem. Spune-mi doar esența.” Input brand + „Ce vinzi?”. AI ghicește industria, afișează badge „Am identificat industria.” Buton: Continuă.

## 2.2 Ecran 2 — Ipoteze inteligente
Titlu: „În industria ta, scopurile obișnuite sunt acestea.” AI generează 3–5 scopuri (ex: atragere distribuitori, creștere vânzări directe etc.). User selectează/ scrie altele. Micro logică: sugestii suplimentare pentru beverage.

## 2.3 Ecran 3 — Întrebări ghidate
Carduri poetice. Întrebări despre canal vânzare (cu opțiuni + sub-scenariu pentru distribuitori), capacitate producție (slider 1–10), ton brand (liste combinate).

## 2.4 Ecran 4 — Resurse media
Titlu: „Arată-mi ce ai ca să pot crea în stilul tău.” Upload logo, poze, clip, pdf, link-uri. Micro-comportamente: AI detectează logo slab → propune nou; dacă nu există nimic → generează (Minimal/Rustic/Premium/Organic/Modern).

## 2.5 Ecran 5 — Sumar Brand Persona v1
Card cu brand, industrie, tip client, obiective, diferențiatori, conținut necesar. Editabil.

## 2.6 Ecran 6 — Confirmare finală
Mesaj poetic: „Perfect. Am înțeles cine ești. Urmează să-ți creez lumea digitală.” Buton: „Începe analiza”.

# Capitolul 3 — Analiza
12 sub-analize: site, Instagram, TikTok, competitori (5 globali + 5 România + 5 similari), industrie, best practices globale, pagini actuale, buyer persona consumer, buyer persona distribuitor, costuri achiziție, ton recomandat, volum conținut necesar. Fiecare produce raport.

# Capitolul 4 — Strategia
- Platforme definite cu rol (TikTok growth, Instagram brand + vânzare, etc.).
- Buget slider (150/500/1000/custom) influențează nr. postări, tipuri, calitate, DM/outreach.

# Capitolul 5 — Generarea conținutului
Pentru fiecare postare: text, variantă scurtă/lungă, hook, flow narativ, CTA, hashtags, prompt vizual, time-of-day, motivul postării, micro-strategie, mockup vizual.

# Capitolul 6 — Feedback loop
Postare în format real (IG/TikTok). Butoane Accept/Respinge/Modifică. Motive presetate (prea agresiv, prea slab, prea lung, nepotrivit tonului/industriei, nu îmi place vizual, nu e uman/premium/autentic). AI învață.

# Capitolul 7 — Postări programate
AI stabilește zi/oră/platformă/caption/hashtags/media. Sistem: fallback, retry, notifications.

# Capitolul 8 — DM Automation
Toate interacțiunile → lead. AI trimite mesaj inițial, întrebări, detectează intenția, livrează materiale, cere date, programează call, face follow-up, DM Inbox stil WhatsApp.

# Capitolul 9 — Lead pipeline (Kanban)
Coloane: New, Cold, Warm, Hot, Booked, Sold, Lost. Drag&drop, click lead → conversație completă.

# Capitolul 10 — Agentul Central (AI Brain)
- UI minimal (birou alb, input „Spune-mi ce ai nevoie.” + sugestii poetice). Input cu efect liquid-glass.
- Categorii comenzi: Analiză, Conținut, Strategie, Funnel/DM, Lead-uri, Tehnic/Integrări, Vizual/Creativ.
- Logică internă: intenție, context, execuție, validare.
- Exemple interacțiune completă (idei TikTok pentru distribuitori), scor calitate output, memorie evolutivă, anti-repetiție.
- Accesibil din pagină dedicată, buton floating, DM editor, content calendar.
- Micro-animații (pulsație, fractal). Comenzi speciale („Restructurează tot”, „Adaptează pentru buget X”, „Plan pe 7 zile”, „Analizează luna trecută”).
- Ton poetic-minimal.

# Capitolul 11 — Dashboard complet
Structurat ca un templu modern cu 5 aripi: Overview, Content Calendar, DM & Leads, Analytics, Integrări & Setări.

## 11.1 Overview
Blocuri: Statusul zilei (indicatori), Pulsul social (grafic 7 zile), „Ce am făcut pentru tine” (timeline), „Recomandarea zilei” (AI insight + acțiuni). Hover/tooltip, CTA direct.

## 11.2 Content Calendar
Stil Google Calendar + Pinterest board. Cod culori per platformă, card postare (thumbnail, titlu, platformă, status). Meniu contextual (editare, regenerare text/vizual, copie, mutare, anulare, export, analiză). Drag-and-drop, micro-interacțiuni, filtre (platformă/status/tip/dimensiune). Buton „Creează postare nouă”.

## 11.3 DM & Leads
Ecran împărțit: Inbox DM (stil WhatsApp Business) + Lead Pipeline (Kanban). Detalii chat, butoane rapide, AI suggestions, voice-to-text poetic. Pipeline cu drag&drop, card lead cu date/conversație/interes/potențial/CTA recomandat, AI insight.

## 11.4 Analytics
Panou cu cifre mari (reach, lead-uri, conversii, cost per lead). Grafice performanță (bar + heatmap), originea lead-urilor, analiză per postare cu insight AI.

## 11.5 Integrări & setări
Carduri pentru IG, FB, TikTok, YouTube, LinkedIn, Shopify, WooCommerce, GA, WhatsApp API, Mailchimp, Sendgrid, Stripe. Stare, ultima sincronizare, număr evenimente, butoane Reconnect/Configure.

## 11.6 Notificări inteligente
Clopoțel cu notificări (trenduri, lead nou, postare programată, DM flow optimizat).

## 11.7 Micro-animații & limbaj vizual
Val lumină la mutare postare, puls verde la lead nou, cerc la postare, cristal la insight. Stil clar, elegant, premium.

# Capitolul 12 — Lead Pipeline (detaliat)
## 12.1 Structură vizuală
Kanban cu 7 coloane (New, Cold, Warm, Hot, Booked Call, Sale/Client, Lost). Micro interacțiuni.

## 12.2 Stadii lead
Definiții pentru fiecare stadiu (New, Cold, Warm, Hot, Booked Call, Sale/Client, Lost).

## 12.3 Logică AI pentru mutări
Inferența tonului, timpi răspuns, complexitate întrebări, analiză lingvistică.

## 12.4 Comportamente automate per stadiu
Mesaje automate adaptate stadiilor (New → mesaj inițial; Cold → follow-up; Warm → info + CTA; Hot → call; Booked → reminder; Sale → mulțumire; Lost → mesaj final).

## 12.5 Interacțiuni user
Click lead → card. Drag & drop → adaptare conversație. AI suggested action etc.

## 12.6 Card lead
Secțiuni: profil, timeline, pain points, recommended next step, lead score (0–100, culori).

## 12.7 Lead Score Engine
Parametri: timpi răspuns (20%), lungime mesaje (10%), calitatea întrebărilor (25%), emoție (15%), potrivire persona (10%), istoric interacțiuni (20%).

## 12.8 Triggeri/notificări/escalări
Notificări (lead nou, lead hot, 48h fără acțiune). Escalări automate pentru leaduri hot etc.

## 12.9 Reguli speciale per industrie
Exemple pentru suc de mere, imobiliare, fitness.

## 12.10 Funcții avansate
Smart Follow-Up (moment perfect + parametri), Smart Nurturing (picături conținut). Leaduri 40–60 scor primesc nurturing.

# Capitolul 13 — Flowchart-uri complete
## 13.1 Flow general
Login → Onboarding (dacă nu complet) → Analiză → Strategie → Generare conținut → Feedback → Calendar → DM automation → Lead pipeline → Analytics → AI Brain (loop continuu).

## 13.2 Flow Onboarding
Pași detaliați (date brand, industrie, scopuri, canal vânzare, capacitate/ambiție, ton brand, resurse media, rezumat & confirmare).

## 13.3 Flow Analiză + Strategie inițială
Colectare date, analiză brand, analiză industrie, creare persona, construire strategie, prezentare user.

## 13.4 Flow Generare conținut
Planificare volum, generare content slots, generare postări (hook, CTA, hashtags, prompt vizual), salvare drafturi, prezentare user.

## 13.5 Flow Calendar & Aprobare
Review, decizii user (approve/edit/reject + feedback), programare automată, postare efectivă.

## 13.6 Flow DM automation
Triggeri, detectare event, asociere flow, mesaje automate, stop criteria, salvare lead.

## 13.7 Flow Lead pipeline
Actualizare scor, decizie automată, trigger acțiuni, intervenție user.

## 13.8 Flow Analytics loop
Colectare date, analiză periodică, generare insights, ajustare strategie.

## 13.9 Flow AI Brain
Interpretare comandă, colectare context, execuție, confirmare pentru schimbări majore.

## 13.10 Flow „Regenerare tot” / schimbare buget
Preia strategia curentă, recalculează resurse, regenerează strategie, prezintă comparație, aplică.

# Capitolul 14 — Memoria AI (Vector DB & learning continuu)
Straturi: Brand Memory, User Behaviour Memory, Content Memory, Lead & Conversation Memory, Strategy & Performance Memory, Memoria globală.

## 14.1 Arhitectură de memorie
DB relațională + Vector DB (embedding-uri, metadata, retrieval contextual).

## 14.2 Brand Memory
Conține industrie, produs, ton, diferențiatori, poveste, exemple „da/nu”, mesaje preferate. Actualizată la onboarding și schimbări. Folosită la generare content, DM, strategie.

## 14.3 User Behaviour Memory
Preferințe user (ton preferat, motive reject, formate preferate, modul de răspuns la insight). Evenimente sumarizate și stocate.

## 14.4 Content Memory
Arhivă postări (text, tip, platformă, persona, scop, data, status, performanță). Rezumate vectoriale cu performance_score (0–100). Folosite pentru idei viitoare și anti-repetiție.

## 14.5 Lead & Conversation Memory
Istoric DM, întrebări, obiecții, replici eficiente. Rezumate conversații pentru training DM.

## 14.6 Strategy & Results Memory
Istoric strategii v1, v2 etc. cu rezultate și reacții user.

## 14.7 Global Memory
Pattern-uri generalizate (fără date sensibile) per industrie/conținut. Ajută brandurile noi.

## 14.8 Retrieval
Task → cerere de memorie (brand_profile, user_pref, content_post, conversation_summary, strategy_version, global_pattern). Folosite în prompt.

## 14.9 Learning loop
Approve/Reject, conversii/pierderi, comenzi AI Brain → evenimente → rezumate → vector DB → context viitor.

## 14.10 Uitare controlată
Deprecare veche, pruning după scor, agregare, limită per brand.

## 14.11 Securitate & izolare
Vectori marcați cu brand_id; retrieval per tenant; pattern-urile globale anonime.

# Capitolul 15 — Algoritmul de recomandare a conținutului
## 15.1 Scop
Nu doar umple calendarul, ci crește vizibilitatea, produce lead-uri, creează încredere, conduce spre conversii cu efort minim.

## 15.2 Inputuri
Brand Memory, strategie activă, buget, performance history, user preferences, platform rules, faza brandului.

## 15.3 Mix conținut (pilonii)
4 piloni: Educație (40%), Brand & emoție (30%), Dovadă socială (20%), Vânzare (10%). Ajustabili per industrie/scop.

## 15.4 Generarea ideilor
- Funnel: TOFU (50%), MOFU (30%), BOFU (20%). Ajustează brand nou vs matur.
- Matrice pilon vs funnel pentru idei.
- Pentru fiecare slot se generează 3–5 idei, se punctează, se alege cea mai bună (>70).

## 15.5 Calendar & timing
Reguli: nu 3 postări de vânzare la rând, alternează platformele, distribuție uniformă. Pattern săptămânal + ora postării (heatmap orar per platformă).

## 15.6 Platform-specific tuning
Adaptare per platformă (TikTok, IG, FB, YouTube, Email). Family of content.

## 15.7 Scor idei
Formula: 0.3 objective_fit + 0.2 persona_fit + 0.15 novelty + 0.1 complexity_inverse + 0.15 tone_fit + 0.1 predicted_performance.

## 15.8 Adaptare în timp
Performance_score 0–100; compară cu idea_score; creează pattern-uri; 10–20% conținut experimental.

## 15.9 Brand nou vs matur
Mode Explorator (teste) vs Mode Exploit (optimizare + 10–20% experiment).

## 15.10 Pseudo-cod developer
Descrie input → pași (determinare volum, slots, retrieval, generare idei, scoring, calendarizare, salvare, evaluare) → output.

# Capitolul 16 — DM Automation Logic
## 16.1 Detectare evenimente
Follow, DM direct, story reply, comentariu, like, click, formulare. Event trimis la DM Processor.

## 16.2 Identificare lead
Match handle/platform; dacă nu există → creează lead (stadiu New).

## 16.3 Clasificare intenție
Clasificatori: intenție, ton, tip lead, nivel funnel.

## 16.4 Alegerea flow-ului
În funcție de industrie, scop, intenție, tip lead, ton. Flow-uri: interes general, preț, produs specific, distribuitori, colaborare, VIP, after-comment, follow-back, client revenit, probleme, nurturing, vânzare directă.

## 16.5 Mesaj inițial
Respectă ton brand, scurt, adaptat platformă, întrebare deschisă, fără vânzare directă, trimis rapid.

## 16.6 Logica conversației
Branch-uri (A interesat, B indecis, C rece, D foarte interesat, E problematic). Fiecare are acțiuni specifice.

## 16.7 Reguli micro
Adaptare industrie/ton/personalitate user, mesaje scurte, întrebări deschise, focus pe apropiere.

## 16.8 Stop criteria
Când leadul cere om, întrebări complexe, devine agresiv, 5–7 mesaje, nu răspunde 24–72h etc. Notifică user.

## 16.9 Nurturing flow
Value drop + mesaj final. Lead mutat Warm/Cold.

## 16.10 Lead summary
După închidere → rezumat (context, interese, ce a mers) → vector DB.

## 16.11 Exemple flow industrie
Suc de mere (distribuitori), imobiliare, fitness.

## 16.12 Pseudo-cod backend
Descrie pipeline (event → identify lead → classify → select flow → generate message → send/update score → branch → stop → summary).

---

# Propuneri de module suplimentare
1. **Content Studio Intern** — studio vizual automat cu template-uri video, generare automată de variante, identitate vizuală coerentă, integrare AI video (Veo, Runway, Pika). Scalabil pentru sute/mii clienți.
2. **Brand DNA Builder** — modul de definire identitate vizuală/textuală (culori, fonturi, ton extins, arhetip, paletă emoții, stil foto, moodboard generat automat). Devine baza creativă.
3. **Content Experimentation Engine** — testare A/B automată (hook-uri, descrieri, CTA, thumbnail). Varianta A rulează 1 oră, se compară și se optimizează.
4. **Real-Time Trend Radar** — detectează trenduri TikTok/IG/YouTube în timp real, generează idei potrivite, notifică userul.
5. **Outreach Automation** — contactare automată parteneri/distribuitori/magazine. Extinde DM automation spre sales/outreach.
6. **Revenue Simulator** — modul ce estimează impactul schimbării volumului de postări/buget, planifică resurse pentru obiective (ex. 10 distribuitori).
7. **Brand Academy (AI Native)** — lecții personalizate, ghiduri, explicații „de ce”, crește retenția userului.

## Elemente de păstrat
- flow onboarding
- descoperirea industriei
- personalizare profundă
- DM automation la nivel intenție
- sistem memorie
- structură strategie (piloni/funnel/platforme)
- vibe poetic de claritate
- calendar respirabil

## Optimizări ușoare
- Calendar cu heatmap „zone roșii/zone verzi”
- DM UI cu timeline teatral
- Integrări mai vizuale
- Raportări cu versiune emoțională

## Propunere avansată
- **Creator Graph**: găsește creatori UGC potriviți, contactează, negociază, trimite brief, importă materiale. Monetizabil pentru planuri premium și diferențiere totală.
