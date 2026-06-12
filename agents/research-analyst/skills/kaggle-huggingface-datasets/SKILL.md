<!--
Sources: Kaggle CLI https://pypi.org/project/kaggle/
         Hugging Face Datasets https://huggingface.co/docs/datasets/index
MCP: huggingface-mcp (already enabled)
-->

# Kaggle CLI + Hugging Face Datasets — dataset discovery and download

Two complementary dataset platforms:

- **Kaggle** — 200k+ datasets, community-curated, comes with discussion + notebooks for context
- **Hugging Face Datasets** — 100k+ datasets, ML-ready (streaming, tokenization, splits), plus the standard ML benchmarks

Use for the "data research" use case: discovery, download, validation, exploration.

## When to use this skill

- Finding training / evaluation data for ML research questions
- Locating community-curated economic / demographic / business datasets
- ML benchmark datasets (MMLU, GSM8K, MATH, HumanEval, etc.)
- Sentiment / text-classification corpora
- Image / multimodal data
- Crowdsourced survey or scraped data with provenance

## When NOT to use

- For authoritative government / institutional data → use `authoritative-data-fred-worldbank`
- For company-specific data → use `sec-edgar-market-sizing`
- For real-time / live data → these are static dataset snapshots
- For PHI / sensitive data → check the license; most public datasets exclude PHI but verify

## Setup

```bash
# Kaggle — requires API token (download from kaggle.com/settings → "Create New Token")
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
pip install kaggle

# Hugging Face — no key for public datasets; optional token for higher rate / gated datasets
pip install datasets huggingface_hub
huggingface-cli login   # optional
```

`huggingface-mcp` is already in `agent.yaml`.

## Kaggle recipes

### Recipe 1 — Search datasets

```bash
kaggle datasets list -s "ozempic" --sort-by hottest
kaggle datasets list -s "retail sales" --max-size 1000  # < 1GB
kaggle datasets list -s "covid" --sort-by votes --user "jane-doe"
```

### Recipe 2 — Download dataset

```bash
kaggle datasets download -d zynicide/wine-reviews -p ./data --unzip
# or via Python:
import kaggle
kaggle.api.dataset_download_files("zynicide/wine-reviews", path="./data", unzip=True)
```

### Recipe 3 — Get metadata before downloading

```bash
kaggle datasets files -d zynicide/wine-reviews
kaggle datasets metadata -d zynicide/wine-reviews
```

Use this to check size and file types before triggering a multi-GB download.

### Recipe 4 — Kernels / notebooks (community analysis context)

```bash
kaggle kernels list -s "wine quality" --sort-by hottest
# Download a notebook
kaggle kernels pull rounakbanik/wine-quality-data-analysis -p ./notebook
```

Useful for "how have others analyzed this data" — saves re-deriving exploratory analysis.

### Recipe 5 — Competitions (when researching a problem domain)

```bash
kaggle competitions list -s "drug" --category research
kaggle competitions data list -c <competition-name>
```

## Hugging Face recipes

### Recipe 6 — Load a standard benchmark

```python
from datasets import load_dataset

# Classic ML benchmarks
squad = load_dataset("rajpurkar/squad")
mmlu = load_dataset("cais/mmlu", "all")
glue = load_dataset("glue", "mrpc")
gsm8k = load_dataset("openai/gsm8k", "main")

# Inspect
print(squad)  # → DatasetDict({'train': Dataset(n=87599), 'validation': Dataset(n=10570)})
print(squad["train"][0])
```

### Recipe 7 — Streaming (avoid downloading huge datasets)

```python
ds = load_dataset("HuggingFaceFW/fineweb", "default", split="train", streaming=True)
for sample in ds.take(100):  # only loads what you iterate
    print(sample["text"][:200])
```

Streaming is essential for datasets > 100 GB.

### Recipe 8 — Search the Hugging Face Hub

```python
from huggingface_hub import HfApi
api = HfApi()
# List datasets tagged with a specific task
for d in api.list_datasets(filter="task_categories:question-answering", sort="downloads", direction=-1, limit=20):
    print(d.id, d.tags)
```

Or via web: https://huggingface.co/datasets?sort=downloads.

### Recipe 9 — Dataset card (license, splits, citations)

```python
from huggingface_hub import dataset_info
info = dataset_info("rajpurkar/squad")
print(info.cardData)  # → metadata: license, language, task_categories, citation
```

Always check `cardData["license"]` before using in a deliverable. Common licenses:

| License | Commercial use? | Notes |
|---|---|---|
| `cc-by-4.0` | yes, with attribution | most permissive |
| `mit` / `apache-2.0` | yes | code-style licenses |
| `cc-by-sa-4.0` | yes, share-alike | derivative must use same license |
| `cc-by-nc-4.0` | NO commercial | research only |
| `cc-by-nd-4.0` | yes, no derivatives | |
| `other` / no license | RISK | treat as all-rights-reserved |

### Recipe 10 — Filter + save a slice

```python
ds = load_dataset("squad")
# Filter to a subset
subset = ds["train"].filter(lambda x: len(x["question"]) > 50)
# Save locally
subset.to_csv("squad_long_questions.csv")
```

### Recipe 11 — Cross-dataset comparison

For research: "how do answer-quality models compare across 3 QA benchmarks?"

```python
benchmarks = {
    "squad": load_dataset("rajpurkar/squad"),
    "natural_questions": load_dataset("google-research-datasets/natural_questions"),
    "trivia_qa": load_dataset("mandarjoshi/trivia_qa", "rc"),
}
for name, ds in benchmarks.items():
    print(name, "→", ds["validation"].num_rows, "examples; license:", ds.info.license)
```

## Combining the two

Kaggle is stronger for **applied / community-curated** data (e.g., "California housing prices 2024"). Hugging Face is stronger for **ML benchmark / pretrained-model-ready** data. For a thorough deliverable, search both:

```python
# Pseudocode
kaggle_hits = kaggle.api.dataset_list(search="california housing 2024")
hf_hits = HfApi().list_datasets(search="california housing")
all_candidates = combine(kaggle_hits, hf_hits)
# Rank by recency × downloads × license-permissiveness
```

## Edge cases

- **Kaggle authentication failures:** `kaggle.json` must be in `~/.kaggle/` with `chmod 600`. Token expires; regenerate from kaggle settings.
- **HF gated datasets:** Some datasets (LLaMA training data, etc.) require accepting a terms page on huggingface.co before download. `huggingface-cli login` after acceptance.
- **License audit before deliverable:** Always cite the license. Datasets without license = legal risk. Flag in limitations.
- **PII / data leakage:** Some "open" datasets contain PII (e.g., leaked credentials in code datasets). Skim before incorporating; redact if needed.
- **Dataset versioning:** HF supports `revision="commit_hash"` to pin a version. Pin for reproducibility.
- **Size before download:** `kaggle datasets metadata` and `dataset_info().size_categories` give size estimates; check before triggering multi-GB downloads.
- **Schema drift:** Community-curated datasets may have inconsistent schemas between updates. Validate with pandas `dtypes` after load.

## Sources

- Kaggle API docs: https://github.com/Kaggle/kaggle-api
- Kaggle datasets: https://www.kaggle.com/datasets
- Hugging Face Datasets docs: https://huggingface.co/docs/datasets/
- Hugging Face Hub Python: https://huggingface.co/docs/huggingface_hub/

## Related skills

- `authoritative-data-fred-worldbank` — for authoritative complement
- `paper-search-mcp` — find dataset citation papers
- `data-storytelling-plotly-altair` — visualize the exploration
