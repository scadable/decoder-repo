# Decoder Service

A lightweight Python service for decoding base64-encoded JSON payloads. This service provides a simple handler function that accepts encoded data, decodes it, and returns structured JSON output.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [For Users: Accessing & Using the Application](#for-users-accessing--using-the-application)
- [For Developers: Setup & Development](#for-developers-setup--development)
- [Deployment](#deployment)
- [Maintenance & Contributing](#maintenance--contributing)

---

## Overview

The Decoder Service is designed to process base64-encoded JSON payloads efficiently. It serves as a middleware component that can be integrated into larger data processing pipelines.

**Key Features:**
- Base64 payload decoding
- JSON parsing and validation
- Type-safe data handling
- Lightweight and extensible architecture

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Decoder Service                     │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │          Input (Dict[str, Any])            │    │
│  │  {                                         │    │
│  │    "payload": "<base64-encoded-string>"    │    │
│  │  }                                         │    │
│  └───────────────┬────────────────────────────┘    │
│                  │                                  │
│                  ▼                                  │
│  ┌────────────────────────────────────────────┐    │
│  │         Handler Function                   │    │
│  │  - Extracts payload                        │    │
│  │  - Base64 decode                           │    │
│  │  - JSON parse                              │    │
│  └───────────────┬────────────────────────────┘    │
│                  │                                  │
│                  ▼                                  │
│  ┌────────────────────────────────────────────┐    │
│  │         Output (Dict[str, Any])            │    │
│  │  {                                         │    │
│  │    "payload": "<base64-encoded-string>",   │    │
│  │    "data": { ... parsed JSON ... }         │    │
│  │  }                                         │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Component Breakdown:**

```
decoder-repo/
├── python/
│   └── main.py          # Core handler function
└── README.md            # This file
```

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.7+ | Core implementation |
| **Encoding** | Base64 | Payload encoding/decoding |
| **Data Format** | JSON | Data serialization |
| **Type Safety** | Python typing module | Type hints and validation |

**Dependencies:**
- `base64` (built-in): Base64 encoding/decoding
- `json` (built-in): JSON parsing and serialization
- `typing` (built-in): Type annotations

---

## For Users: Accessing & Using the Application

### Access Information

**Current Status:** Development/Integration Ready

This service is designed to be integrated as a module or function within your existing Python application or data processing pipeline.

### How to Use

#### Basic Usage

```python
from python.main import handler

# Prepare your data
input_data = {
    "payload": "eyJuYW1lIjogIkpvaG4gRG9lIiwgImFnZSI6IDMwfQ=="  # Base64 encoded JSON
}

# Process the data
result = handler(input_data)

# Access the decoded data
print(result["data"])  # {'name': 'John Doe', 'age': 30}
```

#### Input Format

The handler expects a dictionary with a `payload` key containing a base64-encoded JSON string:

```python
{
    "payload": "<base64-encoded-json-string>"
}
```

#### Output Format

The handler returns the input dictionary with an additional `data` key containing the parsed JSON:

```python
{
    "payload": "<base64-encoded-json-string>",
    "data": {
        # ... parsed JSON object ...
    }
}
```

#### Example Workflow

1. **Encode your JSON data** (if needed):
   ```python
   import base64
   import json

   original_data = {"name": "Jane Smith", "role": "Engineer"}
   encoded = base64.b64encode(json.dumps(original_data).encode("utf-8"))
   ```

2. **Call the handler**:
   ```python
   result = handler({"payload": encoded})
   ```

3. **Use the decoded data**:
   ```python
   user_name = result["data"]["name"]
   user_role = result["data"]["role"]
   ```

### Integration Examples

**AWS Lambda:**
```python
from python.main import handler as decode_handler

def lambda_handler(event, context):
    decoded_result = decode_handler(event)
    return {
        'statusCode': 200,
        'body': decoded_result["data"]
    }
```

**API Endpoint:**
```python
from flask import Flask, request, jsonify
from python.main import handler

app = Flask(__name__)

@app.route('/decode', methods=['POST'])
def decode():
    result = handler(request.json)
    return jsonify(result["data"])
```

---

## For Developers: Setup & Development

### Prerequisites

- Python 3.7 or higher
- Git

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd decoder-repo
   ```

2. **Verify Python version:**
   ```bash
   python --version  # Should be 3.7+
   ```

3. **No external dependencies required** - this project uses only Python standard library modules.

### Project Structure

```
decoder-repo/
├── python/
│   └── main.py          # Core handler implementation
│       └── handler()    # Main decoding function
├── README.md            # Documentation
└── .git/                # Version control
```

### Understanding the Code

#### `python/main.py`

The core handler function (`handler()`) performs three main operations:

1. **Extract the payload** from the input dictionary
2. **Decode the base64 string** to UTF-8 text
3. **Parse the JSON** and add it to the result

```python
def handler(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Default pass-through function that returns data unchanged.
    """
    encoded_payload = data.get("payload", "")
    decoded_str = base64.b64decode(encoded_payload).decode("utf-8")
    data["data"] = json.loads(decoded_str)
    return data
```

**Type Signature:**
- **Input:** `Dict[str, Any]` - Dictionary with at least a "payload" key
- **Output:** `Dict[str, Any]` - Original dict + "data" key with parsed JSON

### Development Workflow

#### Running Tests Locally

```bash
# Create a test script (test_handler.py)
cat > test_handler.py << 'EOF'
import base64
import json
from python.main import handler

def test_basic_decode():
    test_data = {"name": "Test User", "value": 123}
    encoded = base64.b64encode(json.dumps(test_data).encode("utf-8")).decode("utf-8")

    result = handler({"payload": encoded})

    assert result["data"]["name"] == "Test User"
    assert result["data"]["value"] == 123
    print("✓ Basic decode test passed")

if __name__ == "__main__":
    test_basic_decode()
EOF

# Run the test
python test_handler.py
```

#### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** to `python/main.py`

3. **Test your changes** with the test script above

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

#### Extending Functionality

To add new features or modify behavior:

1. **Add error handling:**
   ```python
   try:
       decoded_str = base64.b64decode(encoded_payload).decode("utf-8")
       data["data"] = json.loads(decoded_str)
   except (base64.binascii.Error, json.JSONDecodeError) as e:
       data["error"] = str(e)
   ```

2. **Add validation:**
   ```python
   if not encoded_payload:
       raise ValueError("Payload is required")
   ```

3. **Add additional transformations:**
   ```python
   data["metadata"] = {
       "decoded_at": datetime.now().isoformat(),
       "payload_size": len(encoded_payload)
   }
   ```

### Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Include docstrings for all functions
- Keep functions focused and single-purpose
- Write descriptive variable names

### Setting Up Development Environment

**Optional: Virtual Environment**
```bash
# Create virtual environment (optional, no dependencies needed)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Optional: Add Development Dependencies**
```bash
# Create requirements-dev.txt for linting/testing tools
cat > requirements-dev.txt << EOF
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
pytest>=7.0.0
EOF

pip install -r requirements-dev.txt
```

---

## Deployment

### Deployment Options

This service can be deployed in multiple ways depending on your infrastructure:

#### 1. AWS Lambda

```bash
# Package the function
cd python
zip -r ../lambda_function.zip main.py

# Upload to AWS Lambda via CLI
aws lambda create-function \
  --function-name decoder-service \
  --runtime python3.9 \
  --handler main.handler \
  --zip-file fileb://../lambda_function.zip \
  --role <your-lambda-role-arn>
```

#### 2. Docker Container

```dockerfile
# Create Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY python/ /app/python/

CMD ["python", "-c", "from python.main import handler; print(handler)"]
```

```bash
# Build and run
docker build -t decoder-service .
docker run decoder-service
```

#### 3. Direct Integration

Simply include the `python/` directory in your project and import the handler:

```python
from python.main import handler
```

### Hosting Information

**Recommended Platforms:**
- **AWS Lambda:** Serverless, pay-per-use, auto-scaling
- **Google Cloud Functions:** Similar to Lambda
- **Azure Functions:** Microsoft cloud equivalent
- **Self-hosted:** Any server with Python 3.7+

**Current Status:** Ready for deployment to any Python-compatible environment

---

## Maintenance & Contributing

### Regular Maintenance Tasks

1. **Monitor Python version compatibility** - Ensure compatibility with latest Python versions
2. **Review security updates** - Check for security advisories related to base64/JSON processing
3. **Update documentation** - Keep README in sync with code changes
4. **Test with real-world payloads** - Validate against actual use cases

### Contributing Guidelines

We welcome contributions! Here's how you can help:

#### Reporting Issues

1. Check if the issue already exists
2. Provide a clear description
3. Include sample input/output demonstrating the issue
4. Specify your Python version and environment

#### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with clear, focused commits
4. **Test thoroughly** with various inputs
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description

#### Pull Request Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] Type hints are included for new functions
- [ ] Docstrings are added/updated
- [ ] Changes are tested with sample data
- [ ] README is updated if functionality changes
- [ ] Commit messages are clear and descriptive

### Common Modifications

#### Adding Validation

```python
def handler(data: Dict[str, Any]) -> Dict[str, Any]:
    if "payload" not in data:
        raise ValueError("Missing 'payload' key in input data")

    encoded_payload = data.get("payload", "")
    if not encoded_payload:
        raise ValueError("Payload cannot be empty")

    # ... rest of the function
```

#### Adding Logging

```python
import logging

logger = logging.getLogger(__name__)

def handler(data: Dict[str, Any]) -> Dict[str, Any]:
    logger.info(f"Processing payload of length {len(data.get('payload', ''))}")
    # ... rest of the function
    logger.info("Payload processed successfully")
    return data
```

#### Supporting Multiple Encoding Types

```python
def handler(data: Dict[str, Any], encoding: str = "base64") -> Dict[str, Any]:
    encoded_payload = data.get("payload", "")

    if encoding == "base64":
        decoded_str = base64.b64decode(encoded_payload).decode("utf-8")
    elif encoding == "hex":
        decoded_str = bytes.fromhex(encoded_payload).decode("utf-8")
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")

    data["data"] = json.loads(decoded_str)
    return data
```

### Getting Help

- **Issues:** Create an issue in the repository
- **Questions:** Reach out to the development team
- **Documentation:** This README and inline code comments

### Version History

See commit history for detailed changes:
```bash
git log --oneline
```

---

## License

[Specify your license here]

## Contact

[Specify contact information or support channels here]
