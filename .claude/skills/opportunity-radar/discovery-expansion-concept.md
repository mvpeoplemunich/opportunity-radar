# External Discovery Expansion — Konzept (Entwurf zur Freigabe)

Status: **Entwurf, nicht implementiert.** Architektur (External Signals → Qualified Opportunities, Partner PR Profiles), Qualitätslogik (No Match/Potential Match/Qualified Opportunity), Scoring-Gates und alle bestehenden Guardrails bleiben unverändert. Dieses Dokument erweitert ausschließlich die **Discovery-Tiefe** und das **Matching-Vokabular**, nicht die Qualitätsschwellen.

---

## 1. Zweistufige Discovery-Logik

```
LEVEL A — Open World Discovery (partnerunabhaengig, wie bisher)
   8 Radars, keine Partnerdaten im Zugriff
        +
LEVEL B — Portfolio Topic Discovery (themenbasiert, weiterhin partnerunabhaengig in der Suche selbst)
   Entpersonalisierte Themenraum-Liste, aggregiert aus allen aktiven Partnerprofilen
        ↓
   Kombinierter Query-Pool fuer den taeglichen Lauf
```

Level A bleibt exakt wie bisher: acht Radars, keine Partnerkenntnis fließt in die Suchanfragen ein.

Level B ist neu: Eine **entpersonalisierte** Themenraum-Liste (siehe Punkt 2) fließt zusätzlich in die Suchanfragen ein — aber immer als abstraktes Thema ("Leadership under Pressure"), nie mit Partnername verknüpft. Der Unterschied zu Level A ist nur die *Herkunft* der Suchrichtung (aus dem Portfolio abgeleitet statt aus den 8 Radaren selbst), nicht der *Grad an Partnerbezug* in der Anfrage — beide bleiben strikt partnerunabhängig formuliert. Erst nach dem Fund (Stufe Partner-Matching) wird geprüft, ob ein Partner passt.

**Wo das lebt:** Kein neues Notion-Objekt nötig. Die Themenraum-Liste lebt als einfacher Block auf der "Daily check in - Opportunities"-Seite (ein Aufzählungs-Textblock, den ich periodisch aktualisiere) — kein eigenes Suchprofil pro Partner, kein Datenbankeintrag.

---

## 2. Beispiel: Portfolio Topic Radar (Level B)

Abgeleitet durch Aggregation der `Opportunity Fields` (siehe Punkt 3) über alle 14 aktiven Partner, dedupliziert und verallgemeinert:

```
Leadership under Pressure · Intercultural Leadership · Team Building · Player/Talent Development
Future of Coaching · Career Transitions · Athlete Entrepreneurship · Personal Branding
Club Management · Sports Business · Football Innovation · Technology in Sports
Mental Performance · Generation Z · Communication · Society & Sport · Nachwuchsförderung
Medien & Sport · Sponsoring · Creator Economy
```

Diese Liste wird **nicht** 1:1 aus Michaels Beispielliste übernommen, sondern nur mit Themen befüllt, die tatsächlich durch mindestens ein `Opportunity Field` eines aktiven Partners gedeckt sind — sonst entsteht ein Suchprofil für Partner, die wir gar nicht haben. Aktualisierung: bei jeder wöchentlichen Gap Analysis (Punkt 7) mit-geprüft, nicht täglich neu erfunden.

---

## 3. Partner Opportunity Profile — Struktur

Kein neues Notion-Objekt, sondern **zwei neue Felder auf der bestehenden Partner-PR-Profiles-DB** (geteilt mit `pr-scan`):

| Feld | Typ | Inhalt |
|---|---|---|
| `Opportunity Fields` | Multi-Select | z.B. `Leadership`, `Nachwuchsentwicklung`, `Team Building`, `International Experience`, `Business`, `Performance` — nur was durch vorhandene Evidence gedeckt ist |
| `Opportunity Fields Evidence` | Text | Kurzbeleg pro Feld, z.B. "Leadership: Core Positioning 'Fußballprofessor', ÖFB-Aufbauarbeit" |

Beispiel Thomas Reis:
```
Opportunity Fields: International Experience, Team Building, Leadership
Opportunity Fields Evidence:
  International Experience: Trainerstationen in Deutschland UND Türkei (Core Positioning + Aktuelle Rolle)
  Team Building: "Malocher-Fußball", Führung durch Vertrauen statt Kontrolle (Core Positioning)
  Leadership: medial zurückhaltend, aber dokumentierte Führungsphilosophie (Core Positioning)
```

Nichts wird erfunden — nur destillierte, bereits vorhandene Profildaten in ein durchsuchbares Kurzformat gebracht. Aktualisierung: immer wenn ein Partnerprofil ohnehin bearbeitet wird (neues Meeting, neue Erkenntnis) — kein separater Pflegeaufwand.

---

## 4. Multi-Horizon-Recherchelogik

Neues Pflichtfeld **`Time Horizon`** (Select: `Reactive` / `Momentum` / `Structural`) auf External Signals.

| Horizon | Fenster | Fokus |
|---|---|---|
| Reactive | 0-72h | Breaking News, Personalien, Regeländerungen, kurzfristige Debatten |
| Momentum | 7-30 Tage | wachsende Trends, Studien, wiederkehrende Themen, neue Geschäftsmodelle |
| Structural | bis 90 Tage | hochwertige Reports, wissenschaftliche Erkenntnisse, strukturelle/gesellschaftliche Entwicklungen |

Jeder Lauf recherchiert **alle drei Fenster**, nicht nur Reactive — ein 45 Tage alter, hochwertiger Report kann laut Vorgabe wertvoller sein als News von heute. Die bestehende Aktualitätspflicht (Current Event max. 72h) bleibt für den Signal-Typ "Current Event" unverändert; `Time Horizon` ist eine zusätzliche, unabhängige Klassifizierung, kein Ersatz dafür.

---

## 5. Erweiterte Signaltypen

Michaels Liste hat ~24 Einzeltypen — als einzelnes Select-Feld mit 24 Optionen wird das in der Notion-UI unbenutzbar. Vorschlag: bestehendes `Signal Type` bleibt schlank (4-6 Kategorien), zusätzlich ein neues **`Signal Angle`** Multi-Select für die granulare Einordnung:

- **Signal Type** (Select, erweitert von 4 auf 6): `Current Event` · `Emerging Trend` · `Study/Research` · `Strong Statement/Debate` · `Business/Deal` · `Creative Format`
- **Signal Angle** (Multi-Select, granular, mehrere pro Signal möglich): `Surprising Statistic` · `Contrarian View` · `New Thesis` · `Interview Insight` · `Cross-Industry Case` · `Leadership Case` · `Sports Case` · `Behaviour Change` · `Regulation` · `Communication Mechanic` · `Campaign` · `Content Trend` · `Media Development` · `Technology` · `Business Model` · `Investment/Deal` · `Social Change`

Damit bleiben die Recherche-Leitfragen aus Michaels Vorgabe ("Welche neue Zahl verändert die Sicht auf ein Thema?" etc.) vollständig erhalten, ohne dass ein einzelnes Dropdown überladen wird. **Das ist ein Vorschlag, keine Festlegung — falls du die 24 Typen 1:1 als flache Liste willst, geht das auch, dann aber nur als Multi-Select ohne Kategorisierung.**

---

## 6. Direct Match vs. Analogical Match

Neue Felder direkt auf **External Signals** (nicht erst auf Qualified Opportunities, damit auch Potential Matches diese Einordnung tragen):

- `Partner` (Relation zu Partner PR Profiles, leer bis ein Kandidat gefunden ist)
- `Match Type` (Select: `Direct` / `Analogical`)
- `Partner Question` (Text, Pflicht bei Potential Match)
- `Next Best Action` (Text, Pflicht bei Potential Match und Qualified Opportunity)

**Direct Match**: Signal betrifft unmittelbar ein `Opportunity Field`, für das beim Partner Evidence existiert (Beispiel: Leadership-Studie ↔ Rangnicks dokumentierte Leadership-Positionierung).

**Analogical Match**: Signal stammt aus anderer Branche/Sportart, enthält aber einen übertragbaren Mechanismus. Pflicht bei Analogical Match: explizit benennen (a) welcher konkrete Mechanismus übertragbar ist, (b) warum genau dieser Partner eine glaubwürdige Verbindung dazu hat — reine Rollen-/Karriereweg-Ähnlichkeit reicht nicht (das war exakt der Azzouzi/F1-Fehler, den wir schon einmal zurückgewiesen haben). Analogical Matches werden beim Scoring strenger behandelt: der bestehende Differentiation-Gate (≥12/20) wird bei Analogical Matches faktisch zum Haupt-Hebel, da die Grundregel "abstrakte Ähnlichkeit reicht nicht" hier am häufigsten greift.

---

## 7. Knowledge Gap ≠ No Match — konkrete Notion-Abbildung

`Partner Match Status` auf External Signals wird erweitert:

`No Match` · `Under Review` · **`Potential Match`** (neu) · `Qualified Opportunity Created`

Ein **Potential Match ist ein angereicherter External-Signal-Eintrag** — keine eigene Seite, keine neue Datenbank. Er bekommt `Partner`, `Match Type`, `Partner Question`, `Next Best Action` befüllt und `Partner Match Status = Potential Match`. Erst wenn genug Evidence entsteht (z.B. nach einem Partnergespräch), wird daraus eine echte Seite in Qualified Opportunities — mit Verweis zurück auf das ursprüngliche Signal (bestehende `Source Signal`-Relation).

---

## 8. Weekly Partner Gap Analysis

Neuer wöchentlicher Analyseschritt (kein neuer DB-Typ): für jeden aktiven Partner werden dessen `Opportunity Fields` gegen alle External Signals der letzten 30 Tage abgeglichen (gefiltert auf `Partner Match Status IN (Potential Match, Qualified Opportunity Created)` mit diesem Partner). Felder ohne Treffer = unterrepräsentiert.

Ergebnis wird in zwei neuen, leichten Feldern auf Partner PR Profiles festgehalten:
- `Unterrepräsentierte Opportunity Fields (30d)` (Text)
- `Letzter Gap-Check` (Date)

Die nächste Discovery erhöht dann temporär die Rechercheintensität in den **entpersonalisierten** Themenräumen, die diesen Lücken entsprechen (z.B. "Youth Development", "Education") — nie mit Partnerbezug in der Suchanfrage selbst, wie in Michaels Vorgabe gefordert.

---

## 9. Dynamische Discovery-Gewichtung

Reine Prozesslogik im Skill, kein Notion-Feld nötig. Gewichtungsfaktoren: aktuelles externes Momentum (aus Signal Strength Scores der letzten Tage), Qualität bisheriger Signale pro Radar, Portfolio-Relevanz (Abgleich mit Opportunity Fields), unterrepräsentierte Felder aus der Gap Analysis, saisonale Sportereignisse, neue Reports.

**Pflicht-Gegengewicht gegen Filter Bubble**: ein fester Mindestanteil jedes Laufs (Vorschlag: mindestens 2 von 8 Radaren, rotierend) bleibt bewusst ungewichtet/explorativ, unabhängig von bisherigen Trefferquoten — sonst optimiert sich das System auf das, was bisher funktioniert hat, und verpasst neue Themen.

---

## 10. Partner Matching Priority

Berechnet aus bereits vorhandenen Feldern — kein neues Pflichtfeld nötig: `Aktuelle Prioritäten (Ranking)`, `Current Situation` (z.B. Sportlicher Erfolg, Medienphase, Jobsuche erhöhen Priorität), `Letztes Profil-Update`. Optional, falls gewünscht: ein einfaches `Nächstes Meeting`-Datumsfeld auf Partner PR Profiles würde die Priorisierung schärfen (bevorstehendes Gespräch = höhere Matching-Tiefe) — das ist der einzige echt neue Vorschlag hier, markiere ich als **optional**.

Wichtig, wie gefordert: höhere Priorität = tieferes/häufigeres Matching, **niemals** niedrigere Scoring-Schwellen.

---

## 11. Opportunity Types erweitern

Bestehende Multi-Select auf Qualified Opportunities (`Media, Content, Brand, Business, Speaking, Network, Positioning, Career, Knowledge, Watchlist`) wird um zwei Optionen ergänzt: **`Conversation`** (z.B. "im nächsten Partnermeeting ansprechen" — wertvoll auch ohne Content-Output) und **`Partnership`** (eigenständig von `Business`, für Kooperationen ohne direkten Investment-Charakter). `Speaking` bleibt, deckt Keynote/Panel weiterhin ab.

---

## 12. Discovery Health Metrics

**Kein neues Notion-Objekt** — alle Rohdaten dafür existieren bereits als Felder auf External Signals (`Domain`, `Time Horizon`, `Partner Match Status`, `Match Type`). Die Kennzahlen werden **on-demand per SQL-Aggregation** berechnet, nicht persistiert:

```sql
SELECT "Time Horizon", "Partner Match Status", COUNT(*) 
FROM External_Signals WHERE Date_Discovered >= <30 Tage> 
GROUP BY "Time Horizon", "Partner Match Status"
```

Daraus: Signal→Potential-Match-Rate, Signal→Qualified-Opportunity-Rate, Potential-Match→Qualified-Opportunity-Rate — als Diagnose-Report auf Zuruf oder im Rahmen der wöchentlichen Gap Analysis, nicht als tägliche Notion-Zeile. **Falls du eine historische Trendlinie über Wochen/Monate willst** (nicht nur Momentaufnahme), bräuchte es doch ein minimales wöchentliches Log — das würde ich erst bauen, wenn sich zeigt, dass die On-Demand-Abfrage nicht reicht.

---

## 13. MVPeople Feedback Loop

Neues Feld **`MVPeople Feedback`** (Select) auf Qualified Opportunities: `Strong` · `Interesting` · `Not Relevant` · `Too Generic` · `Too Constructed` · `Already Known` · `Wrong Partner` · `Wrong Timing` · `Need More Partner Knowledge`. Wird von MVPeople manuell gesetzt (wie `Status`), fließt in künftige Läufe als Kontext ein ("bei diesem Partner wurde zuletzt X als 'Too Constructed' zurückgewiesen — bei ähnlichen Analogical Matches besonders streng prüfen"), **nie** als Optimierung auf bereits erfolgreiche Muster, wie gefordert.

---

## 14. Morning Check-in (Format-Ergänzung)

Bleibt kuratiert. Neu: Potential Matches mit befüllter `Partner Question` erscheinen zusätzlich zu Qualified Opportunities, aber nur eine Auswahl (die stärksten, nicht alle) — Format:

```
🔥 [Score]/100 – [Partner] — Qualified Opportunity
...(wie bisher)...

❓ [Partner] — Potential Match
Extern: [was ist passiert]
Frage an Partner: [Partner Question]
Next Best Action: [z.B. "im nächsten Meeting ansprechen"]
```

External Signals ohne Match bleiben im System-Layer, tauchen im Check-in nicht auf.

---

## Vollständiges Funnel-Beispiel

```
LEVEL A/B DISCOVERY
→ Neue Studie: "Interkulturelle Führung bei Nationaltrainern in unterschiedlichen 
   Fußballkulturen" (Momentum, Study/Research, matcht den Portfolio-Topic 
   "Intercultural Leadership")

EXTERNAL SIGNAL
→ Angelegt in External Signals: Time Horizon=Momentum, Signal Type=Study/Research,
   Partner Match Status=Under Review

PARTNER MATCHING
→ Abgleich gegen alle aktiven Partner-Opportunity-Profiles
→ Thomas Reis: Opportunity Field "International Experience" (Evidence: Trainer-
   stationen Deutschland UND Türkei) — Match Type = Direct (kein Analogieschluss,
   es ist buchstäblich sein Erfahrungsfeld)
→ Aber: keine dokumentierte Meinung/Haltung von Reis zu interkultureller Führung 
   als Thema → Evidence Level = Unknown für die konkrete Haltung

KLASSIFIKATION
→ Potential Match (nicht No Match, nicht Qualified — Verbindung ist stark, 
   aber entscheidendes Partnerwissen fehlt)
→ Partner Match Status = Potential Match
→ Partner Question: "Würdest du deine Erfahrung als Trainer in zwei sehr 
   unterschiedlichen Fußballkulturen mit Bezug auf diese Studie öffentlich 
   oder intern einordnen?"
→ Next Best Action: "Im nächsten Partnergespräch ansprechen"

MVPEOPLE REVIEW
→ Erscheint im Morning Check-in unter "Potential Matches"
→ Partner Manager nimmt Frage ins nächste Meeting mit
→ MVPeople Feedback (falls gesetzt): z.B. "Interesting"

NÄCHSTER SCHRITT (falls Reis eine klare Haltung äußert)
→ Partnerinfo wird ins Profil übernommen, Evidence Level → Explicit
→ Signal wird zur echten Qualified-Opportunity-Seite hochgestuft, 
   Source Signal verweist zurück, Scoring erneut geprüft (Gates weiterhin 
   verbindlich, Partnerwissen ändert am Signal-Quality-Wert nichts)
```

---

## Zusammenfassung: Notion-Änderungen (falls freigegeben)

**Keine neue Datenbank.** Nur Feldergänzungen an drei bestehenden DBs:

| DB | Neue/geänderte Felder |
|---|---|
| External Signals | `Time Horizon` (neu), `Signal Angle` (neu, Multi-Select), `Partner` (neu, Relation), `Match Type` (neu), `Partner Question` (neu), `Next Best Action` (neu), `Signal Type` (erweitert), `Partner Match Status` (erweitert um "Potential Match") |
| Qualified Opportunities | `Time Horizon` (neu), `Match Type` (neu), `MVPeople Feedback` (neu), `Opportunity Type` (erweitert um Conversation/Partnership) |
| Partner PR Profiles | `Opportunity Fields` (neu), `Opportunity Fields Evidence` (neu), `Unterrepräsentierte Opportunity Fields (30d)` (neu), `Letzter Gap-Check` (neu), optional `Nächstes Meeting` |

Plus: Portfolio-Topic-Radar-Liste als Textblock auf der bestehenden "Daily check in - Opportunities"-Seite (kein neues Objekt).

**SKILL.md**: umfassende Erweiterung von Discovery-Abschnitt (Level A/B, Multi-Horizon, erweiterte Signaltypen, Cross-Industry-Verstärkung), Matching-Abschnitt (Direct/Analogical, Potential-Match-Handling), neue Abschnitte für Weekly Gap Analysis, Dynamic Weighting, Partner Matching Priority, Discovery Health Metrics, Feedback Loop, aktualisiertes Morning-Check-in-Format.

**Cloud-Routinen-Prompt**: keine Änderung nötig (verweist schon jetzt ausschließlich auf SKILL.md als Quelle der Wahrheit).

## Offene Fragen an Michael

1. Punkt 5 (Signaltypen): reicht die vorgeschlagene Zwei-Ebenen-Lösung (schlankes `Signal Type` + granulares `Signal Angle`), oder lieber alle ~24 Typen flach als ein Multi-Select?
2. Punkt 10: soll ich das optionale `Nächstes Meeting`-Datumsfeld mit aufnehmen?
3. Punkt 12: reicht die On-Demand-Berechnung der Health Metrics, oder von Anfang an ein wöchentliches Log für Trendverlauf?
