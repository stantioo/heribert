-- 23.09.2026 — Letzte Luecke im Grundsatz "wer bearbeiten darf, darf alles"
--
-- Das Stift-Symbol in der Teilen-Liste schaltet die Rechte einer ANDEREN
-- Person um. Die WITH-CHECK-Bedingung verlangte "auth.uid() = owner_id" --
-- die Zeile gehoert aber dem Freigebenden, nicht dem Bearbeiter. Das Symbol
-- war also da, das Umschalten lief in einen RLS-Verstoss.
--
-- Beim INSERT ist die Bedingung entbehrlich: die Stempel-Trigger
-- set_shares_stamp_owner / folder_invites_stamp_owner setzen owner_id
-- bedingungslos auf auth.uid(), eine Zeile kann also gar nicht unter
-- fremdem Namen entstehen.
alter policy set_shares_manage on public.set_shares
  using      (auth.uid() = owner_id or public.can_write_set(set_id))
  with check (public.can_write_set(set_id));

alter policy folder_invites_manage on public.folder_invites
  using      (auth.uid() = owner_id or public.can_write_folder(folder_id))
  with check (public.can_write_folder(folder_id));
