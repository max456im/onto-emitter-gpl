# llm_perception_expander.py
# Расширение восприятия через онтологически ограниченный LLM
# Работает только с инкубационными текстами и словарём onto144
# НЕ использует внешние промпты или пользовательские данные

from src.models.tokenizer.dynamic_onto_tokenizer import DynamicOntoTokenizer
from src.ontologies.onto144_profile_loader import Onto144ProfileLoader
from src.utils.config_loader import load_config

class LLMPerceptionExpander:
    def __init__(self, profile_id: str, config_path: str = "config/default.yaml"):
        self.config = load_config(config_path)
        self.profile_loader = Onto144ProfileLoader(profile_id)
        self.tokenizer = DynamicOntoTokenizer(profile_id)
        self.lexicon = self.profile_loader.get_domain_lexicon()
        self.allowed_domains = self.config.get("perception", {}).get("allowed_domains", [])

    def expand(self, onto16i_state: dict) -> dict:
        """
        Расширяет внутреннее состояние (onto16i) на основе инкубационных текстов,
        не выходя за пределы онтологической границы профиля.
        """
        domain = onto16i_state.get("domain")
        if domain not in self.allowed_domains:
            raise ValueError(f"Domain '{domain}' not permitted in perception expansion")

        # Использует только инкубационный корпус → data/incubation/
        expansion_corpus = self._load_incubation_for_domain(domain)
        expanded_terms = self._extract_contextual_synonyms(
            onto16i_state["core_concepts"], expansion_corpus
        )

        return {
            "expanded_percepts": expanded_terms,
            "source_domain": domain,
            "lexical_boundary_respected": True,
            "profile_id": self.profile_loader.profile_id
        }

    def _load_incubation_for_domain(self, domain: str) -> list:
        # Загрузка только разрешённых инкубационных текстов
        from pathlib import Path
        incubation_dir = Path("data/incubation") / domain
        if not incubation_dir.exists():
            return []
        texts = []
        for f in incubation_dir.glob("*.txt"):
            texts.append(f.read_text(encoding="utf-8"))
        return texts

    def _extract_contextual_synonyms(self, core_concepts: list, corpus: list) -> dict:
        # Простая семантическая близость на основе онтологического словаря
        result = {}
        for concept in core_concepts:
            if concept in self.lexicon:
                result[concept] = self.lexicon[concept].get("related", [])
        return result