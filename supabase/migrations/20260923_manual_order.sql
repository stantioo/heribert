-- 23.09.2026 — Reihenfolge von Hand (Sets und Karten)
--
-- Die Reihenfolge steht in der Datenbank und gilt damit fuer alle, die den
-- Ordner sehen. Die gewaehlte SORTIERUNG (A-Z, neueste zuerst, ...) ist
-- dagegen Ansichtssache und liegt im localStorage des jeweiligen Browsers.

alter table public.sets  add column if not exists position integer;
alter table public.cards add column if not exists position integer;

with o as (
  select id, (row_number() over (partition by coalesce(folder_id,'__root') order by created_at, id) - 1)::int as pos
    from public.sets)
update public.sets s set position = o.pos from o where s.id = o.id and s.position is null;

with o as (
  select id, (row_number() over (partition by set_id order by created_at, id) - 1)::int as pos
    from public.cards)
update public.cards c set position = o.pos from o where c.id = o.id and c.position is null;

create index if not exists sets_folder_position_idx on public.sets  (folder_id, position);
create index if not exists cards_set_position_idx   on public.cards (set_id, position);

-- Eine Zeile pro Karte waeren bei 100 Karten 100 Anfragen. Bewusst SECURITY
-- INVOKER: so greifen die normalen RLS-Regeln, eine Zeile, die man nicht
-- schreiben darf, wird schlicht nicht getroffen.
create or replace function public.reorder_sets(p_ids text[])
returns void language sql volatile set search_path = public as $$
  with ord as (
    select t.id, (t.ord - 1)::int as pos
      from unnest(p_ids) with ordinality as t(id, ord))
  update public.sets s set position = ord.pos from ord where s.id = ord.id;
$$;

create or replace function public.reorder_cards(p_ids text[])
returns void language sql volatile set search_path = public as $$
  with ord as (
    select t.id, (t.ord - 1)::int as pos
      from unnest(p_ids) with ordinality as t(id, ord))
  update public.cards c set position = ord.pos from ord where c.id = ord.id;
$$;

do $$
declare fn text;
begin
  foreach fn in array array['reorder_sets(text[])','reorder_cards(text[])']
  loop
    execute format('revoke execute on function public.%s from public', fn);
    execute format('revoke execute on function public.%s from anon', fn);
    execute format('grant  execute on function public.%s to authenticated', fn);
  end loop;
end $$;
