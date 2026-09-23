-- 23.09.2026 — Alte Freigaben bekommen ihre Ordner-Einladung nachgetragen
--
-- Freigaben aus April/Mai haengen NUR an einzelnen Sets (set_shares). Damit
-- dort dieselben Rechte gelten wie in neu geteilten Ordnern -- vor allem
-- "neues Set anlegen" -- braucht jede solche Freigabe eine folder_invites-Zeile.
--
-- can_edit bewusst mit bool_AND: die Nachtragung darf keine Rechte erweitern.
-- Wer nur an EINEM Set des Ordners schreiben durfte, bekommt am Ordner kein
-- Bearbeiten-Recht (sein Set-Recht bleibt davon unberuehrt).
--
-- Der Stempel-Trigger zieht owner_id aus der Session und wuerde hier NULL
-- schreiben -- fuer diese eine Nachtragung deshalb ausgeschaltet.
alter table public.folder_invites disable trigger folder_invites_stamp_owner_trg;

insert into public.folder_invites (folder_id, owner_id, owner_email, invited_email, can_edit)
select s.folder_id,
       f.user_id,
       (select u.email from auth.users u where u.id = f.user_id),
       lower(sh.invited_email),
       bool_and(coalesce(sh.can_edit,false))
  from public.set_shares sh
  join public.sets s    on s.id = sh.set_id
  join public.folders f on f.id = s.folder_id
 where s.folder_id is not null
 group by s.folder_id, f.user_id, lower(sh.invited_email)
on conflict (folder_id, invited_email) do nothing;

alter table public.folder_invites enable trigger folder_invites_stamp_owner_trg;
