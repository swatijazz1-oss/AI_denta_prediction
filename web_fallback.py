"""
Web fallback for the AI Dental Analyzer.

This module is used only when the local/vector dental
knowledge base does not provide sufficiently relevant
information.

It searches the web and extracts readable text from
relevant dental-health pages.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


# ============================================================
# CONFIGURATION
# ============================================================

REQUEST_TIMEOUT = 10

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0 Safari/537.36"
)


# ============================================================
# SEARCH WEB
# ============================================================

def search_web(query, max_results=5):
    """
    Search the web using DuckDuckGo HTML search.

    Returns a list of dictionaries containing:
        title
        url
        snippet
    """

    search_url = (
        "https://html.duckduckgo.com/html/?q="
        + quote(query)
    )

    headers = {
        "User-Agent": USER_AGENT
    }

    try:

        response = requests.get(
            search_url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

    except requests.RequestException as e:

        print("Web search failed:", e)

        return []


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    results = []


    for result in soup.select(
        ".result"
    )[:max_results]:

        title_element = result.select_one(
            ".result__title"
        )

        link_element = result.select_one(
            ".result__a"
        )

        snippet_element = result.select_one(
            ".result__snippet"
        )


        if not link_element:

            continue


        title = (
            title_element.get_text(
                " ",
                strip=True
            )
            if title_element
            else "Dental information"
        )


        url = link_element.get(
            "href",
            ""
        )


        snippet = (
            snippet_element.get_text(
                " ",
                strip=True
            )
            if snippet_element
            else ""
        )


        if url:

            results.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet
                }
            )


    return results


# ============================================================
# EXTRACT PAGE TEXT
# ============================================================

def extract_page_text(url, max_chars=6000):
    """
    Download a webpage and extract its main readable text.
    """

    headers = {
        "User-Agent": USER_AGENT
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

    except requests.RequestException:

        return ""


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # Remove elements that usually don't contain
    # useful article content.

    for element in soup(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]
    ):

        element.decompose()


    text = soup.get_text(
        " ",
        strip=True
    )


    # Normalize whitespace.

    text = " ".join(
        text.split()
    )


    return text[:max_chars]


# ============================================================
# DENTAL WEB FALLBACK
# ============================================================

def web_fallback(
    query,
    max_results=3
):
    """
    Search for dental information and retrieve
    readable text from the most relevant pages.

    Returns:

        {
            "used": True/False,
            "results": [...]
        }
    """

    results = search_web(
        query,
        max_results=max_results
    )


    enriched_results = []


    for result in results:

        page_text = extract_page_text(
            result["url"]
        )


        if page_text:

            enriched_results.append(
                {
                    "title": result["title"],
                    "url": result["url"],
                    "snippet": result["snippet"],
                    "content": page_text
                }
            )


    return {
        "used": len(enriched_results) > 0,
        "results": enriched_results
    }


# ============================================================
# FORMAT WEB RESULTS FOR GEMINI
# ============================================================

def format_web_context(
    web_results,
    max_chars_per_source=3500
):
    """
    Convert retrieved web pages into a compact
    context string for Gemini.
    """

    if not web_results:

        return (
            "No useful web information was retrieved."
        )


    context_parts = []


    for index, result in enumerate(
        web_results,
        start=1
    ):

        content = result.get(
            "content",
            ""
        )


        content = content[
            :max_chars_per_source
        ]


        context_parts.append(
            f"""
SOURCE {index}

Title:
{result.get("title", "Unknown")}

URL:
{result.get("url", "")}

Summary:
{result.get("snippet", "")}

Retrieved page content:
{content}
"""
        )


    return "\n\n".join(
        context_parts
    )