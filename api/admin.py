"""GET /api/admin/session — Vercel serverless (read-only)"""
import json

def handler(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json; charset=utf-8"

    if request.method == "OPTIONS":
        response.status_code = 204
        return response

    response.status_code = 200
    response.body = json.dumps({
        "authenticated": False,
        "message": "Admin panel faqat local versiyada ishlaydi: python3 app.py"
    })
    return response
