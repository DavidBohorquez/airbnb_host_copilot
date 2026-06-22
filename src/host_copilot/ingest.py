"""One-off: build documents -> embeddings -> populate Chroma. Implement in M5 (docs/06_chroma.md).

Run with: make ingest
"""

from __future__ import annotations

from host_copilot.config import get_settings
from host_copilot.data.loaders import load_listings
from host_copilot.documents import listing_metadata, listing_to_document
from host_copilot.embeddings import Embedder
from host_copilot.vectorstore.chroma_store import ChromaStore


def main() -> None:
    df = load_listings()
    documents = [listing_to_document(r) for _, r in df.iterrows()]
    metadatas = [listing_metadata(r) for _, r in df.iterrows()]
    ids = df["id"].tolist()

    cache = get_settings().artifacts_path / "listings.npy"
    vectors = Embedder().encode_passages(documents, cache_path=cache)

    store = ChromaStore()
    store.upsert(ids, vectors, metadatas, documents)
    print(f"ingested {store.count()} listings into {get_settings().chroma_path}")


if __name__ == "__main__":
    main()
