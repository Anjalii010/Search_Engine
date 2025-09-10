Mini Python Search Engine

A Python-based mini search engine that allows users to add web pages, search for queries, and get ranked results with real-time suggestions. It demonstrates core algorithms and data structures used in information retrieval, such as Tries, inverted indexes, and frequency-based ranking.

Features

Add web pages with automatic word indexing.

Search queries with ranked results based on:

Number of matched words

Word frequency in pages

Exact phrase matches

Autocomplete suggestions while typing using a Trie.

Tokenization and preprocessing:

Lowercase conversion

Punctuation removal

Stopword filtering

Word stemming (singular/plural handling)

Word-break handling to split concatenated words into meaningful terms.

Inverted index for fast word-to-page lookup.

How it Works

Tokenization & Preprocessing: Input text is cleaned, stopwords are removed, and words are converted to singular forms.

Trie: All words are inserted into a Trie for fast autocomplete suggestions and word searches.

Inverted Index: Maps each word to the web pages it appears in for quick lookup.

Search & Ranking: Queries are matched against indexed pages. Results are ranked based on:

Number of matching query words

Total frequency of matched words in the page

Whether the page contains the exact query phrase

Word Break: Handles concatenated words by suggesting valid splits using the Trie.
