config/
├── default.yaml                                  # Базовые настройки: пути, режимы, логирование, сериализация
│
├── ethical_rules.yaml                            # Этические правила и контексты
│   ├── trust_levels:                             # Уровни доверия к контексту
│   │   - low (обычные запросы)
│   │   - medium (финансы, образование)
│   │   - high (медицина, право, экология)
│   │   - critical (жизнь, смерть, нарушение целостности)
│   ├── high_stakes_contexts:                     # Список доменов, требующих VMA-валидации
│   │   - organ_transplant
│   │   - criminal_liability
│   │   - ecosystem_harm
│   │   - family_integrity
│   └── omission_rules:                           # Правила обработки умолчаний (implicit harm)
│
├── onto144_bindings.yaml                         # Привязка профилей к внутренним идентификаторам
│   ├── profile_id_map:
│   │   medical_choleric_1985: "onto144:MC85"
│   │   legal_sanguine_1990: "onto144:LS90"
│   └── profile_loading_policy: "strict"           # Запрет частичной загрузки
│
├── domain_bindings.yaml                          # Привязка доменов к лексиконам и стилям
│   ├── medical:
│   │   lexicon: "domain_lexicons/medical_terms.yaml"
│   │   emission_style: "relational_style.yaml"
│   │   phase_strategy: "reflective_mode.yaml"
│   │   temperament_filter: "choleric"
│   │
│   └── legal:
│       lexicon: "domain_lexicons/legal_terms.yaml"
│       emission_style: "canonical_style.yaml"
│       phase_strategy: "reflective_mode.yaml"
│       temperament_filter: "sanguine"
│
├── canonical_generation_rules.yaml               # Правила генерации канонического текста
│   ├── structural_integrity: true                # Запрет на нарушение синтаксиса онтологии
│   ├── literary_degradation_threshold: 0.15      # Макс. допустимая мера «деградации»
│   ├── require_vma_signature: true               # Обязательная подпись VMA для L0–L2
│   ├── allow_human_paraphrase: false             # Запрет на перефразирование без валидации
│   └── sign_with_profile_id: true                # Подпись профилем onto144
│
└── hardware_and_license_policy.yaml              # (опционально, но рекомендуется)
    ├── enforce_gpl_runtime: true
    ├── allow_cloud_execution: false              # Только локальные/лицензированные среды
    └── require_crypto_validation: true           # Проверка подписи перед эмиссией