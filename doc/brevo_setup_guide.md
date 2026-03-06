# Brevo API Key Setup Guide for AI Compass

This guide walks you through creating a Brevo account, verifying your sender email (`info@the-ai-compass.de`), generating an API key, and connecting it to your AI Compass application.

## Step 1: Create a Brevo Account
1. Go to [https://www.brevo.com/](https://www.brevo.com/) and click **Sign Up Free**.
2. Fill in your details (name, company size, etc.). You can use a free tier account for this project, which allows up to 300 emails per day.
3. Verify your phone number and complete the onboarding questionnaire.

## Step 2: Add and Verify Your Sender Email
Before Brevo will let you send emails, you must prove you own the `info@the-ai-compass.de` address.
1. In the Brevo dashboard, click on your **Profile name** in the top right corner.
2. Select **Senders, Domains & Dedicated IPs**.
3. Under the **Senders** tab, click **Add a sender**.
4. Enter the following:
   * **From Name:** AI Compass
   * **From Email:** info@the-ai-compass.de
5. Click **Save**.
6. Brevo will send a confirmation email to `info@the-ai-compass.de`. Open that email inbox and click the verification link inside the email. 
   *(Note: You must have access to the `info@the-ai-compass.de` inbox to click this link.)*

## Step 3: Authenticate Your Domain (Highly Recommended for Deliverability)
To ensure your emails don't end up in users' spam folders, you need to authenticate `the-ai-compass.de`.
1. In Brevo, go to **Senders, Domains & Dedicated IPs** -> **Domains**.
2. Click **Add a domain** and enter `the-ai-compass.de`.
3. Brevo will provide you with several DNS records (TXT records).
4. Go to your domain registrar (where you host `the-ai-compass.de` DNS settings).
5. Add the provided DNS TXT records exactly as Brevo displays them.
6. Return to Brevo and click **Verify & Authenticate**. It may take a few minutes (or up to 24 hours) for the DNS to propagate.

## Step 4: Generate Your API Key
Once your sender is verified, you can create the API key for the backend application.
1. In the top right corner of the Brevo dashboard, click on your **Profile name**.
2. Select **SMTP & API**.
3. Go to the **API keys** tab.
4. Click **Generate a new API key**.
5. Name your key something recognizable (e.g., `ai-compass-production-backend`).
6. Click **Generate**.
7. **Copy the API key immediately.** (It usually starts with `xkeysib-...`). You will not be able to see it again after you close the window.

## Step 5: Add the API Key to Your Application

### Local Development (Your Machine)
1. Open the file `Application_Prototype/mvp_v1/backend/.env` in your code editor.
2. Add your key like this:
   `BREVO_API_KEY=xkeysib-your-long-api-key-here`
3. Restart your local backend server using `./start.sh` or `start.bat`.

### Production (Render.com)
1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Select your backend Web Service.
3. Click on the **Environment** tab on the left sidebar.
4. Click **Add Environment Variable**.
5. Enter `BREVO_API_KEY` as the Key, and paste your actual API key as the Value.
6. Click **Save Changes**. (Render will automatically redeploy your application with the new key).

---
**Troubleshooting:**
If a user submits an assessment and receives a `500 Server Error`, it means either the `BREVO_API_KEY` is missing in the environment variables, or Brevo has rejected the email (often because the sender `info@the-ai-compass.de` is not verified in Step 2). Check the Render logs or your local terminal to see the exact rejection reason from Brevo.
