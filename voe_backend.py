from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from twilio.rest import Client
import random
import os
from dotenv import load_dotenv

# Load local environment variables (for local testing)
load_dotenv()

app = FastAPI(title="Vault Optix Engine - WhatsApp API")

# Allow your local HTML file to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# TWILIO CREDENTIALS (Securely fetched)
# ==========================================
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class OTPRequest(BaseModel):
    phone_number: str  # e.g., "+919876543210"

@app.post("/voe/send-otp")
async def send_whatsapp_otp(request: OTPRequest):
    try:
        # 1. Generate a random 4-digit OTP
        otp_code = random.randint(1000, 9999)
        
        # 2. Format the message exactly how a premium D2C brand would
        message_body = f"🔒 *Vault OS Verification*\n\nYour secure checkout code is: *{otp_code}*\n\nPlease enter this code in the cart to confirm your Cash on Delivery order."

        # 3. Send the WhatsApp Message
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=f"whatsapp:{request.phone_number}"
        )
        
        return {
            "status": "success", 
            "message": "OTP sent via WhatsApp!",
            "message_sid": message.sid,
            "simulated_otp": otp_code # We return it just so you can log it in the console for the demo
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
