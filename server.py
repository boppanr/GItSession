import os, json, requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

LAMBDA_MCP_URL = os.environ["LAMBDA_MCP_URL"].rstrip("/")

app = FastAPI()

@app.get("/mcp")
def tools():
    payload = requests.get(LAMBDA_MCP_URL + "/").json()
    tools = payload.get("tools", [])
    actions = payload.get("actions")
    if not actions:
        actions = [{
            "name": t["name"],
            "description": t.get("description", ""),
            "parameters": t.get("input_schema", {
                "type": "object",
                "properties": {},
                "required": []
            })
        } for t in tools]
    return {"actions": actions, "tools": tools}

@app.post("/mcp")
async def invoke(req: Request):
    body = await req.json()
    r = requests.post(LAMBDA_MCP_URL + "/", json=body, timeout=120)
    return JSONResponse(status_code=r.status_code, content=r.json() if r.content else {})
