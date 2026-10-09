from fastapi import FastAPI, Request
from datetime import datetime
import requests

from requests.auth import HTTPDigestAuth

app = FastAPI(
	title = "Lock",
	version = "0.0.1"
)

events = []

@app.get("/")
def	root():
	return {
		"status": "online",
		"Device": "Lock",
		"service": "Hikvision Test API"
	}


# ============================================================
# RECEBER EVENTOS DA HIKVISION
# ============================================================
@app.put("/hikvision/event")
async def	hikvisionEvent(request: Request):
	body = await request.boby()

	event = {
		"received_at": datetime.now().isoformat(),
		"header": dict(request.headers),
		"body": body.decode("utf-8", errors="Reaplace")
	}

	events.append(event)

	print("\n========== EVENTO HIKVISION ==========")
	print(event)
	print("======================================\n")

	return {
		"success": True,
		"message": "Evento recebido"
	}


@app.post("/hikvision/events")
async def	hikvisionEvents(request: Request):
	body = await request.body()

	event = {
		"received_at": datetime.now().isoformat(),
		"header": dict(request.headers),
		"body": body.decode("utf-8", errors="Reaplace")
	}

	events.append(event)

	print("\n========== EVENTO HIKVISION ==========")
	print(event)
	print("======================================\n")

	return {
		"success": True,
		"message": "Evento recebido"
	}

@app.get("/events")
def	get_events():
	return {
		"total_events": len(events),
		"events": events
	}

@app.delete("/events")
def	clean_events():
	events.clear()

	return {
		"clean_events": True,
		"massager": "remuved events"
	}


# ============================================================
# ENVIAR REQUISIÇÃO PARA O CONTROLADOR HIKVISION
# ============================================================

@app.get("/hikvision/send")
async def	send_to_hikvision():
	ip: str = "192.168.1.248"
	port: int = 80
	user_name: str = "admin"
	password: str = "Doria00#"
	url = f"http://192.168.1.19:20480/ISAPI/AccessControl/RemoteControl/door/1"

	xml = """<?xml version="1.0" encoding="UTF-8"?>
<RemoteControlDoor xmlns="http://www.isapi.org/ver20/XMLSchema" version="2.0">
    <cmd>open</cmd>
</RemoteControlDoor>
"""

	try:
		response = requests.put(
			url,
			data = xml.encode("utf-8"),
			auth = HTTPDigestAuth(user_name, password),
			headers = {
				"Content-Type": "application/xml"
			},
			timeout = 10
		)

		return {
			"sucess": True,
			"status_code": response.status_code,
			"respose": response.text
		}
	except Exception as e:
		return {
			"sucess": False,
			"Error": str(e)
		}
