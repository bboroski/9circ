# Linguistic Heritage Engine: Cyrillic Ы

**Status:** scoped research integration  
**Record:** `data/linguistic-heritage/cyrillic-letter-y.json`  
**Contract:** `linguistic-heritage.letter.v1`

This repository participates in the 13-repository Linguistic Heritage Engine, which separates grapheme genealogy, historical phonology, modern articulation, comparative Slavic phonetics, orthographic history and cultural interpretation.

## Repository role

Reference/documentation integration: this repository carries a versioned research record and conformance test as metadata. It does not acquire a new runtime dependency or change its existing product behavior.

## Evidence policy

- Separate the history of Ы as a grapheme from the history of [ɨ] as a sound.
- Treat ЪІ / ЪИ as the conventional ligature account, without inventing a single creation date.
- Mark /i/ versus /ɨ/ phonological analyses as debated.
- Do not equate Russian ы, Polish y and Ukrainian и as identical sounds.
- Keep symbolism and numerology in the interpretive layer, not the evidence layer.
- Require shelfmark, folio and specialist source for manuscript-specific claims.
- Distinguish evidence, scholarly interpretation and open hypothesis.

## Validation

```bash
python -m unittest discover -s tests -p 'test_linguistic_heritage_contract.py' -v
```

The standard-library test checks data structure and research guardrails; it does not prove historical claims.

## Sources

- Cavar et al., *High central vowels in Polish, Ukrainian and Russian*, JIPA (2025), [DOI](https://doi.org/10.1017/S0025100325000040).
- *Russian*, JIPA (2015), [Cambridge Core](https://www.cambridge.org/core/journals/journal-of-the-international-phonetic-association/article/russian/55589EC639ADEF1764B5ECD0B76970FA).
