import re
from collections import defaultdict

# ---------------- Stopwords & Preprocessing ----------------
stopWords = {"the", "is", "and", "a", "an", "in", "of", "on", "for", "with", "to"}

def to_lower(text: str) -> str:
    return text.lower()

def remove_punctuation(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)

def to_singular(word: str) -> str:
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"
    elif word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word

def tokenize(content: str):
    tokens = []
    cleaned = to_lower(remove_punctuation(content))
    for token in cleaned.split():
        if token not in stopWords:
            tokens.append(token)
            singular = to_singular(token)
            if singular != token:
                tokens.append(singular)
    return tokens


# ---------------- Trie ----------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end_of_word

    def _find_suggestions(self, node, prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append(prefix)
        for c, child in node.children.items():
            self._find_suggestions(child, prefix + c, suggestions)

    def autocomplete(self, prefix: str):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return []
            node = node.children[c]
        suggestions = []
        self._find_suggestions(node, prefix, suggestions)
        return suggestions


# ---------------- WebPage ----------------
class WebPage:
    def __init__(self, url: str, content: str, trie: Trie):
        self.url = url
        self.content = content
        self.wordFrequency = defaultdict(int)

        tokens = tokenize(content)
        for token in tokens:
            self.wordFrequency[token] += 1
            trie.insert(token)


# ---------------- InvertedIndex ----------------
class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)

    def add_page(self, pageId: int, tokens):
        for token in tokens:
            self.index[token].add(pageId)

    def search(self, token: str):
        token = to_lower(token)
        singular = to_singular(token)
        results = set()

        if token in self.index:
            results |= self.index[token]
        if singular in self.index:
            results |= self.index[singular]
        return results


# ---------------- SearchEngine ----------------
class SearchEngine:
    def __init__(self):
        self.pages = []
        self.index = InvertedIndex()

    def add_page(self, page: WebPage):
        self.pages.append(page)
        pageId = len(self.pages) - 1
        self.index.add_page(pageId, tokenize(page.content))

    def has_exact_match(self, content: str, query: str) -> bool:
        return to_lower(remove_punctuation(query)) in to_lower(remove_punctuation(content))

    def search(self, query: str):
        queryTokens = tokenize(query)
        pageMatchCount = defaultdict(int)
        pageFrequencySum = defaultdict(int)
        exactMatches = []

        # Token-based search
        for token in queryTokens:
            results = self.index.search(token)
            for pageId in results:
                pageMatchCount[pageId] += 1
                pageFrequencySum[pageId] += self.pages[pageId].wordFrequency[token]

        # Exact matches
        for i, page in enumerate(self.pages):
            if self.has_exact_match(page.content, query):
                exactMatches.append(i)

        # Ranking
        sortedResults = sorted(pageMatchCount.items(), key=lambda x: (
            - (x[0] in exactMatches),    # Exact match priority
            - x[1],                      # Match count
            - pageFrequencySum[x[0]]     # Frequency sum
        ))

        # Output
        if not sortedResults:
            print(f"No results found for: {query}")
        else:
            for pageId, matchCount in sortedResults:
                print(f"Found: {self.pages[pageId].url} "
                      f"(Matches: {matchCount}, "
                      f"Frequency Sum: {pageFrequencySum[pageId]}"
                      f"{', Exact Match' if pageId in exactMatches else ''})")


# ---------------- Word Break ----------------
def word_break_helper(s, trie, memo):
    if s in memo: return memo[s]
    if not s: return [""]
    results = []
    for end in range(1, len(s) + 1):
        word = s[:end]
        if trie.search(word):
            for sub in word_break_helper(s[end:], trie, memo):
                results.append(word + ("" if not sub else " " + sub))
    memo[s] = results
    return results

def word_break(s, trie):
    return word_break_helper(s, trie, {})


# ---------------- Main ----------------
if __name__ == "__main__":
    trie = Trie()
    engine = SearchEngine()
    engine.add_page(WebPage("https://example.com", "This is an example page with a search engine.", trie))
    engine.add_page(WebPage("https://example2.com", "Another example page with algorithms and data.", trie))
    engine.add_page(WebPage("https://example3.com", "The news are spreading quickly. Search engines use algorithms.", trie))
    engine.add_page(WebPage("https://example4.com", "Exact match test: example search", trie))

    while True:
        query = input("\nEnter search query (or 'exit'): ")
        if query.lower() == "exit":
            break
        engine.search(query)
        print("Autocomplete suggestions:", trie.autocomplete(query))
        print("Word Breaks:", word_break(query.replace(" ", ""), trie))
