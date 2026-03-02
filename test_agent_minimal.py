#!/usr/bin/env python3
"""
Minimal Plus-Auto.ro Test Agent
For debugging GitHub Actions issues
"""

import requests
import json
import os
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_website_access():
    """Test if we can access plus-auto.ro"""
    logger.info("🌐 Testing plus-auto.ro access...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get("https://plus-auto.ro/", headers=headers, timeout=15)
        logger.info(f"✅ Response code: {response.status_code}")
        logger.info(f"📄 Content length: {len(response.text)}")
        
        if "autoturisme" in response.text.lower():
            logger.info("✅ Romanian automotive content detected")
            return True
        else:
            logger.warning("⚠️ No automotive content detected")
            return False
            
    except Exception as e:
        logger.error(f"❌ Website access failed: {e}")
        return False

def test_email_config():
    """Test email configuration"""
    logger.info("📧 Testing email configuration...")
    
    email_password = os.getenv('EMAIL_PASSWORD')
    sender_email = os.getenv('SENDER_EMAIL') 
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    
    if not email_password:
        logger.error("❌ EMAIL_PASSWORD not set")
        return False
    if not sender_email:
        logger.error("❌ SENDER_EMAIL not set")
        return False
    if not recipient_email:
        logger.error("❌ RECIPIENT_EMAIL not set")
        return False
        
    logger.info("✅ All email environment variables set")
    return True

def send_test_email():
    """Send a simple test email"""
    logger.info("📤 Sending test email...")
    
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        email_password = os.getenv('EMAIL_PASSWORD')
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Plus-Auto.ro Agent Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        body = f"""
🧪 GITHUB ACTIONS TEST SUCCESSFUL!

✅ Agent execution: Working
✅ Website access: Tested  
✅ Email delivery: Working
⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This confirms your agent can run successfully in GitHub Actions.
Ready for full deployment! 🚀
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        server.send_message(msg)
        server.quit()
        
        logger.info("✅ Test email sent successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Email sending failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🧪 Starting Plus-Auto.ro Agent Test")
    logger.info("="*50)
    
    success_count = 0
    total_tests = 3
    
    # Test 1: Website access
    if test_website_access():
        success_count += 1
        
    # Test 2: Email configuration  
    if test_email_config():
        success_count += 1
        
    # Test 3: Email sending
    if send_test_email():
        success_count += 1
    
    logger.info("="*50)
    logger.info(f"🎯 TEST RESULTS: {success_count}/{total_tests} passed")
    
    if success_count == total_tests:
        logger.info("✅ ALL TESTS PASSED - Agent ready for deployment!")
        return 0
    else:
        logger.error(f"❌ {total_tests - success_count} tests failed")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
