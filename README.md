# DMARC Parser API

A Python Flask application that serves as a DMARC parser API. Parse a provided DMARC record and to check the current DNS DMARC record. Simple as that.

## Requirements

- **Python**: 3.9 or higher
- **Docker**
- **Docker Compose**

## Installation

### Environment Variables

```dotenv
PYTHONUNBUFFERED=1
FLASK_ENV=development
API_KEY=your_api_key
```

### Running the Application

#### Using Docker

1. **Build and Run the Application**

   ```bash
   docker-compose up --build
   ```

2. **Access the API**

   App root: `http://localhost:8080`.

## Usage

#### Parse DMARC Record

- **Endpoint**

  ```
  POST /parse_dmarc
  ```

- **Headers**

  ```http
  x-api-key: your_api_key
  Content-Type: application/json
  ```

- **Request Body**

  ```json
  {
    "dmarc_record": "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
  }
  ```

- **Response**

  ```json
  {
    "v": "DMARC1",
    "p": "none",
    "rua": "mailto:dmarc@example.com"
  }
  ```

- **Example with `curl`**

  ```bash
  curl -X POST \
       -H "Content-Type: application/json" \
       -H "x-api-key: your_api_key" \
       -d '{"dmarc_record": "v=DMARC1; p=none; rua=mailto:dmarc@example.com"}' \
       http://localhost:8080/parse_dmarc
  ```

#### Check DNS DMARC Record

- **Endpoint**

  ```
  GET /check_dmarc/<domain>
  ```

- **Headers**

  ```http
  x-api-key: your_api_key
  ```

- **Response**

  ```json
  {
    "v": "DMARC1",
    "p": "reject",
    "rua": "mailto:dmarc@example.com"
  }
  ```

- **Example with `curl`**

  ```bash
  curl -H "x-api-key: your_api_key" \
       http://localhost:8080/check_dmarc/example.com
  ```

## Contributing

I created this API for a personal project and wanted to publish it. Feel free to fork or contribute it. But please don't expect me to maintain it on ocassion.
