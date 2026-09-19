# Edge Functions

Hier liegt der Quelltext der Supabase Edge Functions dieses Projekts. Bisher
existierte er nur im Supabase-Dashboard, es gab also keinen Stand, gegen den
man eine Aenderung haette vergleichen koennen.

**Achtung: dieser Ordner deployt nicht von selbst.** Ein Push hierher aendert
nichts an der laufenden Funktion. Ausgerollt wird ueber das Supabase-Dashboard
oder die Supabase-CLI. Wer hier etwas aendert, muss es getrennt ausrollen --
und wer im Dashboard etwas aendert, sollte es hier nachtragen.

Projekt: `ivvrfnsuoufymcwtsycp`

| Funktion | Zweck | verify_jwt |
|---|---|---|
| `generate-cards` | Dokumenttext -> Karteikarten (Gemini) | false, die Funktion prueft das Session-Token selbst |

`verify_jwt` steht bewusst auf false: sonst scheitert schon der CORS-Preflight,
weil der Browser ihn ohne Token schickt. Die Anmeldepruefung passiert in der
Funktion, anonyme Aufrufe bekommen 401, bevor ein Gemini-Aufruf entsteht.
