#!/usr/bin/env python3
"""
Podchaser Enterprise GraphQL API client for the MVPeople PR Intelligence Agent.

Auth: client_credentials flow. Needs PODCHASER_CLIENT_ID and PODCHASER_CLIENT_SECRET
in a .env file at the project root (see .env.example). The access token is valid for
1 year and gets cached in .podchaser_token.json (gitignored) so we don't re-request it
on every call.

Usage:
    python3 scripts/podchaser.py search "mental health" --language de --limit 10
    python3 scripts/podchaser.py search "Leadership" --language de --category business
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

API_URL = "https://api.podchaser.com/graphql"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")
TOKEN_CACHE_FILE = os.path.join(PROJECT_ROOT, ".podchaser_token.json")


def load_env():
    env = dict(os.environ)
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                env.setdefault(key.strip(), value.strip())
    return env


def graphql_request(query, variables=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} error from Podchaser API:", file=sys.stderr)
        print(e.read().decode("utf-8"), file=sys.stderr)
        sys.exit(1)


def get_access_token(env):
    client_id = env.get("PODCHASER_CLIENT_ID")
    client_secret = env.get("PODCHASER_CLIENT_SECRET")
    if not client_id or not client_secret:
        print(
            "Fehlt: PODCHASER_CLIENT_ID und/oder PODCHASER_CLIENT_SECRET in .env.\n"
            "Beide Werte findest du im Podchaser-Dashboard unter API-Settings "
            "(Development oder Production Client).",
            file=sys.stderr,
        )
        sys.exit(1)

    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, "r") as f:
            cached = json.load(f)
        if cached.get("expires_at", 0) > time.time() + 3600:
            return cached["access_token"]

    mutation = """
    mutation RequestAccessToken($client_id: String!, $client_secret: String!) {
      requestAccessToken(
        input: {
          grant_type: CLIENT_CREDENTIALS
          client_id: $client_id
          client_secret: $client_secret
        }
      ) {
        access_token
        token_type
        expires_in
      }
    }
    """
    result = graphql_request(
        mutation, {"client_id": client_id, "client_secret": client_secret}
    )
    if "errors" in result:
        print("Fehler beim Token-Request:", json.dumps(result["errors"], indent=2), file=sys.stderr)
        sys.exit(1)

    token_data = result["data"]["requestAccessToken"]
    access_token = token_data["access_token"]
    expires_in = token_data.get("expires_in", 31536000)
    with open(TOKEN_CACHE_FILE, "w") as f:
        json.dump(
            {"access_token": access_token, "expires_at": time.time() + expires_in}, f
        )
    return access_token


def search_podcasts(token, search_term, language=None, category=None, limit=10):
    query = """
    query SearchPodcasts($searchTerm: String, $filters: PodcastFilters, $first: Int) {
      podcasts(searchTerm: $searchTerm, filters: $filters, first: $first) {
        data {
          id
          title
          description
          url
          rssUrl
          webUrl
          imageUrl
          language
          numberOfEpisodes
          applePodcastsId
          latestEpisodePublishDate
        }
        paginatorInfo {
          total
        }
      }
    }
    """
    filters = {}
    if language:
        filters["language"] = [language]
    if category:
        filters["categories"] = [{"category": category}]

    variables = {"searchTerm": search_term, "filters": filters or None, "first": limit}
    result = graphql_request(query, variables, token=token)
    if "errors" in result:
        print("GraphQL-Fehler:", json.dumps(result["errors"], indent=2), file=sys.stderr)
        sys.exit(1)
    return result["data"]["podcasts"]


def main():
    parser = argparse.ArgumentParser(description="Podchaser podcast search for PR research")
    sub = parser.add_subparsers(dest="command", required=True)

    search_p = sub.add_parser("search", help="Search podcasts by keyword")
    search_p.add_argument("term", help="Search term, e.g. 'mental health'")
    search_p.add_argument("--language", help="2-letter language code, e.g. de, en")
    search_p.add_argument("--category", help="Podchaser category slug, e.g. business")
    search_p.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()
    env = load_env()
    token = get_access_token(env)

    if args.command == "search":
        results = search_podcasts(
            token, args.term, language=args.language, category=args.category, limit=args.limit
        )
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
