from typing import Dict, Any, Optional, Union
import json
import requests
from datetime import datetime

class DocumentProcessor:
    def __init__(
        self,
        api_endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        default_metadata: Optional[Dict[str, Any]] = None
    ):
        self.api_endpoint = api_endpoint
        self.headers = headers or {}
        self.default_metadata = default_metadata or {}

    def process_file(self, file_path: str, callback=None) -> None:
        """Process JSONL file and send documents."""
        with open(file_path) as f:
            for line in f:
                try:
                    data = json.loads(line)
                    processed_doc = self.prepare_document(data)
                    
                    if callback:
                        # Allow custom handling of processed document
                        callback(processed_doc)
                    else:
                        # Default sending behavior
                        self.send_document(processed_doc)
                except Exception as e:
                    print(f"Error processing line: {e}")

    def prepare_document(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare document from raw data."""
        # Extract content
        raw_content = data.get('content', None)
        content = self._process_content(raw_content)
        
        # Get title
        title = data.get('page_title')
        
        if not content or not title:
            raise ValueError("Missing required content or title")

        # Determine classification
        classification = self._determine_classification(data.get('url', ''))

        # Combine with default metadata and return
        metadata = {
            **self.default_metadata,
            "url": data.get('url', ''),
            "h2_headers": data.get('h2_headers', []),
        }

        return {
            "classification": classification,
            "contents": content,
            "name": title,
            "metadata": metadata
        }

    def send_document(self, document: Dict[str, Any]) -> requests.Response:
        """Send document to API endpoint."""
        response = requests.post(
            self.api_endpoint,
            json=document,
            headers=self.headers
        )
        return response

    def _process_content(self, raw_content: Union[list, str, None]) -> str:
        """Process raw content into string."""
        if isinstance(raw_content, list):
            return ' '.join(str(c) for c in raw_content)
        elif isinstance(raw_content, str):
            return raw_content
        raise ValueError(f"Unexpected content type: {type(raw_content)}")

    def _determine_classification(self, url: str) -> str:
        """Determine document classification based on URL."""
        return "developer" if "developer.rocket.chat" in url else "user"

# Example usage:
if __name__ == "__main__":
    # Configuration
    processor = DocumentProcessor(
        api_endpoint="http://{{host}}/documents",
        headers={
            "Content-Type": "application/json",
            # Add any other headers here
        },
        default_metadata={
            "doc_expiry": "2024-12-31T23:59:59Z",
            "source": "Rocket.Chat",
            # Add any other default metadata here
        }
    )

    # Process file
    processor.process_file("rocket_chat_docs.jsonl")

    # Or with custom callback
    def custom_handler(doc):
        print(f"Processing document: {doc['name']}")
        # Add custom logic here
    
    processor.process_file("rocket_chat_docs.jsonl", callback=custom_handler)