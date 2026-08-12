# Partnership Intelligence Agent — MVPeople

Agent zur Identifikation, Bewertung und Vorbereitung von Brand-Partnerschaften für MVPeople-Athlet:innen. Getrennt vom bestehenden PR-Intelligence-Setup (`Development/.claude/skills/pr-scan`, Podchaser-Integration) — dieses hier ist ausschließlich für Partnership-/Brand-Deal-Akquise.

**Prinzip:** Diese Agent-Logik ist athletenunabhängig und wiederverwendbar. Die konkreten Arbeitsergebnisse (Partnership-Profile, Brand Radars, Deep Dives) gehören in den jeweiligen Athleten-Ordner unter `Desktop/claude/[Name]/`, nicht hierher.

## Status je Athlet (Stand 10.08.2026)

| Athlet | Notion-Workspace | Phase-1 (Partnership-Profil) | Phase 2 (Brand Radar) | Kontakte via Cognism |
|---|---|---|---|---|
| Nicolas Seiwald | "Team Nici" | ✅ fertig, freigegeben | ✅ fertig (9 Top/8 Developing/10 Watchlist) | ✅ Hornbach (3 Kontakte in Notion) |
| Maximilian Arnold | eigener Workspace | ✅ fertig, wartet auf Freigabe | offen | offen |
| Haris Tabaković | eigener Workspace | offen — **Vorsicht:** "Partner PR Profiles"-Stub enthält fälschlich von Nicolas' Notizen abgeleitete Daten, vor Nutzung die echte Persönlichkeitsanalyse als Quelle nehmen | offen | offen |
| Ralf Rangnick | eigener Workspace | offen, aber Persönlichkeitsanalyse bereits vollständig vorhanden (ÖFB-Teamchef) | offen | offen |

Jeder Athlet hat in Notion dieselbe Grundstruktur: Übersicht (Dokumente), Social Media, Collabs, PR, Meetings, Creativity. Bei Nicolas zusätzlich vier Strategiedokumente (Brand DNA, Strategische Leitplanken, Cluster-Einteilung, Persönlichkeitsprofil) als PDFs — bei den anderen dreien existieren diese vier Dokumente noch **nicht**, nur die Persönlichkeitsanalyse (entspricht in etwa Nicolas' Cluster-Einteilung).

## Workflow (Phasen)

1. **Partnership-Profil** — Notion-Recherche (Persönlichkeitsanalyse, Social-Media-Log, bestehende Collabs/Meetings, Klub-/Verbandssponsoren via öffentliche Recherche) → 5–8 Partnership-Territorien, Ausschlüsse/Konflikte, offene Fragen. Muss von MVPeople freigegeben werden, bevor Brand-Recherche startet.
2. **Brand Radar** — Konkrete Brand-Kandidaten je Territorium recherchieren (Trigger, Partnership-Affinität, Konflikte), scoren, in Top/Developing/Watchlist einordnen. Alle Brands landen als "Idee" in der Collabs-Datenbank des jeweiligen Athleten.
3. **Deep Dive** — Für priorisierte Brands vollständiges Opportunity-Dossier (17-Punkte-Struktur).
4. **Kontaktsuche (Cognism)** — Erst nach expliziter Freigabe pro Brand. Siehe Abschnitt unten.

## Cognism-API — technische Referenz

Kein offizieller MCP-Connector vorhanden; Zugriff läuft über direkte REST-Calls (curl/Bash). Die Doku-Domain `documentation.cognism.com` ist von dieser Umgebung aus nicht per DNS erreichbar — folgende Details wurden durch Recherche + Trial-and-Error ermittelt und funktionieren nachweislich (Stand 10.08.2026):

**Base URL:** `https://app.cognism.com/api/search/...` (NICHT `api.cognism.com` — das ist nur die Marketing-Domain hinter Cloudflare-Bot-Schutz; NICHT `platform.cognism.com` — das ist die Frontend-SPA)

**Endpunkte:**
- `POST /api/search/contact/search`
- `POST /api/search/contact/redeem`
- `POST /api/search/contact/enrich`
- `POST /api/search/account/search`
- `POST /api/search/account/redeem`
- `POST /api/search/account/enrich`

**Auth:** Header `Authorization: Bearer {API_KEY}`. API-Key wird in Cognism unter Profile Settings erzeugt, hat 6 Monate TTL. **Ohne von Cognism-Support gesetzte "Entitlements" liefert die API nur `{"msg":"You have no entitlement set. Please contact CSM."}`** — das ist ein einmaliger Freischaltschritt bei Cognism, nicht selbst konfigurierbar.

**Wichtige Stolperfallen:**
- `page` und `pageSize` gehören als **Query-Parameter** in die URL (`?page=1&pageSize=20`), NICHT in den JSON-Body — sonst `{"msg":"Search request contains unknown field"}`.
- Job-Titel-Feld heißt `jobTitles` (Plural, Array), nicht `jobTitle`.
- Firmenname muss verschachtelt unter `account.names` (Array) stehen, nicht als eigenes Top-Level-Feld `accountName`.
- Ein Search-Call ohne erkannte Filterfelder liefert `{"msg":"Empty search request"}`.
- Beispiel-Request-Body, der nachweislich funktioniert:
```json
{
  "jobTitles": ["Marketing Director", "Head of Marketing", "Head of Brand", "Head of Sponsoring"],
  "account": { "names": ["Hornbach"] }
}
```
- `Search`/`Preview` verbraucht laut Doku kein echtes Budget (nur "Preview Limit", sehr hohes Kontingent), **`Redeem` verbraucht echte Credits** (Kontostand einsehbar über Response-Header `x-credits-limit-remaining`).

**Verbindliche Prozessregel (von Mitch bestätigt, 10.08.2026):**
1. Search/Preview darf frei laufen.
2. **Vor jedem Redeem-Call immer erst die Kandidatenliste zeigen und explizite Freigabe einholen** — nicht automatisch redeemen.
3. Nach Freigabe: redeemen, dann Ergebnisse (Name, Position, Unternehmen, Region, E-Mail + Qualitätsflag, LinkedIn, Contact Fit Score, Begründung, empfohlener Zugangsweg, Quelle, Datum) direkt in die Notion-Collabs-Seite der jeweiligen Brand eintragen — ohne dass extra danach gefragt werden muss.

**Bekannter Stolperstein bei Notion-Textinserts:** Beim Einfügen von mehrzeiligem Content über `insert_content`/`update_content` müssen echte Zeilenumbrüche verwendet werden. Literale `\n`-Zeichenketten wurden einmal fälschlich als Text übernommen (Notion strippt das Backslash, übrig bleibt ein nacktes "n" im Fließtext, zusätzlich wurden dadurch zwei LinkedIn-URLs mit einem angehängten "n-" korrumpiert). Vor dem Absenden Content auf echte Newlines prüfen.

## Outreach-E-Mail-Stil (Mitch, bestätigt 10.08.2026)

Kaltakquise-Mails **nicht** im formellen Dossier-Ton schreiben, sondern:
1. Locker starten, "du" explizit anbieten ("ich hoffe es geht dir gut und das 'du' ist okay für dich").
2. Kurzer, generischer Ein-Satz-Intro zu MVPeople ("wir unterstützen Sportler, Trainer und Sportfunktionäre im Personal Branding"), bevor der konkrete Athlet genannt wird.
3. Konkrete, echte Anekdote als Aufhänger statt "wir haben eure Marke recherchiert" — wenn Mitch eine reale Situation nennt (z. B. "Wir saßen gestern im Trainingslager zusammen..."), diese nutzen; sonst faktenbasiert bleiben und NICHT erfinden.
4. Einfach sagen, dass der Athlet selbst um den Kontakt gebeten hat, ohne es zu überbegründen.
5. Offene, unverbindliche Formulierung statt kalkuliert wirkender Sätze ("Vielleicht ergibt sich ja in irgendeiner Form eine Zusammenarbeit").
6. Warmer, kurzer Sign-off: Vorname + Stadt ("Viele Grüße aus München / Mitch"), kein voller Signatur-Block.

## Wer ist wer (aus Notion "MVPeople PR Intelligence" + Meetings-Kontext)

- **Mitch** — arbeitet seit 3 Jahren als Head of Media bei einem SailGP-Team (neben MVPeople) → direkter warmer Zugang zu Sailing/Lifestyle/Nachhaltigkeits-Content, aktuell genutzt für Maximilian Arnold.
- **Michael Klement** (User dieser Sessions) — MVPeople, Partnership Management.
- Laut Notion betreut MVPeople mindestens: Nicolas Seiwald, Maximilian Arnold, Haris Tabaković, Ralf Rangnick, und laut einer Meeting-Notiz zusätzlich "Rani Kshaka" (noch nicht recherchiert).

## Nächste sinnvolle Schritte

1. Maximilian-Arnold-Profil intern freigeben, dann Brand Radar (Territorium 1 Family Health und Territorium 2 Sailing haben bereits warme Anknüpfungspunkte).
2. Haris Tabakovićs "Do Not Pitch"-Datenfehler in der PR-Intelligence-Datenbank korrigieren, bevor mit ihm gearbeitet wird.
3. Ralf Rangnick als dritten Kandidaten angehen — Persönlichkeitsanalyse ist bereits vollständig, ÖFB-Sponsorenkonfliktliste ist aus Nicolas' Recherche bereits vorhanden und direkt wiederverwendbar.
