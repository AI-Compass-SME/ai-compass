import os
import json
import logging
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)

SENDER_EMAIL = "info@the-ai-compass.de"
SENDER_NAME = "AI Compass"

# Brand colors matching the webapp
_GRADIENT_FROM = "#2563eb"   # blue-600  (same as nav CTA gradient start)
_GRADIENT_TO   = "#9333ea"   # purple-600 (same as nav CTA gradient end)
_INDIGO        = "#4f46e5"   # indigo-600 — accent / links
_SLATE_900     = "#0f172a"
_SLATE_700     = "#334155"
_SLATE_500     = "#64748b"
_SLATE_100     = "#f1f5f9"
_SLATE_50      = "#f8fafc"
_WHITE         = "#ffffff"
_BORDER        = "#e2e8f0"

def _get_logo_img_tag() -> str:
    """Returns an <img> tag with the logo hosted on the live Vercel/Render frontend for maximum email compatibility."""
    # Using the live unauthenticated URL ensures email clients (Gmail, Outlook) download it properly via their proxies
    logo_url = "https://kmwe38clpa2nailq.public.blob.vercel-storage.com/ai_compass_logo.png"
    return f'<img src="{logo_url}" width="32" height="32" alt="AI Compass Logo" style="display:block;border-radius:6px;"/>'

def _build_email_wrapper(body_html: str, t: dict, footer_extra: str = "") -> str:
    """Builds the full premium email shell with header and footer."""
    
    footer_links = f"""
      <p style="margin:0 0 12px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:12px;color:{_SLATE_500};">
        <a href="https://the-ai-compass.de" style="color:{_INDIGO};text-decoration:none;margin:0 8px;">{t['nav_home']}</a> &bull;
        <a href="https://the-ai-compass.de/imprint" style="color:{_INDIGO};text-decoration:none;margin:0 8px;">{t['nav_imprint']}</a> &bull;
        <a href="https://the-ai-compass.de/privacy-policy" style="color:{_INDIGO};text-decoration:none;margin:0 8px;">{t['nav_privacy']}</a>
      </p>
      {footer_extra}
      <p style="margin:8px 0 0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:11px;color:{_SLATE_500};">
        &copy; 2026 AI Compass &bull; the-ai-compass.de &bull; {t['rights']}
      </p>
    """

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>AI Compass</title>
</head>
<body style="margin:0;padding:0;background-color:{_SLATE_100};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <!-- Outer wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{_SLATE_100};padding:40px 16px;">
    <tr>
      <td align="center">
        <!-- Email card -->
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:{_WHITE};border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

          <!-- ===== HEADER ===== -->
          <tr>
            <td style="background:linear-gradient(135deg,{_GRADIENT_FROM} 0%,{_GRADIENT_TO} 100%);padding:28px 36px;">
              <table cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td>
                    <table cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td valign="middle" style="padding-right:10px;">
                          {_get_logo_img_tag()}
                        </td>
                        <td valign="middle">
                          <span style="font-size:20px;font-weight:700;color:{_WHITE};letter-spacing:-0.3px;">AI Compass</span>
                        </td>
                      </tr>
                    </table>
                  </td>
                  <td align="right" valign="middle">
                    <span style="font-size:12px;color:rgba(255,255,255,0.75);letter-spacing:1px;text-transform:uppercase;font-weight:600;">{t['header_suffix']}</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- ===== BODY ===== -->
          <tr>
            <td style="padding:40px 36px 32px;">
              {body_html}
            </td>
          </tr>

          <!-- ===== FOOTER ===== -->
          <tr>
            <td style="background-color:{_SLATE_50};border-top:1px solid {_BORDER};padding:24px 36px;text-align:center;">
              {footer_links}
            </td>
          </tr>

        </table>
        <!-- / Email card -->

        <!-- Sub-footer note -->
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;margin-top:20px;">
          <tr>
            <td align="center" style="padding:0 16px;">
              <p style="font-size:11px;color:{_SLATE_500};margin:0;">
                {t.get('footer_note', '')}
              </p>
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>
</body>
</html>
"""


def _cta_button(label: str, href: str) -> str:
    """Renders a premium gradient CTA button."""
    return f"""
<table cellpadding="0" cellspacing="0" border="0" style="margin:32px 0;">
  <tr>
    <td align="center" style="border-radius:12px;background:linear-gradient(135deg,{_GRADIENT_FROM} 0%,{_GRADIENT_TO} 100%);box-shadow:0 8px 20px rgba(79,70,229,0.35);">
      <a href="{href}" target="_blank"
         style="display:inline-block;padding:14px 36px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;font-weight:700;color:{_WHITE};text-decoration:none;border-radius:12px;letter-spacing:0.2px;">
        {label} &nbsp;&#8594;
      </a>
    </td>
  </tr>
</table>
"""


def _divider() -> str:
    return f'<hr style="border:none;border-top:1px solid {_BORDER};margin:28px 0;"/>'


class EmailService:
    @staticmethod
    def _send_brevo_email(data: dict) -> bool:
        # Read from pydantic settings so it's properly sourced from .env or env vars
        from config import get_settings
        brevo_api_key = get_settings().BREVO_API_KEY
        if not brevo_api_key:
            logger.error("BREVO_API_KEY environment variable is not set. Cannot dispatch emails.")
            raise ValueError("Email Service Configuration Error: API Key missing.")
            
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": brevo_api_key,
            "content-type": "application/json"
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                if response.status in (200, 201, 202):
                    return True
                else:
                    logger.error(f"Brevo API failed with status {response.status}")
                    raise RuntimeError(f"Email Dispatch Failed (Status {response.status})")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8', errors='ignore')
            logger.error(f"Brevo HTTP Error: {e.code} - {error_body}")
            raise RuntimeError("Upstream Email Provider Error") from e
        except Exception as e:
            logger.error(f"Fatal exception calling Brevo: {e}")
            raise RuntimeError("Email Service Unavailable") from e

    @staticmethod
    def send_verification_email(to_email: str, company_name: str, verification_link: str, lang: str = 'en') -> bool:
        t = {
            'en': {
                'title': f"Welcome, {company_name}! 🎉",
                'subtitle': "Your AI Maturity Assessment is complete and your personalised strategic report is ready.",
                'includes': "Your report includes",
                'item1': "AI Maturity Score",
                'item2': "Strategic Gap Analysis",
                'item3': "3-Phase Roadmap",
                'item4': "Industry Benchmark",
                'item5': "Cluster Profile",
                'item6': "Executive Briefing + PDF",
                'cta_text': "Click the button below to <strong>verify your email</strong> and instantly access your interactive dashboard and downloadable PDF report.",
                'btn': "Verify Email & View My Report",
                'disclaimer': "This link is secure and unique to your assessment. If you didn't take an AI Compass assessment, you can safely ignore this email.",
                'subject': f"[Action Required] Verify your email to access your AI Compass Report — {company_name}",
                'footer_note': "You received this email because an AI Compass assessment was completed using this address.<br/>If this wasn't you, simply ignore this email.",
                'nav_home': "Home",
                'nav_imprint': "Imprint",
                'nav_privacy': "Privacy Policy",
                'rights': "All rights reserved.",
                'header_suffix': "Strategic AI Assessment"
            },
            'de': {
                'title': f"Willkommen beim AI Compass!",
                'subtitle': "Ihre maßgeschneiderte Analyse und strategische Roadmap für belastbare Entscheidungen und einen nachhaltigen Wettbewerbsvorteil liegen nun bereit.",
                'includes': "IHR BERICHT ENTHÄLT",
                'item1': "Individueller Reifegrad-Score",
                'item2': "Strategische Roadmap",
                'item3': "KI-Profil",
                'item4': "Gap-Analyse",
                'item5': "Exklusiver Branchen-Benchmark",
                'item6': "Management-Briefing & PDF-Export",
                'cta_text': "Klicken Sie auf den Button unten, um Ihre E-Mail zu bestätigen und sofortigen Zugriff auf Ihre Analyse sowie den vollständigen Report zu erhalten:",
                'btn': "Jetzt Analyse und Roadmap öffnen",
                'disclaimer': "Dieser Link ist exklusiv für Ihr Assessment generiert worden. Falls Sie keine KI-Bewertung angefordert haben, können Sie diese Nachricht einfach ignorieren. Ihre Daten werden in diesem Fall nicht weiter verarbeitet.",
                'subject': f"[Aktion erforderlich] E-Mail bestätigen & Ihren AI Compass-Bericht abrufen — {company_name}",
                'footer_note': "Sie haben diese E-Mail erhalten, weil ein AI Compass Assessment unter dieser Adresse abgeschlossen wurde.<br/>Falls Sie dies nicht waren, ignorieren Sie diese E-Mail einfach.",
                'nav_home': "Startseite",
                'nav_imprint': "Impressum",
                'nav_privacy': "Datenschutz",
                'rights': "Alle Rechte vorbehalten.",
                'header_suffix': "Strategische KI-Analyse"
            }
        }
        
        # fallback to EN if language is unmatched
        lang_code = lang.split('-')[0].lower()
        active_t = t.get(lang_code, t['en'])

        body = f"""
<h1 style="margin:0 0 6px;font-size:26px;font-weight:800;color:{_SLATE_900};letter-spacing:-0.5px;">
  {active_t['title']}
</h1>
<p style="margin:0 0 24px;font-size:15px;color:{_SLATE_500};line-height:1.5;">
  {active_t['subtitle']}
</p>

<!-- Highlight card -->
<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background:linear-gradient(135deg,rgba(37,99,235,0.06) 0%,rgba(147,51,234,0.06) 100%);
              border:1px solid {_BORDER};border-radius:12px;margin-bottom:12px;">
  <tr>
    <td style="padding:22px 24px;">
      <p style="margin:0 0 6px;font-size:13px;font-weight:700;color:{_INDIGO};text-transform:uppercase;letter-spacing:1px;">{active_t['includes']}</p>
      <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td width="50%" style="padding:6px 0;font-size:13px;color:{_SLATE_700};">&#10003;&nbsp; {active_t['item1']}</td>
          <td width="50%" style="padding:6px 0;font-size:13px;color:{_SLATE_700};">&#10003;&nbsp; {active_t['item2']}</td>
        </tr>
        <tr>
          <td style="padding:6px 0;font-size:13px;color:{_SLATE_700};">&#10003;&nbsp; {active_t['item3']}</td>
          <td style="padding:6px 0;font-size:13px;color:{_SLATE_700};">&#10003;&nbsp; {active_t['item4']}</td>
        </tr>
        <tr>
          <td style="padding:6px 0;font-size:13px;color:{_SLATE_700};">&#10003;&nbsp; {active_t['item5']}</td>
          <td style="padding:6px 0;font-size:13px;color:{_SLATE_700};">&#10003;&nbsp; {active_t['item6']}</td>
        </tr>
      </table>
    </td>
  </tr>
</table>

<p style="margin:20px 0 4px;font-size:15px;color:{_SLATE_700};line-height:1.6;">
  {active_t['cta_text']}
</p>

{_cta_button(active_t['btn'], verification_link)}

{_divider()}

<p style="margin:0;font-size:12px;color:{_SLATE_500};line-height:1.6;">
  {active_t['disclaimer']}
</p>
"""
        html = _build_email_wrapper(body, t=active_t)
        
        data = {
            "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "to": [{"email": to_email, "name": company_name}],
            "subject": active_t['subject'],
            "htmlContent": html
        }
        return EmailService._send_brevo_email(data)

    @staticmethod
    def send_results_email_with_pdf(to_email: str, company_name: str, results_link: str, pdf_bytes: bytes, lang: str = 'en') -> bool:
        t = {
            'en': {
                'title': "Your AI Maturity Report is Ready &#128196;",
                'subtitle': f"Hello <strong>{company_name}</strong>, thank you for verifying your email. Your full strategic AI maturity report is attached to this email as a PDF.",
                'inside': "What's inside your PDF",
                'item1': "Maturity Score Overview",
                'item2': "Critical Gap Analysis",
                'item3': "3-Phase Action Roadmap",
                'item4': "Industry Benchmarking",
                'item5': "Cluster Profile",
                'item6': "Executive Briefing",
                'btn': "View Report",
                'next_steps': "Next steps",
                'next_desc': "Review your roadmap with your leadership team and identify the highest-impact actions for your next quarter. If you'd like expert guidance implementing your strategy, our team is available for a free consultation.",
                'confidential': f"This is a confidential report prepared exclusively for {company_name}. Your secure dashboard link is permanent — bookmark it for future reference.",
                'secure_dash': "Your secure dashboard:",
                'subject': f"Your AI Compass Strategic Report — {company_name}",
                'nav_home': "Home",
                'nav_imprint': "Imprint",
                'nav_privacy': "Privacy Policy",
                'rights': "All rights reserved.",
                'footer_note': "",
                'header_suffix': "Strategic AI Assessment"
            },
            'de': {
                'title': "Ihr KI-Reifegradbericht ist fertig &#128196;",
                'subtitle': f"Hallo <strong>{company_name}</strong>, danke für die Verifizierung Ihrer E-Mail. Ihr vollständiger strategischer KI-Reifegradbericht ist dieser E-Mail als PDF beigefügt.",
                'inside': "Was in Ihrem PDF enthalten ist",
                'item1': "Individueller Reifegrad-Score",
                'item2': "Strategische Gap-Analyse",
                'item3': "Strategische Roadmap & Empfehlungen",
                'item4': "Branchen-Benchmarking",
                'item5': "KI-Profil",
                'item6': "AI-Compass Strategisches Briefing",
                'cta_pre': "Sie können jederzeit über Ihren sicheren, dauerhaften Link unten auf Ihr <strong>interaktives Live-Dashboard</strong> zugreifen:",
                'btn': "Bericht ansehen",
                'next_steps': "Nächste Schritte",
                'next_desc': "Überprüfen Sie Ihre Roadmap mit Ihrem Führungsteam und identifizieren Sie die Maßnahmen mit den höchsten Auswirkungen für das nächste Quartal. Wenn Sie fachkundige Anleitung bei der Umsetzung Ihrer Strategie wünschen, steht Ihnen unser Team für eine kostenlose Beratung zur Verfügung.",
                'confidential': f"Dies ist ein vertraulicher Bericht, der exklusiv für {company_name} erstellt wurde. Ihr sicherer Dashboard-Link ist permanent — speichern Sie ihn für künftige Referenzen.",
                'secure_dash': "Ihr sicheres Dashboard:",
                'subject': f"Ihr strategischer AI Compass-Bericht — {company_name}",
                'nav_home': "Startseite",
                'nav_imprint': "Impressum",
                'nav_privacy': "Datenschutz",
                'rights': "Alle Rechte vorbehalten.",
                'footer_note': "",
                'header_suffix': "Strategische KI-Analyse"
            }
        }
        lang_code = lang.split('-')[0].lower()
        active_t = t.get(lang_code, t['en'])
        
        import base64
        b64_pdf = base64.b64encode(pdf_bytes).decode('ascii')

        body = f"""
<h1 style="margin:0 0 6px;font-size:26px;font-weight:800;color:{_SLATE_900};letter-spacing:-0.5px;">
  {active_t['title']}
</h1>
<p style="margin:0 0 24px;font-size:15px;color:{_SLATE_500};line-height:1.5;">
  {active_t['subtitle']}
</p>

<!-- What's inside card -->
<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background:{_SLATE_50};border:1px solid {_BORDER};border-radius:12px;margin-bottom:8px;">
  <tr>
    <td style="padding:20px 24px;">
      <p style="margin:0 0 12px;font-size:13px;font-weight:700;color:{_INDIGO};text-transform:uppercase;letter-spacing:1px;">{active_t['inside']}</p>
      <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td width="50%" style="padding:5px 0;font-size:13px;color:{_SLATE_700};">📊&nbsp; {active_t['item1']}</td>
          <td width="50%" style="padding:5px 0;font-size:13px;color:{_SLATE_700};">🔍&nbsp; {active_t['item2']}</td>
        </tr>
        <tr>
          <td style="padding:5px 0;font-size:13px;color:{_SLATE_700};">🗺️&nbsp; {active_t['item3']}</td>
          <td style="padding:5px 0;font-size:13px;color:{_SLATE_700};">📈&nbsp; {active_t['item4']}</td>
        </tr>
        <tr>
          <td style="padding:5px 0;font-size:13px;color:{_SLATE_700};">🏷️&nbsp; {active_t['item5']}</td>
          <td style="padding:5px 0;font-size:13px;color:{_SLATE_700};">📋&nbsp; {active_t['item6']}</td>
        </tr>
      </table>
    </td>
  </tr>
</table>

<p style="margin:20px 0 4px;font-size:15px;color:{_SLATE_700};line-height:1.6;">
  {active_t['cta_pre']}
</p>

{_cta_button(active_t['btn'], results_link)}

{_divider()}

<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background:linear-gradient(135deg,rgba(37,99,235,0.05) 0%,rgba(147,51,234,0.05) 100%);
              border:1px solid {_BORDER};border-left:4px solid {_INDIGO};border-radius:8px;">
  <tr>
    <td style="padding:16px 20px;">
      <p style="margin:0 0 4px;font-size:13px;font-weight:700;color:{_SLATE_900};">💡 {active_t['next_steps']}</p>
      <p style="margin:0;font-size:13px;color:{_SLATE_700};line-height:1.6;">
        {active_t['next_desc']}
      </p>
    </td>
  </tr>
</table>

<p style="margin:24px 0 0;font-size:12px;color:{_SLATE_500};line-height:1.6;">
  {active_t['confidential']}
</p>
"""
        footer_extra = f"""
      <p style="margin:8px 0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:12px;color:{_SLATE_500};">
        {active_t['secure_dash']} <a href="{results_link}" style="color:{_INDIGO};text-decoration:none;">{results_link}</a>
      </p>
"""
        html = _build_email_wrapper(body, t=active_t, footer_extra=footer_extra)
        
        data = {
            "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "to": [{"email": to_email, "name": company_name}],
            "subject": active_t['subject'],
            "htmlContent": html,
            "attachment": [
                {
                    "content": b64_pdf,
                    "name": f"AI_Compass_Strategischer_Bericht_{company_name.replace(' ', '_')}.pdf" if lang_code == 'de' else f"AI_Compass_Report_{company_name.replace(' ', '_')}.pdf"
                }
            ]
        }
        return EmailService._send_brevo_email(data)


email_service = EmailService()
