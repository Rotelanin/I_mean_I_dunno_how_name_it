from fastapi import FastAPI, WebSocket, BackgroundTasks, Form
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
import json
import asyncio
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt

app = FastAPI()

SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

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
    token: str = Depends(verify_token),
    background_tasks: BackgroundTasks = None
):
    background_tasks.add_task(send_email, email, subject, message)
    return {"message": "Email is being sent"}

clients = []

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket, token: str):
    verify_token(token)  # Verify JWT token before accepting connection
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
