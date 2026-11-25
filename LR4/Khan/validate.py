"""Статическая проверка C4 PlantUML: ID, связи, нумерация.

Это не компилятор PlantUML: полную проверку выполняет PlantUML CLI/VS Code.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "diagrams"
EXPECTED = {
    "landscape_analytics.puml",
    "context_analytics_local.puml",
    "dynamic_rating_calc.puml",
    "deployment_analytics.puml",
}
DEFINITION = re.compile(
    r"(?m)^\s*(?:Person|System|System_Ext|Enterprise_Boundary|System_Boundary|"
    r"Container|ContainerDb|Container_Boundary|Component|Deployment_Node)\(\s*(\w+)\s*,"
)
REL = re.compile(r"(?m)^\s*Rel\(\s*(\w+)\s*,\s*(\w+)\s*,\s*\"([^\"]+)\"")
FORBIDDEN = re.compile(r"(?m)\b(?:Rel_R|Rel_L|Rel_U|Rel_D)\(")


def validate() -> None:
    filenames = {p.name for p in ROOT.glob("*.puml")}
    assert EXPECTED == filenames, f"Ожидаются {sorted(EXPECTED)}, найдены {sorted(filenames)}"

    diagrams: dict[str, str] = {}
    for filename in sorted(EXPECTED):
        text = (ROOT / filename).read_text(encoding="utf-8")
        diagrams[filename] = text
        assert text.startswith("@startuml") and text.rstrip().endswith("@enduml"), filename
        assert not FORBIDDEN.search(text), f"{filename}: запрещено принудительное позиционирование"
        assert text.count("{") == text.count("}"), f"{filename}: несбалансированные границы"
        definitions = DEFINITION.findall(text)
        assert len(definitions) == len(set(definitions)), f"{filename}: повтор ID"
        ids = set(definitions)
        relationships = REL.findall(text)
        assert relationships, f"{filename}: нет связей"
        for origin, target, _ in relationships:
            assert origin in ids and target in ids, f"{filename}: {origin} -> {target} (не объявлен)"

    dynamic = diagrams["dynamic_rating_calc.puml"]
    numbers = [int(re.match(r"\d+", label).group(0)) for _, _, label in REL.findall(dynamic)]
    assert numbers == list(range(1, 14)), f"Нарушена хронология Dynamic: {numbers}"
    for element in ["api_gateway", "analytics_service", "grpc_handler",
                    "analytics_coordinator", "rating_calc", "analytics_repo", "database"]:
        assert element in dynamic and element in diagrams["deployment_analytics.puml"] + dynamic
    assert "Rel(api_gateway, analytics_service," in diagrams["deployment_analytics.puml"]
    assert "finance_scholarship" in diagrams["landscape_analytics.puml"]

    print("OK: 4 диаграммы, идентификаторы, связи, 13 шагов Dynamic и архитектурные стыки.")
    print("Внимание: визуальную компиляцию C4-PlantUML требуется проверить отдельно.")


if __name__ == "__main__":
    validate()
