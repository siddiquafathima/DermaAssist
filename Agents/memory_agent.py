# memory_agent.py
import os
import json
from pathlib import Path
import numpy as np

# Try to import FAISS + sentence-transformers; if missing, use JSON fallback.
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    FAISS_OK = True
except Exception:
    MODEL = None
    FAISS_OK = False

DATA_DIR = Path("data/profiles")
FAISS_PATH = Path("data/faiss_index.bin")
META_JSON = Path("data/faiss_meta.json")
DATA_DIR.mkdir(parents=True, exist_ok=True)

EMB_DIM = 384
SIM_THRESHOLD = 0.70  # similarity threshold for a positive match

def _encode_text(profile: dict) -> str:
    return f"{profile.get('name','')}; {profile.get('age','')}; {profile.get('skin_type','')}; {profile.get('concern','')}"

def encode_profile(profile: dict):
    text = _encode_text(profile)
    if not FAISS_OK or MODEL is None:
        return None, text
    emb = MODEL.encode([text], convert_to_numpy=True)
    return emb.astype("float32"), text

def _init_index():
    return faiss.IndexFlatL2(EMB_DIM)

def save_profile_memory(profile: dict) -> str:
    # Save readable JSON
    uid = profile.get("user_id") or f"{profile.get('name')}_{profile.get('age')}"
    pfile = DATA_DIR / f"profile_{uid}.json"
    with open(pfile, "w") as f:
        json.dump(profile, f, indent=2)

    emb, text = encode_profile(profile)
    if not FAISS_OK or emb is None:
        # JSON fallback: append to meta json
        meta = []
        if META_JSON.exists():
            meta = json.loads(META_JSON.read_text())
        meta.append({"profile": text, "user_id": uid})
        META_JSON.write_text(json.dumps(meta, indent=2))
        return "✔ Memory saved to JSON fallback."
    # use FAISS
    if FAISS_PATH.exists():
        index = faiss.read_index(str(FAISS_PATH))
        meta = json.loads(META_JSON.read_text()) if META_JSON.exists() else []
    else:
        index = _init_index()
        meta = []
    index.add(emb)
    meta.append({"profile": text, "user_id": uid})
    faiss.write_index(index, str(FAISS_PATH))
    META_JSON.write_text(json.dumps(meta, indent=2))
    return "✔ Memory saved to FAISS."

def retrieve_memory(profile: dict):
    emb, text = encode_profile(profile)
    # no memory stored yet
    if not FAISS_OK or not FAISS_PATH.exists():
        # fallback: try last exact user_id match
        if META_JSON.exists():
            meta = json.loads(META_JSON.read_text())
            uid = profile.get("user_id")
            if uid:
                for item in reversed(meta):
                    if item.get("user_id") == uid:
                        return item, 1.0
        return None, 0.0

    index = faiss.read_index(str(FAISS_PATH))
    D, I = index.search(emb, 1)
    distance = float(D[0][0])
    similarity = 1.0 / (1.0 + distance)  # heuristic convert L2→[0,1]
    meta = json.loads(META_JSON.read_text()) if META_JSON.exists() else []

    pos = int(I[0][0])
    if pos < 0 or pos >= len(meta):
        return None, similarity

    match = meta[pos]
    if similarity >= SIM_THRESHOLD:
        return match, similarity
    return None, similarity
