# MVPeople Opportunity Intelligence — Zielarchitektur (Entwurf zur Freigabe)

Status: **Entwurf, nicht implementiert.** Fasst zusammen, was bereits gebaut ist (Layer 1 und 3 grösstenteils, Teile von Layer 4/5), und was neu hinzukommt (v.a. Layer 2 — Trend Intelligence — und das geschärfte Opportunity-Output-Schema in Layer 5). Keine Datenbank, Property oder Automatisierung wird durch dieses Dokument verändert.

**Selbstverständnis (Korrektur, seit dieser Runde):** Der Agent ist kein Content-Ideen-Agent und kein News-Matching-Agent, sondern ein **Opportunity Intelligence Layer** für MVPeople. Zweck: externe Veränderungen erkennen und prüfen, ob daraus für einen konkreten Partner eine relevante Handlung, Entscheidung, Information, Beziehung oder außergewöhnliche Positionierungsmöglichkeit entsteht — Content ist eine von vier möglichen Konsequenzen, nicht die Standardannahme.

---

## Layer 1 — External Signal Layer

**Zweck:** Externe Welt partnerunabhängig beobachten, einzelne Ereignisse/Erkenntnisse qualitätsgeprüft erfassen — die Rohdaten-Basis für alles Weitere.

**Input:** 8 Research Radars (Level A, komplett partnerunabhängig) + Portfolio Topic Radar (Level B, entpersonalisierte Themen aus dem Gesamtportfolio), je in drei Zeitfenstern (Reactive/Momentum/Structural).

**Verarbeitung:** Signal-Qualitätscheck (Aktualität, Neuigkeitswert, Quellenqualität, Momentum, Überraschungswert) als Gatekeeper vor jedem weiteren Schritt; Faktenprüfung (bestätigt/Gerücht/Kommentar/Spekulation); Deduplication (mehrere Berichte zum selben Ereignis = ein Signal).

**Output:** ein qualitätsgeprüftes External Signal mit Domain, Signal Type, Signal Angle, Time Horizon, Source/Source Date, Signal Strength Score.

**Notion-DB:** External Signals (bestehend, `collection://380f828e-5102-4593-9810-9e23817cb1f3`) — bereits mit Time Horizon, Signal Type/Angle, Partner-Relation, Match Type, Partner Question, Next Best Action ausgestattet.

**Neue Property (einzige Ergänzung):** `Trend` — Relation zur neuen Trend-Intelligence-DB (Layer 2), damit ein Signal einem oder mehreren Trends zugeordnet werden kann.

**Datenfluss:** → Layer 2 (jedes neue Signal wird zuerst gegen bestehende Trends geprüft) und parallel → Layer 4 (Einzelsignal-Matching gegen Partner-Profile läuft unabhängig vom Trend-Status weiter).

---

## Layer 2 — Trend Intelligence Layer (NEU)

**Zweck:** verhindert, dass dieselbe strukturelle Entwicklung jeden Tag neu "entdeckt" wird. Trends bekommen ein Gedächtnis und einen Lifecycle statt bei jedem Lauf bei null anzufangen.

**Input:** jedes neue External Signal aus Layer 1.

**Verarbeitung:**
1. **Matching gegen bestehende Trends:** gehört das Signal mechanistisch (nicht nur thematisch oberflächlich) zu einem bereits erfassten Trend?
2. **Wenn ja:** bestehenden Trend aktualisieren (Last Updated, Signal-Anzahl, ggf. Strength neu bewerten) — **kein** neuer Trend-Eintrag.
3. **Materialitäts-Check:** hat dieses neue Signal den Trend materiell verändert (deutlich stärkere Evidenz, neue Branche/Liga/Region, erstmalige institutionelle Adoption, regulatorische Veränderung, neue wirtschaftliche Dimension, direkte Verbindung zu einem aktiven Partner, neue zeitkritische Konsequenz)? Nur dann darf daraus eine neue oder aktualisierte Opportunity entstehen (siehe Layer 5, Dedup-Regel).
4. **Wenn kein bestehender Trend passt** UND mindestens zwei unabhängige, glaubwürdige Signale denselben Mechanismus stützen: neuen Trend mit Status `Emerging` anlegen. Ein Trend aus nur einem Signal oder aus mehreren Berichten über dasselbe Ereignis wird **nicht** angelegt.
5. **Lifecycle-Pflege:** `Emerging` (2 Signale) → `Confirmed` (3+ Signale oder erste bestätigte Partner-Relevanz) → `Accelerating` (mehrere neue Signale in kurzer Zeit, Momentum steigt) → `Stable` (weiter relevant, aber kein neues Signal seit mehreren Wochen) → `Declining`/`Closed` (kein Momentum mehr, Trend hat sich erledigt oder ist voll eingepreist).

**Output:** ein Trend-Eintrag mit vollständigem Datensatz, verknüpft mit allen zugehörigen Signalen.

**Notion-DB:** **NEU — "Trend Intelligence"**, eigene Datenbank unter derselben "Daily check in - Opportunities"-Seite. Begründung für die Ausnahme von "keine neuen Datenbanken": ein Trend ist strukturell weder ein Signal noch eine Opportunity — er lebt über Wochen, hat einen eigenen Lifecycle-Status, eine Many-to-Many-Beziehung zu Signalen und potenziell mehreren Partnern gleichzeitig. Das passt in kein bestehendes Objekt, ohne es zu verbiegen.

**Properties:**
| Feld | Typ |
|---|---|
| Trend Name | Title |
| Trend Description | Text |
| First Detected | Date |
| Last Updated | Date |
| Lifecycle Status | Select: Emerging / Confirmed / Accelerating / Stable / Declining / Closed |
| Strength | Select: Low / Medium / High |
| Anzahl unabhängiger Signale | Rollup (Count) aus Signal-Relation |
| Domains | Multi-Select (geteilt mit External Signals) |
| Betroffene aktive Partner | Relation zu Partner PR Profiles |
| Partner Relevance | Text (pro Partner kurz warum) |
| Zugehörige Signale | Relation zu External Signals (dual mit `Trend` aus Layer 1) |
| Letzte erzeugte Opportunity | Relation zu Qualified Opportunities |
| Letzte MVPeople Action | Text + Date |

**Datenfluss:** ← Layer 1 (neue Signale koppeln an). → Layer 4 (sowohl einzelne Signale als auch ganze Trends werden gegen Partner-Profile gematcht — ein Trend kann eine stärkere Opportunity erzeugen als ein Einzelsignal, siehe Shadow-Run-Beispiele Azzouzi/Rangnick).

---

## Layer 3 — Partner Knowledge Layer

**Zweck:** bestätigtes internes Partnerwissen als Matching-**Filter** — niemals als Ideenquelle.

**Input:** Core Positioning, Current Situation, Aktuelle Prioritäten (Ranking), Opportunity Fields + Opportunity Fields Evidence, Meetings/Persönlichkeitsanalyse, Content-Historie/bestehende Creativity-Einträge, Partner Status (Active-Filter), Nächstes Meeting.

**Verarbeitung:** bereits etabliert — Felder progressiv aktualisieren, wenn ein Partner ohnehin bearbeitet wird (neues Meeting, neue Erkenntnis), kein täglicher Pflicht-Abgleich aller 14 aktiven Partner.

**Output:** das Partner Opportunity Profile (destillierte Opportunity Fields) plus Priorisierungssignale (Current Situation, Nächstes Meeting) für die Matching-Tiefe.

**Notion-DB:** Partner PR Profiles (bestehend, geteilt mit `pr-scan`, `collection://365179bc-d750-4d4d-b4d5-08ac85b66b8d`).

**Neue Properties:** keine — Opportunity Fields, Opportunity Fields Evidence, Unterrepräsentierte Opportunity Fields (30d), Letzter Gap-Check, Nächstes Meeting und Partner Status sind bereits vorhanden.

**Datenfluss:** → Layer 4 (liefert den Filter). ← Weekly Gap Analysis (aktualisiert Unterrepräsentierte Felder, siehe SKILL.md).

---

## Layer 4 — Matching & Reasoning Layer

**Zweck:** entscheidet, was aus einem Signal oder Trend für einen Partner wird — inklusive der neuen Pflicht-Prüfreihenfolge und der geschärften Output-Klassen.

**Input:** External Signal ODER Trend (Layer 1/2) × Partner Opportunity Profile (Layer 3).

**Verarbeitung:**
1. Standalone Idea Test + Unique Partner Contribution Test (bestehend, unverändert).
2. Direct vs. Analogical Match (bestehend, unverändert).
3. **Value-Type-Prüfreihenfolge (NEU, zwingende Reihenfolge, Content ist nie Default):**
   `1. Strategic/Business → 2. Network/Relationship → 3. Knowledge/Advisory → 4. Creative/Positioning`
   Leitfrage zuerst: *"Wenn wir keine Social-Media-Kanäle und keine Pressearbeit hätten — wäre diese Information für den Partner trotzdem wertvoll?"* Erst wenn Strategic/Network/Knowledge ausscheiden, wird Creative/Content geprüft.
4. Evidence-Klassifizierung pro Aussage: External Fact / Partner Evidence / Derived Insight / Creative Hypothesis / Unknown.
5. **Output-Klassifikation (geschärft, seit dieser Runde):**
   - **ACT NOW** — unmittelbar ausführbare, ausreichend validierte Opportunity.
   - **STRATEGIC** — die externe Entwicklung kann eine konkrete **aktuelle** Entscheidung, Verhandlung, Initiative, Investition, Karriereoption oder ein laufendes Projekt beeinflussen (Referenzbeispiel: Arnold/Athlete Equity — laufendes Motorsport-Projekt, Trend betrifft mögliche Deal-Struktur, zeitkritisch).
   - **KNOWLEDGE/ADVISORY** (neu) — relevante Entwicklung, die MVPeople dem Partner aktiv mitteilen sollte, obwohl aktuell keine konkrete Entscheidung/Initiative dadurch verändert wird (Referenzbeispiel: Dorawa/Rule42 — relevant und wissenswert fürs Geschäftsfeld, aber keine dokumentierte laufende Initiative betroffen).
   - **ASK PARTNER** — eine fehlende Partnerinformation entscheidet darüber, ob die Verbindung überhaupt existiert (nicht: ob sie schon ausformuliert ist).
   - **NO ACTION** — interessant, aber aktuell kein ausreichend relevanter Mehrwert.
6. **Deduplication:** vor jeder neuen Opportunity prüfen — ist das eine wirklich neue Handlungsmöglichkeit, oder nur neue Evidenz für eine bereits bekannte Opportunity/einen bekannten Trend? Neue Evidenz → bestehende Opportunity aktualisieren. Neue Konsequenz → neue Opportunity erlaubt.

**Output:** klassifiziertes Ergebnis mit vollständigem Reasoning-Trail (What Changed / Why This Partner / Why Now / So What / Value Type / Confidence / Risk).

**Notion-DB:** keine eigene — reine Verarbeitungslogik im Skill, liest Layer 1-3, schreibt nach Layer 5.

**Datenfluss:** ← Layer 1, 2, 3. → Layer 5 nur bei ACT NOW / STRATEGIC / KNOWLEDGE-ADVISORY / ASK PARTNER. NO ACTION erzeugt keinen Opportunity-Eintrag, nur den `Partner Match Status` auf dem Signal selbst (bzw. bleibt No Match/Under Review).

---

## Layer 5 — Opportunity Layer

**Zweck:** die tatsächlich verwertbaren Ergebnisse persistent und für MVPeople in ca. 30 Sekunden erfassbar ablegen.

**Input:** klassifizierte Ergebnisse aus Layer 4 (ACT NOW / STRATEGIC / KNOWLEDGE-ADVISORY / ASK PARTNER).

**Verarbeitung:** Dedup-Check (siehe Layer 4), Feldausfüllung nach dem neuen, geschärften Output-Schema.

**Output:** ein Qualified-Opportunity-Eintrag, Status bleibt `New` (MVPeople-Freigabe-Gate unverändert zwingend).

**Notion-DB:** Qualified Opportunities (bestehend, `collection://eab8b976-d9ef-47c3-a797-9760f78c994c`) — Feldschema wird angepasst, keine neue Datenbank.

**Neue/geänderte Properties:**
| Feld | Typ | Ersetzt/ergänzt |
|---|---|---|
| `Output-Klasse` | Select: ACT NOW / STRATEGIC / KNOWLEDGE-ADVISORY / ASK PARTNER | neu, zentrale Einordnung statt reiner Score-Bänder |
| `What Changed` | Text | = External Fact kompakt, ersetzt sinngemäß `Signal` in der Kurzansicht |
| `So What` | Text | neu — expliziter Konsequenz-Satz, Pflichtfeld |
| `Value Type` | Select: Strategic / Network / Knowledge / Creative | neu, ersetzt/ergänzt `Opportunity Type` in der Kernlogik |
| `Confidence` | Select: Explicit / Strongly Inferred / Hypothesis | Umbenennung/Erweiterung von `Evidence Level` |
| `Trend` | Relation zu Trend Intelligence | neu, optional — nur befüllt, wenn die Opportunity aus einem Cluster statt einem Einzelsignal entstand |

Bestehende Felder bleiben: `Why This Partner`, `Timing`/Why Now, `Next Best Action`, `Risk / Open Question`, `Partner Question`, `Urgency`, `Owner`, `Status`, `Source`/`Source Date`.

**Datenfluss:** ← Layer 4. → Layer 6 (MVPeople Review, Routing, Feedback).

---

## Layer 6 — Action / Feedback Layer

**Zweck:** menschliche Freigabe, Routing in die operative Arbeit, Rückkopplung ins System.

**Input:** Qualified-Opportunity-Einträge (Layer 5) + MVPeople-Entscheidung (Approve/Reject/Feedback).

**Verarbeitung:** bestehendes Owner-Routing (abgeleitet aus `Next Best Action`-Inhalt), bestehender Creativity-DB-Routing-Mechanismus (`An Creativity senden`-Checkbox), Erfassung von `MVPeople Feedback`.

**Output:** finale Handlung (Content/PR/Partnergespräch/Wissen geteilt/keine Aktion) + Feedback zurück ins System.

**Notion-DB:** Qualified Opportunities (`Status`, `Owner`, `MVPeople Feedback`, `An Creativity senden`/`In Creativity übernommen`/`Creativity-Eintrag`) — alles bereits vorhanden, keine neuen Properties nötig.

**Datenfluss:** ← Layer 5. Feedback fließt konzeptionell zurück in Layer 4 (schärft künftige Bewertungen desselben Partners/Trends), **niemals automatisiert als Lern-Loop** — nur als Kontext, den du oder ich beim nächsten Mal bewusst berücksichtigen, kein Autolearning ohne menschliche Zwischenstation.

---

## Gesamtfluss (Zusammenfassung)

```
Layer 1 External Signal ──┬─→ Layer 2 Trend Intelligence (Matching, Lifecycle, Materialitäts-Check)
                           │         │
                           ↓         ↓
                    Layer 4 Matching & Reasoning ←── Layer 3 Partner Knowledge
                           │
                           ↓ (nur ACT NOW / STRATEGIC / KNOWLEDGE-ADVISORY / ASK PARTNER)
                    Layer 5 Opportunity
                           │
                           ↓
                    Layer 6 Action / Feedback ──→ (zurück zu Layer 4 als Kontext)
```

## Was schon existiert vs. was neu ist

**Bereits implementiert (frühere Freigabe):** Layer 1 komplett, Layer 3 komplett, Teile von Layer 4 (Direct/Analogical, Standalone/Unique-Contribution-Tests), Teile von Layer 5 (Grundschema Qualified Opportunities), Layer 6 komplett (Routing, Feedback-Feld, Creativity-Mechanismus).

**Neu in diesem Konzept:** die komplette **Trend Intelligence Layer (2)** als einzige neue Datenbank, die **Value-Type-Prüfreihenfolge** und **KNOWLEDGE/ADVISORY-Klasse** in Layer 4, das **geschärfte Output-Schema** (What Changed/So What/Value Type/Confidence) in Layer 5, sowie die **Dedup-gegen-Trend-Regel**, die verhindert, dass bekannte Trends täglich neue Opportunities erzeugen.

## Offene Entscheidung für Michael

Die Trend-Intelligence-DB ist die einzige tatsächlich neue Datenbank in diesem gesamten Ausbau. Alles andere sind Feldergänzungen an den drei bestehenden. Bitte explizit bestätigen, ob diese eine Ausnahme von "keine neuen Datenbanken" für dich in Ordnung ist — Alternative wäre, den Trend-Lifecycle als Text-Block/Property auf bestehenden Objekten zu simulieren, was aber die Kernanforderung (persistentes Gedächtnis mit Lifecycle und Many-to-Many-Signalbezug) strukturell schlechter abbilden würde.
