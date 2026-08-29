# Shopify Card Checker API

## Deployment
Deploy on Railway with one click.

## API Format
GET /shopify?cc=CARD&site=SITE&proxy=PROXY

### Parameters
| Parameter | Required | Format | Example |
|-----------|----------|--------|---------|
| cc | Yes | CC|MM|YYYY|CVV | 4111111111111111|12|2026|123 |
| site | Yes | Shopify URL | example.myshopify.com |
| proxy | No | ip:port:user:pass | 192.168.1.1:8080:user:pass |

### Example Request
GET https://your-app.railway.app/shopify?cc=4111111111111111|12|2026|123&site=example.myshopify.com

### Example Response
{
  "cc": "4111111111111111|12|2026|123",
  "site": "example.myshopify.com",
  "proxy": "None",
  "status": false,
  "response": "CARD_DECLINED",
  "gateway": "Shopify",
  "price": "0.00",
  "currency": "USD",
  "time": "3.45s"
}