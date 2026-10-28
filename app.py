import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from google import genai
from google.genai import types

from demo_application import DemoApplication


class GeminiEmbeddingModel:
    def __init__(self):
        self.client = genai.Client()

    def embed(self, text):
        result = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=text,
            config=types.EmbedContentConfig(output_dimensionality=768),
        )
        return result.embeddings[0].values


controller = DemoApplication.main(GeminiEmbeddingModel())


def match_to_dict(match):
    return {
        "title": match.getTitle(),
        "description": match.getDescription(),
        "match": match.getMatch(),
    }


class MovieHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)

        try:
            if parsed_url.path == "/movies/search":
                query = params.get("query", [""])[0]
                if not query:
                    return self.send_json(400, {"error": "query is required"})
                matches = controller.search(query)

            elif parsed_url.path == "/movies/similar":
                title = params.get("title", [""])[0]
                if not title:
                    return self.send_json(400, {"error": "title is required"})
                matches = controller.similar_movies(title)

            else:
                return self.send_json(404, {"error": "Not found"})

            self.send_json(200, [match_to_dict(match) for match in matches])
        except Exception as error:
            self.send_json(500, {"error": str(error)})

    def send_json(self, status, data):
        response = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), MovieHandler)
    print("Movie API running at http://127.0.0.1:8000")
    server.serve_forever()
