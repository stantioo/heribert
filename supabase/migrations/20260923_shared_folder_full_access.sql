-- 23.09.2026 — Freigegebene Ordner: Rechte und Sichtbarkeit
--
-- Ausgangslage (echter Fehler): In Lilos Ordner "Data Driven Advertising"
-- hatten Jana und Fiona 120 Karten angelegt. Die beiden sahen alles, LILO
-- sah nichts -- ihr eigener Ordner war bei ihr leer. Grund: die einzige
-- Leseregel fuer Karten war "own_cards" (auth.uid() = user_id) plus
-- "Invitees read cards in shared sets" (set_shares auf die eigene Adresse).
-- Der EIGENTUEMER eines Sets/Ordners kam in keiner der beiden Regeln vor.
--
-- Neue Regel: Wer Bearbeiten-Recht an einem Ordner hat, darf darin alles --
-- und der Eigentuemer sieht und bearbeitet alles, was in seinem Ordner liegt.
-- Einzige Ausnahme: den Ordner LOESCHEN darf weiter nur der Eigentuemer,
-- das raeumt per Cascade seine Sets und Karten mit ab.
--
-- Merkregel (schon einmal teuer bezahlt): Jede Besitzpruefung, die eine
-- ANDERE Tabelle liest, gehoert in eine SECURITY-DEFINER-Funktion. Sonst
-- laeuft die Policy-Auswertung sets -> folders -> sets im Kreis und PostgREST
-- macht daraus einen 500er.

create or replace function public.can_write_folder(p_folder_id text)
returns boolean language sql stable security definer set search_path = public as $$
  select p_folder_id is not null and (
       exists (select 1 from public.folders f
                where f.id = p_folder_id and f.user_id = auth.uid())
    or exists (select 1 from public.folder_invites iv
                where iv.folder_id = p_folder_id
                  and lower(iv.invited_email) = lower(auth.jwt() ->> 'email')
                  and iv.can_edit = true)
  );
$$;

create or replace function public.can_read_folder(p_folder_id text)
returns boolean language sql stable security definer set search_path = public as $$
  select p_folder_id is not null and (
       exists (select 1 from public.folders f
                where f.id = p_folder_id and f.user_id = auth.uid())
    or exists (select 1 from public.folder_invites iv
                where iv.folder_id = p_folder_id
                  and lower(iv.invited_email) = lower(auth.jwt() ->> 'email'))
    or exists (select 1 from public.sets s
                join public.set_shares sh on sh.set_id = s.id
               where s.folder_id = p_folder_id
                 and lower(sh.invited_email) = lower(auth.jwt() ->> 'email'))
  );
$$;

create or replace function public.can_read_set(p_set_id text)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.sets s
                  where s.id = p_set_id and s.user_id = auth.uid())
      or exists (select 1 from public.set_shares sh
                  where sh.set_id = p_set_id
                    and lower(sh.invited_email) = lower(auth.jwt() ->> 'email'))
      or exists (select 1 from public.sets s
                  where s.id = p_set_id and s.folder_id is not null
                    and ( exists (select 1 from public.folders f
                                   where f.id = s.folder_id and f.user_id = auth.uid())
                       or exists (select 1 from public.folder_invites iv
                                   where iv.folder_id = s.folder_id
                                     and lower(iv.invited_email) = lower(auth.jwt() ->> 'email')) ));
$$;

create or replace function public.can_write_set(p_set_id text)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.sets s
                  where s.id = p_set_id and s.user_id = auth.uid())
      or exists (select 1 from public.set_shares sh
                  where sh.set_id = p_set_id
                    and lower(sh.invited_email) = lower(auth.jwt() ->> 'email')
                    and sh.can_edit = true)
      or exists (select 1 from public.sets s
                  where s.id = p_set_id and s.folder_id is not null
                    and ( exists (select 1 from public.folders f
                                   where f.id = s.folder_id and f.user_id = auth.uid())
                       or exists (select 1 from public.folder_invites iv
                                   where iv.folder_id = s.folder_id
                                     and lower(iv.invited_email) = lower(auth.jwt() ->> 'email')
                                     and iv.can_edit = true) ));
$$;

-- Supabase vergibt per DEFAULT PRIVILEGES einen DIREKTEN Execute-Grant an
-- anon und authenticated. "revoke from public" allein reicht deshalb NICHT --
-- sonst haengt jede neue Funktion als /rest/v1/rpc/<name> offen im Netz.
do $$
declare fn text;
begin
  foreach fn in array array['can_write_folder(text)','can_read_folder(text)','can_read_set(text)','can_write_set(text)']
  loop
    execute format('revoke execute on function public.%s from public', fn);
    execute format('revoke execute on function public.%s from anon', fn);
    execute format('grant  execute on function public.%s to authenticated', fn);
  end loop;
end $$;

-- ---- cards -------------------------------------------------------------
drop policy if exists "Invitees read cards in shared sets" on public.cards;
drop policy if exists "Shared users can insert cards"      on public.cards;
drop policy if exists "Shared users can update cards"      on public.cards;
drop policy if exists "Shared users can delete cards"      on public.cards;

create policy cards_read   on public.cards for select using (auth.uid() = user_id or public.can_read_set(set_id));
create policy cards_insert on public.cards for insert with check (user_id = auth.uid() and public.can_write_set(set_id));
create policy cards_update on public.cards for update using (public.can_write_set(set_id)) with check (public.can_write_set(set_id));
create policy cards_delete on public.cards for delete using (public.can_write_set(set_id));

-- ---- sets ---------------------------------------------------------------
drop policy if exists "Invitees read shared sets"     on public.sets;
drop policy if exists "Shared users can update sets"  on public.sets;

create policy sets_read   on public.sets for select using (auth.uid() = user_id or public.can_read_set(id));
create policy sets_insert on public.sets for insert with check (user_id = auth.uid() and (folder_id is null or public.can_write_folder(folder_id)));
create policy sets_update on public.sets for update using (public.can_write_set(id)) with check (public.can_write_set(id) and (folder_id is null or public.can_write_folder(folder_id)));
create policy sets_delete on public.sets for delete using (public.can_write_set(id));

-- ---- folders ------------------------------------------------------------
drop policy if exists read_shared_folders on public.folders;
create policy folders_read   on public.folders for select using (auth.uid() = user_id or public.can_read_folder(id));
-- Umbenennen/Farbe auch fuer Eingeladene mit Bearbeiten-Recht. Loeschen NICHT.
create policy folders_update on public.folders for update using (public.can_write_folder(id)) with check (public.can_write_folder(id));

-- Ein Eingeladener darf den Ordner umbenennen, aber nicht an sich reissen
-- oder in seinen eigenen Baum haengen.
create or replace function public.folders_guard_foreign_update()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is not null and old.user_id <> auth.uid() then
    new.id        := old.id;
    new.user_id   := old.user_id;
    new.parent_id := old.parent_id;
  end if;
  return new;
end $$;
revoke execute on function public.folders_guard_foreign_update() from public, anon, authenticated;
drop trigger if exists folders_guard_foreign_update_trg on public.folders;
create trigger folders_guard_foreign_update_trg
  before update on public.folders
  for each row execute function public.folders_guard_foreign_update();

-- ---- Einladungen / Freigaben --------------------------------------------
drop policy if exists folder_invites_owner on public.folder_invites;
create policy folder_invites_manage on public.folder_invites for all
  using      (auth.uid() = owner_id or public.can_write_folder(folder_id))
  with check (auth.uid() = owner_id and public.can_write_folder(folder_id));

drop policy if exists "Owners manage their shares" on public.set_shares;
create policy set_shares_manage on public.set_shares for all
  using      (auth.uid() = owner_id or public.can_write_set(set_id))
  with check (auth.uid() = owner_id and public.can_write_set(set_id));
