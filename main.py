"""ANSR Profile — PDF Generation & Email Delivery API
Deploy to Railway. Connects to: Vercel assessment → this API → Resend email → client inbox.

Endpoints:
  POST /generate-and-send  — Generate PDF + email it
  POST /generate-pdf       — Generate PDF only (return file)
  GET  /health             — Health check
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import tempfile, os, time, hashlib, hmac, json, logging

# Import the PDF generator
from pdf_generator import generate_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ansr-api")

app = FastAPI(title="ANSR Profile API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ansr-profile.vercel.app",
        "https://ansr-pulse.vercel.app",
        "http://localhost:5173",
    ],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════
# CONFIG — set these as Railway env vars
# ═══════════════════════════════════════
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "ELIA <care@eliaheals.com>")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "ansr-profile-2026")

# ═══════════════════════════════════════
# MODELS
# ═══════════════════════════════════════
class ProfileRequest(BaseModel):
    name: str
    email: Optional[str] = ""
    primary: str       # "velvetblade"
    secondary: str     # "heartwood"
    sensory: str       # "V", "A", "M", "S", "O", "D"
    scores: dict       # {"alertness": 4.3, ...}
    token: Optional[str] = ""

class HealthResponse(BaseModel):
    status: str
    version: str
    pdf_generator: str

# ═══════════════════════════════════════
# EMAIL DELIVERY via Resend
# ═══════════════════════════════════════
def send_email_with_pdf(to_email: str, name: str, pdf_path: str, profile_name: str):
    """Send PDF as email attachment via Resend API."""
    if not RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not set — skipping email")
        return False
    
    try:
        import base64
        import urllib.request
        
        with open(pdf_path, "rb") as f:
            pdf_data = base64.b64encode(f.read()).decode()
        
        first_name = name.split()[0] if name else "there"
        
        email_body = f"""<div style="font-family: Georgia, serif; color: #3A3530; max-width: 480px; margin: 0 auto; padding: 40px 20px;">
  <p style="font-size: 18px; letter-spacing: 0.3em; color: #1A1714; text-align: center; margin-bottom: 32px;">E L I A</p>
  <p style="font-size: 15px; line-height: 1.8; margin-bottom: 20px;">{first_name},</p>
  <p style="font-size: 15px; line-height: 1.8; margin-bottom: 20px;">Your ANSR Profile is attached.</p>
  <p style="font-size: 15px; line-height: 1.8; margin-bottom: 32px;">Read it slowly. Your nervous system found its way here. That matters.</p>
  <p style="font-size: 13px; color: #B0A494; line-height: 1.7; margin-bottom: 8px;">— Alexandre Olive</p>
  <p style="font-size: 13px; color: #B0A494; font-style: italic;">ELIA — Beauty That Heals</p>
</div>"""
        
        payload = {
            "from": FROM_EMAIL,
            "to": [to_email],
            "subject": f"Your ANSR Profile — {name}",
            "html": email_body,
            "attachments": [{
                "filename": f"ANSR-Profile-{name.replace(' ', '-')}.pdf",
                "content": pdf_data,
                "content_type": "application/pdf"
            }]
        }
        
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            logger.info(f"Email sent to {to_email}: {result}")
            return True
            
    except Exception as e:
        logger.error(f"Email failed for {to_email}: {e}")
        return False

# ═══════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════
@app.get("/health")
async def health():
    return HealthResponse(
        status="ok",
        version="1.0.0",
        pdf_generator="reportlab"
    )

@app.post("/generate-pdf")
async def generate_pdf_endpoint(data: ProfileRequest):
    """Generate PDF and return as download."""
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            from datetime import datetime
            date_str = datetime.now().strftime("%d %B %Y")
            
            result = generate_pdf(
                data.name, data.primary, data.secondary,
                data.scores, data.sensory, f.name, date_str
            )
            
            if not result:
                raise HTTPException(status_code=500, detail="PDF generation failed")
            
            return FileResponse(
                f.name,
                media_type='application/pdf',
                filename=f"ANSR-Profile-{data.name.replace(' ', '-')}.pdf"
            )
    except Exception as e:
        logger.error(f"PDF generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-and-send")
async def generate_and_send(data: ProfileRequest, background_tasks: BackgroundTasks):
    """Generate PDF, email it, return success."""
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False, dir='/tmp') as f:
            from datetime import datetime
            date_str = datetime.now().strftime("%d %B %Y")
            
            result = generate_pdf(
                data.name, data.primary, data.secondary,
                data.scores, data.sensory, f.name, date_str
            )
            
            if not result:
                raise HTTPException(status_code=500, detail="PDF generation failed")
            
            # Send email in background
            if data.email:
                profile_name = {
                    "sunfire": "Sunfire", "velvetblade": "Velvet Blade",
                    "eclipse": "Eclipse", "summerstorm": "Summer Storm",
                    "heartwood": "Heartwood", "newmoon": "New Moon"
                }.get(data.primary, data.primary)
                
                background_tasks.add_task(
                    send_email_with_pdf, data.email, data.name, f.name, profile_name
                )
            
            return JSONResponse({
                "status": "ok",
                "pdf_generated": True,
                "email_queued": bool(data.email),
                "profile": data.primary,
                "secondary": data.secondary
            })
            
    except Exception as e:
        logger.error(f"Generate-and-send error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
