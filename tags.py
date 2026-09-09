"""Génération automatique de tags par correspondance de mots-clés.

Approche volontairement simple (pas de LLM, pas de dépendance externe) :
chaque tag est associé à une liste de mots-clés/synonymes. On cherche ces
mots-clés (en frontière de mot, insensible à la casse, pluriel anglais
simple toléré) dans le titre et le résumé d'un article. Les tags trouvés
sont retournés triés par pertinence (nombre de correspondances), plafonnés
à `max_tags`.
"""
import re

# articles matching these terms are dropped entirely before tagging/storage
# (see is_ai_related below) rather than merely left untagged — AI content is
# excluded from this dashboard altogether, not just unlabeled.
EXCLUDED_AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "ml", "neural network",
    "llm", "gpt", "chatgpt", "claude", "gemini", "openai", "anthropic", "deepseek",
    "deep learning", "transformer", "foundation model", "open model", "genai",
]

# displayed tag -> keywords that trigger it
TAG_KEYWORDS = {
    "Data": ["data engineering", "data science", "dataset", "etl", "pandas", "spark", "airflow", "data pipeline", "big data"],
    "Python": ["python", "pypi", "django", "flask", "fastapi", "pytest", "pip"],
    "JavaScript": ["javascript", "typescript", "node.js", "nodejs", "react", "vue", "svelte", "next.js", "deno", "bun"],
    "Rust": ["rust", "cargo", "rustlang"],
    "Go": ["golang", "go lang"],
    "Web": ["web dev", "frontend", "front-end", "backend", "back-end", "html", "css", "browser", "web browser", "extension", "webassembly", "wasm"],
    "Mobile": ["ios", "android", "swift", "kotlin", "flutter", "react native", "mobile app"],
    "Cloud": ["aws", "azure", "gcp", "google cloud", "cloud native", "serverless", "lambda"],
    "DevOps": ["devops", "docker", "kubernetes", "k8s", "ci/cd", "terraform", "ansible", "container"],
    "Security": ["security", "vulnerability", "cve", "exploit", "ransomware", "breach", "phishing", "encryption", "cybersecurity", "authentication", "cyber command", "cyberattack"],
    "Database": ["database", "sql", "postgres", "postgresql", "mysql", "mongodb", "redis", "sqlite", "nosql"],
    "API": ["api", "rest api", "graphql", "webhook", "grpc"],
    "Open Source": ["open source", "open-source", "github", "git", "pull request", "license", "oss"],
    "3D / Graphics": ["3d", "blender", "cgi", "render", "motion design", "animation", "vfx", "unreal engine", "unity"],
    "Gaming": ["game dev", "gamedev", "video game", "game"],
    "Blockchain": ["blockchain", "crypto", "ethereum", "bitcoin", "web3", "nft", "smart contract"],
    "Startup / Business": ["startup", "funding", "venture capital", "acquisition", "ipo", "layoffs"],
    "Career": ["career", "interview", "job", "hiring"],
    "Tutorial": ["tutorial", "how to", "guide", "walkthrough", "cheat sheet"],
    "Performance": ["performance", "optimization", "benchmark", "latency", "scalability"],
    "Linux": ["linux", "ubuntu", "debian", "bash", "shell", "cli", "terminal"],
    "Design": ["design", "ui/ux", "user experience", "figma", "typography"],
    "Research": ["research", "paper", "arxiv", "study"],
    "Privacy": ["privacy", "gdpr", "tracking"],
    "Robotics / Hardware": ["robotics", "hardware", "iot", "raspberry pi", "arduino", "chip", "semiconductor", "nvidia", "gpu", "memory chip"],
    "Systems / Low-level": ["assembly", "kernel", "compiler", "embedded system", "firmware", "x86", "risc-v", "verilog", "fpga", "llvm", "operating system"],
    "Algorithms / CS Theory": ["algorithm", "computational complexity", "graph theory", "np-hard", "data structure"],
    "Space": ["nasa", "satellite", "telescope", "spacecraft", "voyager", "spacex", "astronomy", "orbit", "space agency"],
}

def _compile(keywords):
    return [re.compile(r"(?<![\w-])" + re.escape(kw.strip()) + r"(?:s|es)?(?![\w-])", re.IGNORECASE)
            for kw in keywords]


_COMPILED = {tag: _compile(keywords) for tag, keywords in TAG_KEYWORDS.items()}
_EXCLUDED_AI_PATTERNS = _compile(EXCLUDED_AI_KEYWORDS)


def is_ai_related(text: str) -> bool:
    """True si `text` mentionne l'IA/le machine learning — utilisé pour exclure
    entièrement ces articles avant stockage (cf. sources/__init__.py)."""
    return bool(text) and any(p.search(text) for p in _EXCLUDED_AI_PATTERNS)


def generate_tags(text: str, max_tags: int = 5) -> list[str]:
    """Retourne jusqu'à `max_tags` tags pertinents pour `text`, triés par nombre de correspondances."""
    if not text:
        return []

    scored = []
    for tag, patterns in _COMPILED.items():
        hits = sum(1 for pattern in patterns if pattern.search(text))
        if hits:
            scored.append((hits, tag))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [tag for _, tag in scored[:max_tags]]
