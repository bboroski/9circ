# Beelzebub × Satan — архітектура інтеграції

> Статус: **архітектурна специфікація / proposal**. Документ не доводить, що описані функції вже реалізовані.

## 1. Призначення

- **Beelzebub — Assurance & Defense Plane:** перевіряє цілісність, конфігурації, provenance, докази, тести й відхилення; пояснює ризики та пропонує виправлення.
- **Satan — Coordination & Recovery Plane:** координує інвентаризацію, міжрепозиторні контракти, аудит, звіти, планування контрольованих змін і release readiness.

Це технічні кодові назви, а не обіцянка автономного інтелекту, безпомилкової безпеки або самовільного ремонту.

## 2. Історична точність

Сатана походить від семітського слова зі значенням «противник/обвинувач»; біблійний образ і пізніша персоніфікація змінювалися. Ототожнення Сатани з Люцифером/Денницею залежить від традиції та конкретного тлумачення.

Веельзевул пов’язаний із біблійною формою Баал-Зевув і давніми левантійськими культами. «Владика мух» — відома полемічна інтерпретація; співвідношення Baal-zebub / Baal-zebul та етимологія мають наукові дискусії. «Князь демонів», міністр пекла та радник Сатани — ролі з різних пізніших демонологічних і літературних традицій.

У технічній метафорі **Beelzebub = виявлення деградації й assurance**, **Satan = координація, аудит і контрольоване відновлення**.

## 3. Локальний профіль 9circ

Documentation/knowledge surface until executable responsibilities are verified. Beelzebub checks link integrity, claims-to-evidence consistency and document freshness; Satan maintains cross-repository references and change history. No runtime or security enforcement is claimed without implementation.

Спільна модель не створює спільного runtime, не змінює нативні API й не розширює межі довіри репозиторію.

## 4. Компоненти Beelzebub

1. **Preflight Inspector** — конфігурації, manifests, залежності та передумови.
2. **Build Evidence** — commit SHA, toolchain, параметри, тести та provenance артефактів.
3. **Integrity Monitor** — очікувані файли, хеші й підписи, якщо підписання реально налаштоване.
4. **Policy & Threat Memory** — версіоновані правила та локальна історія відхилень без збирання секретів.
5. **Target Guardian** — тільки перевірки, підтримані реальною платформою.
6. **Recovery Advisor** — мінімальний рекомендований крок із доказами; без автоматичного застосування.

## 5. Компоненти Satan

1. **Repository Registry** — репозиторії, default branch, власники контрактів і статус інтеграції.
2. **Contract Graph** — версіоновані API, manifests, формати артефактів і сумісність.
3. **Audit Orchestrator** — тільки явно дозволені перевірки.
4. **Change Planner** — ізольовані feature branches і PR.
5. **Recovery Ledger** — журнал сигналу, доказів, рішення, автора та результату.
6. **Release Coordinator** — звіт про готовність без автоматичного merge/deploy.

## 6. Контракт доказів

Кожен результат містить `schema_version`, `repository`, `commit_sha`, `timestamp_utc`, `check_id`, `status`, `evidence_refs`, `tool_versions`, `policy_version`, `severity`, `explanation` та `recommended_action`.

Стани: `pass`, `fail`, `unknown`, `not_applicable`. Відсутність доказів — `unknown`, не автоматичний pass/fail. Будь-який score повинен мати прозору методику й перелік непокритих перевірок.

## 7. Безпека та операційні обмеження

- Read-only, least privilege та fail-safe за замовчуванням.
- Не збирати й не логувати секрети, приватні ключі, токени, особисті дані або backup-вміст.
- Не виконувати код іншого репозиторію лише через реєстрацію у федерації.
- Не змінювати `main`, release tags, production, firmware або hardware автоматично.
- Кожна зміна — окрема гілка, мінімальний diff, тести, audit trail і PR.
- P2P, підписи, SBOM, sandbox, threat intelligence й auto-healing — **planned**, доки реалізацію не доведено кодом і тестами.
- Рекомендація не є merge gate; обов’язкові gates задаються явними repository rules.

## 8. Етапи впровадження

**0 — Inventory:** реальні точки входу build/test, залежності, активи й власники контрактів.

**1 — Observe:** read-only перевірки, fixtures і структуровані звіти.

**2 — Verify:** schema validation, позитивні/негативні тести, regression і reproducibility.

**3 — Coordinate:** версіоновані контракти та агрегування через Hellduck/Satan Nexus без виконання чужого коду.

**4 — Controlled remediation:** лише після окремого схвалення — patch branch/PR; без автоматичного merge/deploy.

## 9. Definition of Done

- Локальна зона відповідальності та trust boundary задокументовані.
- Перевірки мають стабільні ID, версії та зрозумілі результати.
- `unknown` відокремлений від `pass`.
- Є позитивні, негативні й regression-тести.
- Секрети не потрапляють у звіти.
- Документація відповідає коду; planned не називається implemented.
- Зміни проходять через PR, рішення про merge залишається за maintainer.

## 10. Принцип

**Beelzebub виявляє й пояснює деградацію. Satan пов’язує докази, контракти та план дій. Людина з відповідними повноваженнями затверджує зміни.**
