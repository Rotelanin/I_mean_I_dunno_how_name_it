from fastapi import FastAPI, WebSocket, BackgroundTasks, Form
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
import json
import asyncio
import os

app = FastAPI()

SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str

async def send_email(email: str, subject: str, message: str):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = email
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, email, msg.as_string())
    except Exception as e:
        print(f"Email sending failed: {e}")

@app.post("/send-email/")
async def send_email_endpoint(
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    background_tasks: BackgroundTasks = None
):
    background_tasks.add_task(send_email, email, subject, message)
    return {"message": "Email is being sent"}

clients = []

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.dumps({"type": "notification", "content": data})
            await asyncio.gather(*[client.send_text(message) for client in clients])
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        clients.remove(websocket)
