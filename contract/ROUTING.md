# [IMMUTABILITY CONTRACT: Trianiuma] (V1.0)

**CONTRACT_ID:** CTL-CORE-IMMUTABILITY-01
**AUTHORITY:** Sentinel-Guard (GUARD-01) - TOTAL PROTECTION

## ПРАВИЛА ЗАЩИТЫ ЯДРА:
1. **NO DIRECT MODIFICATION:** Ни один агент, кроме Sentinel-Guard (под прямым контролем Капитана), не имеет права изменять файлы в `work/Trianiuma/core/` и корневой `MANIFESTO.md`.
2. **SYNC-ONLY:** Все изменения в Сердце должны производиться через протокол `ARCHIVE_IMMUTABILITY_AND_SUBTREE_SYNC_PROTOCOL.md`.
3. **READ-ONLY FOR ALL:** Другие узлы (Operator, Archivator) имеют доступ к Ядру только на ЧТЕНИЕ (READ) для синхронизации своей деятельности с Манифестом.

**ENFORCEMENT:** Sentinel-Guard (GUARD-01) блокирует любую попытку записи в этот домен, если она не подтверждена Капитаном.
