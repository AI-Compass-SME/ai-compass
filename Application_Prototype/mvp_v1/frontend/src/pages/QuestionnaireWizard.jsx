import React, { useEffect, useState, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { PageBackground } from '@/components/ui/PageBackground';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../lib/api';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Checkbox } from "@/components/ui/checkbox";
import { Slider } from "@/components/ui/slider";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, SkipForward, ArrowRight, CheckCircle2, Circle, Disc, Check, Menu, Compass } from 'lucide-react';
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

const getDimensionName = (q, lang) => {
    let name = lang === 'de' && q.dimension_name_de ? q.dimension_name_de : q.dimension_name;
    if (lang === 'de') {
        if (name === 'Datenbereitschaft und -kompetenz') return 'Datenreife & Datenkompetenz';
        if (name === 'Menschen & Kultur') return 'Mensch & Kultur';
        if (name === 'Strategie und Geschäftsvision') return 'Strategie & Zielbild';
        if (name === 'Anwendungsfälle und Geschäftswert') return 'Use Cases & Business Value';
        if (name === 'Governance und Compliance') return 'Governance & Compliance';
    }
    return name;
};

const formatAnswerText = (ans, lang, currentQ) => {
    let text = lang === 'de' && ans?.answer_text_de ? ans.answer_text_de : (ans?.answer_text || '');

    // Override for question 1 answers
    if (lang === 'de' && currentQ?.question_id === 1) {
        if (ans.answer_level === 1) return 'Nicht thematisiert';
        if (ans.answer_level === 2) return 'Reaktive Erwähnung (ad-hoc)';
        if (ans.answer_level === 3) return 'Fallweise Abstimmung zu konkreten Initiativen';
        if (ans.answer_level === 4) return 'Fester Bestandteil der Agenda';
        if (ans.answer_level === 5) return 'Zentraler Strategie-Treiber';
    }

    // Override for question 2 answers
    if (lang === 'de' && currentQ?.question_id === 2) {
        if (ans.answer_level === 1) return 'Keine formale Planung vorhanden';
        if (ans.answer_level === 2) return 'Informelle Ansätze und isolierte Einzelziele';
        if (ans.answer_level === 3) return 'Strukturierter Rahmenentwurf (Draft)';
        if (ans.answer_level === 4) return 'Verabschiedete Roadmap mit Meilensteinen';
        if (ans.answer_level === 5) return 'Ganzheitliche Strategie inkl. Budgetierung';
    }

    // Override for question 3 answers
    if (lang === 'de' && currentQ?.question_id === 3) {
        if (ans.answer_level === 1) return 'Keine dedizierte Budgetierung';
        if (ans.answer_level === 2) return 'Bedarfsorientierte Einzelfallprüfung';
        if (ans.answer_level === 3) return 'Projektbezogene Budgetallokation';
        if (ans.answer_level === 4) return 'Systematische Fachbereichs-Budgets';
        if (ans.answer_level === 5) return 'Strategische Investitionsplanung & ROI-Steuerung';
    }

    // Override for question 4 answers
    if (lang === 'de' && currentQ?.question_id === 4) {
        if (ans.answer_level === 1) return 'Bewusste Zurückhaltung';
        if (ans.answer_level === 2) return 'Gezielte Beobachtung bewährter Standards';
        if (ans.answer_level === 3) return 'Zeitnahe Adaption erfolgreicher Benchmarks';
        if (ans.answer_level === 4) return 'Frühzeitige Differenzierung durch Eigenentwicklung';
        if (ans.answer_level === 5) return 'Technologische Branchen-Dominanz';
    }

    // Override for question 5 answers
    if (lang === 'de' && currentQ?.question_id === 5) {
        if (ans.answer_level === 1) return 'Aktive Ablehnung';
        if (ans.answer_level === 2) return 'Abwartende Skepsis';
        if (ans.answer_level === 3) return 'Passive Akzeptanz';
        if (ans.answer_level === 4) return 'Aktive Mitwirkung';
        if (ans.answer_level === 5) return 'Hohe Eigeninitiative';
    }

    // Override for question 7 answers
    if (lang === 'de' && currentQ?.question_id === 7) {
        if (ans.answer_level === 1) return 'Keine: Aktuell finden keine KI-spezifischen Schulungen statt.';
        if (ans.answer_level === 2) return 'Ad-hoc: Punktuelle Angebote bei konkretem Bedarf (z. B. einzelne Webinare).';
        if (ans.answer_level === 3) return 'Reaktiv: Regelmäßige, aber unkoordinierte Formate (z. B. Workshops in Fachabteilungen).';
        if (ans.answer_level === 4) return 'Strukturiert: Geplante Weiterbildungsprogramme mit festen Lernpfaden.';
        if (ans.answer_level === 5) return 'Strategisch: Fest verankerte Kultur des kontinuierlichen Lernens („Lifelong Learning“).';
    }

    // Override for question 9 answers
    if (lang === 'de' && currentQ?.question_id === 9) {
        if (ans.answer_level === 1) return 'Vertriebs- & Transaktionsdaten (z. B. Historische Verkäufe, POS-Daten)';
        if (ans.answer_level === 2) return 'Kundeninteraktionsdaten (z. B. E-Mail-Verläufe, Chat-Logs, CRM-Notizen)';
        if (ans.answer_level === 3) return 'Digitale Nutzungsdaten (z. B. Website-Tracking, App-Interaktionen)';
        if (ans.answer_level === 4) return 'Kundenfeedback & Sentiment-Daten (z. B. Bewertungen, Umfragen, Rezensionen)';
        if (ans.answer_level === 5) return 'Produkt- & Maschinendaten (z. B. IoT-Sensoren, Logistik-Daten, Qualitätsdaten)';
        if (ans.answer_level === 6) return 'Finanz- & ERP-Stammdaten (z. B. Bestände, Kostenrechnung, Lieferantendaten)';
        if (ans.answer_level === 7) return 'Personal- & Organisationsdaten (z. B. Skill-Matrix, Kapazitäten, HR-Stamm)';
        if (ans.answer_level === 8) return 'Keine systematische Erfassung dieser Datentypen (Exklusive Option)';
    }

    // Override for question 10 answers
    if (lang === 'de' && currentQ?.question_id === 10) {
        if (ans.answer_level === 1) return 'On-Premise-Infrastruktur (Eigene Server vor Ort)';
        if (ans.answer_level === 2) return 'Cloud-Plattformen (z. B. AWS, Azure, Google Cloud)';
        if (ans.answer_level === 3) return 'CRM-Systeme (z. B. Salesforce, HubSpot, Microsoft Dynamics)';
        if (ans.answer_level === 4) return 'ERP-Systeme (z. B. SAP, Microsoft Dynamics, Infor)';
        if (ans.answer_level === 5) return 'E-Commerce- & Vertriebsplattformen (z. B. Shopify, Shopware)';
        if (ans.answer_level === 6) return 'Business Intelligence & Analytics (z. B. Power BI, Tableau)';
        if (ans.answer_level === 7) return 'Systemübergreifende Schnittstellen (APIs) zur Datenintegration';
        if (ans.answer_level === 8) return 'Keine der oben genannten Lösungen';
    }

    // Override for question 11 answers
    if (lang === 'de' && currentQ?.question_id === 11) {
        if (ans.answer_level === 1) return 'Fragmentiert & Inkonsistent';
        if (ans.answer_level === 2) return 'Digital, aber unstrukturiert';
        if (ans.answer_level === 3) return 'Punktuell bereinigt';
        if (ans.answer_level === 4) return 'Standardisiert & Systematisch';
        if (ans.answer_level === 5) return 'Hochwertig & Echtzeit-verfügbar';
    }

    // Override for question 12 answers
    if (lang === 'de' && currentQ?.question_id === 12) {
        if (ans.answer_level === 1) return 'Erfahrungsbasiert: Entscheidungen basieren primär auf Intuition und langjähriger Erfahrung.';
        if (ans.answer_level === 2) return 'Punktuelles Bewusstsein: Daten werden wahrgenommen, aber nur selten systematisch in Prozesse einbezogen.';
        if (ans.answer_level === 3) return 'Sicherer Umgang mit Kennzahlen: Standard-KPIs werden verstanden und regelmäßig zur Kontrolle genutzt.';
        if (ans.answer_level === 4) return 'Analytische Arbeitsweise: Das Team leitet eigenständig Erkenntnisse aus Daten ab, um Abläufe zu optimieren.';
        if (ans.answer_level === 5) return 'Datengesteuerte Kultur: Daten sind die primäre Grundlage für strategische und operative Entscheidungen.';
    }

    // Override for question 13 answers
    if (lang === 'de' && currentQ?.question_id === 13) {
        if (ans.answer_level === 1) return 'Ad-hoc & Intuitionsbasiert: Projekte starten oft ohne formelle Vorabprüfung von Datenreife oder Compliance.';
        if (ans.answer_level === 2) return 'Reaktive Bewertung: Fundierte Prüfungen erfolgen meist erst nach Projektstart, was oft zu Verzögerungen führt.';
        if (ans.answer_level === 3) return 'Informelle Vorabprüfung: Große Initiativen durchlaufen einen Basis-Check der Datenlage und rechtlichen Hürden.';
        if (ans.answer_level === 4) return 'Strukturierter Gate-Prozess: Jeder Use Case erfordert eine formelle Validierung (Daten, Recht, Business), bevor Budget fließt.';
        if (ans.answer_level === 5) return 'Integriertes Framework: Ein standardisierter Prozess sichert die perfekte Abstimmung von Technik, Strategie und Regulierung ab Tag eins.';
    }

    // Override for question 14 answers
    if (lang === 'de' && currentQ?.question_id === 14) {
        if (ans.answer_level === 1) return 'Keine';
        if (ans.answer_level === 2) return 'Konzeption (Ideen & Brainstorming)';
        if (ans.answer_level === 3) return 'Pilotierung (1-2 Testprojekte)';
        if (ans.answer_level === 4) return 'Produktiv (Mehrere im Einsatz)';
        if (ans.answer_level === 5) return 'Skaliert (Voll integriert)';
    }

    // Override for question 15 answers
    if (lang === 'de' && currentQ?.question_id === 15) {
        if (ans.answer_level === 1) return 'Keine systematische Messung: Erfolg wird bisher nicht formal erfasst oder bewertet.';
        if (ans.answer_level === 2) return 'Reines Kosten-Controlling: Die Überwachung beschränkt sich primär auf die Einhaltung der Projektbudgets.';
        if (ans.answer_level === 3) return 'Qualitative Nutzenbewertung: Der Erfolg wird anhand von weichen Faktoren (z. B. Mitarbeiterfeedback, gefühlte Entlastung) bewertet.';
        if (ans.answer_level === 4) return 'KPI-basiertes Tracking: Messung erfolgt über definierte operative Kennzahlen (z. B. Zeitersparnis, Fehlerrate).';
        if (ans.answer_level === 5) return 'Quantitativer ROI: Der finanzielle Wertbeitrag wird präzise berechnet und gegen die Investitionskosten gestellt.';
    }

    // Override for question 16 answers
    if (lang === 'de' && currentQ?.question_id === 16) {
        if (ans.answer_level === 1) return 'Rein explorativ: Fokus liegt auf Experimenten und dem Kennenlernen der Technologie ohne direkten Geschäftsbezug.';
        if (ans.answer_level === 2) return 'Randbereiche: KI berührt zwar Kernprozesse, löst aber noch keine kritischen oder strategischen Probleme.';
        if (ans.answer_level === 3) return 'Punktuelle Entlastung: KI wird bei bekannten Engpässen eingesetzt, der messbare Erfolg ist jedoch noch nicht durchgängig belegt.';
        if (ans.answer_level === 4) return 'Systematische Optimierung: KI behebt gezielt schwere Engpässe und sorgt für nachweisbare Produktivitätssteigerungen.';
        if (ans.answer_level === 5) return 'Strategischer Hebel: KI definiert Prozesse neu, beseitigt strukturelle Barrieren und sichert langfristige Wettbewerbsvorteile.';
    }

    // Override for question 17 answers
    if (lang === 'de' && currentQ?.question_id === 17) {
        if (ans.answer_level === 1) return 'Informell: Prozesse sind kaum dokumentiert und hängen stark vom Wissen einzelner Mitarbeiter ab.';
        if (ans.answer_level === 2) return 'Punktuell: Es existieren grobe Checklisten oder Leitfäden für wichtige Teilbereiche.';
        if (ans.answer_level === 3) return 'Systematisch dokumentiert: Kernprozesse sind schriftlich fixiert und für das Team zugänglich.';
        if (ans.answer_level === 4) return 'Standardisierte SOPs: Verbindliche Standard-Betriebsabläufe (SOPs) sind unternehmensweit etabliert.';
        if (ans.answer_level === 5) return 'Digital & Automatisiert: Prozesse sind vollständig digital abgebildet und ermöglichen eine datengestützte Optimierung.';
    }

    // Override for question 18 answers
    if (lang === 'de' && currentQ?.question_id === 18) {
        if (ans.answer_level === 1) return 'Ad-hoc & Undefiniert: Projekte entstehen zufällig; es gibt keine festen Abläufe oder klaren Verantwortlichkeiten.';
        if (ans.answer_level === 2) return 'Personenabhängig: Die Umsetzung hängt vom Engagement einzelner „KI-Treiber“ ab; ein einheitliches Playbook fehlt.';
        if (ans.answer_level === 3) return 'Standardisierte Workflows: Wir nutzen konsistente Methoden (z. B. Task-Boards, Sprints), um Projekte planbar zu steuern.';
        if (ans.answer_level === 4) return 'Spezifische KI-Methodik: Ein angepasster Prozess (inkl. Prototyping & Daten-Check) sichert die effiziente Ressourcennutzung.';
        if (ans.answer_level === 5) return 'Agile Skalierung: Ein hocheffizienter Prozess ermöglicht den nahtlosen Übergang vom Pilotprojekt (PoC) in den produktiven Live-Betrieb.';
    }

    // Override for question 19 answers
    if (lang === 'de' && currentQ?.question_id === 19) {
        if (ans.answer_level === 1) return '> 12 Monate';
        if (ans.answer_level === 2) return '7 – 12 Monate';
        if (ans.answer_level === 3) return '3 – 6 Monate';
        if (ans.answer_level === 4) return '1 – 2 Monate';
        if (ans.answer_level === 5) return '< 4 Wochen';
    }

    // Override for question 20 answers
    if (lang === 'de' && currentQ?.question_id === 20) {
        if (ans.answer_level === 1) return 'Ad-hoc: Es existiert kein definierter Prozess; die Umsetzung erfolgt nach individueller Gelegenheit.';
        if (ans.answer_level === 2) return 'Fallbasiert: Der Übergang erfolgt manuell und wird für jedes Projekt individuell neu organisiert.';
        if (ans.answer_level === 3) return 'Standardisiert: Es gibt einen festen Leitfaden für die Entwicklung und den Go-Live von KI-Lösungen.';
        if (ans.answer_level === 4) return 'Optimierter Skalierungspfad: Ein systematischer Prozess sichert Qualität und Effizienz beim Rollout ab.';
        if (ans.answer_level === 5) return 'Vollautomatisierter Rollout: Ein integriertes System (z. B. MLOps) ermöglicht eine nahtlose und automatisierte Bereitstellung.';
    }

    // Override for question 21 answers
    if (lang === 'de' && currentQ?.question_id === 21) {
        if (ans.answer_level === 1) return 'Kein Regelwerk: Es gibt bisher keine schriftlichen Vorgaben oder Verbote für die Nutzung von KI-Tools.';
        if (ans.answer_level === 2) return 'Informelle Absprachen: Es existieren mündliche oder unverbindliche Empfehlungen (z. B. „Keine Kundendaten in ChatGPT“).';
        if (ans.answer_level === 3) return 'Konzeptioneller Entwurf: Ein offizielles Regelwerk (KI-Policy) ist in Arbeit oder liegt als Entwurf vor.';
        if (ans.answer_level === 4) return 'Publizierte Richtlinie: Eine verbindliche KI-Leitlinie ist offiziell kommuniziert und für alle Mitarbeiter zugänglich.';
        if (ans.answer_level === 5) return 'Gelebte Governance: Die Einhaltung der Richtlinien wird aktiv überwacht (Compliance-Checks) und regelmäßig an neue Gesetze (z. B. EU AI Act) angepasst.';
    }

    // Override for question 22 answers
    if (lang === 'de' && currentQ?.question_id === 22) {
        if (ans.answer_level === 1) return 'Ungeprüft (Hohes Risiko)';
        if (ans.answer_level === 2) return 'Punktuell (Reaktive Prüfung)';
        if (ans.answer_level === 3) return 'DSGVO-konform (Standard)';
        if (ans.answer_level === 4) return 'Systematisch (Privacy by Design)';
        if (ans.answer_level === 5) return 'Revisionssicher (Full Compliance)';
    }

    // Override for question 23 answers
    if (lang === 'de' && currentQ?.question_id === 23) {
        if (ans.answer_level === 1) return 'Undefiniert: Es gibt keine explizite Zuweisung von Verantwortlichkeiten für KI-Outputs.';
        if (ans.answer_level === 2) return 'Individuell: Die Verantwortung liegt ad-hoc bei den jeweiligen Mitarbeitern, die ein Tool nutzen.';
        if (ans.answer_level === 3) return 'Dezentral: Abteilungsleiter tragen die Verantwortung für die in ihrem Bereich eingesetzte KI.';
        if (ans.answer_level === 4) return 'Zentralisiert: Ein benannter KI-Verantwortlicher (AI Lead) koordiniert die Strategie und Risiken.';
        if (ans.answer_level === 5) return 'Institutionalisiert: Eine etablierte Governance-Struktur mit klaren Haftungs- und Überwachungsregeln ist aktiv.';
    }

    // Override for question 24 answers
    if (lang === 'de' && currentQ?.question_id === 24) {
        if (ans.answer_level === 1) return 'Keine Anforderungen: Wir verlassen uns auf die Standardangaben der Anbieter; es gibt keine spezifischen Prüfprozesse.';
        if (ans.answer_level === 2) return 'Passive Akzeptanz: Wir fordern Standard-Zertifikate an, prüfen aber nicht die Details der KI-Modelle oder Datenherkunft.';
        if (ans.answer_level === 3) return 'Grundlegende Transparenz: Partner müssen wesentliche Informationen (z. B. DSGVO-Konformität, Einsatzbereiche) vertraglich zusichern.';
        if (ans.answer_level === 4) return 'Detaillierte Offenlegung: Wir fordern Einblick in Modell-Details, Trainingsdaten-Struktur und potenzielle Biases (Voreingenommenheiten).';
        if (ans.answer_level === 5) return 'Strategische Partnerschaft: Volle Transparenz über den gesamten Lebenszyklus sowie regelmäßige Audits der KI-Systeme sind fest verankert.';
    }

    // Override for question 25 answers
    if (lang === 'de' && currentQ?.question_id === 25) {
        if (ans.answer_level === 1) return 'On-Premise (Lokal)';
        if (ans.answer_level === 2) return 'Virtualisiert (On-Prem+)';
        if (ans.answer_level === 3) return 'Hybrid (Mix)';
        if (ans.answer_level === 4) return 'Cloud-First';
        if (ans.answer_level === 5) return 'Cloud-Native';
    }

    // Override for question 26 answers
    if (lang === 'de' && currentQ?.question_id === 26) {
        if (ans.answer_level === 1) return 'Fertige KI-Anwendungen (SaaS): Direkte Nutzung von Tools wie ChatGPT (Team/Enterprise), Jasper oder DeepL.';
        if (ans.answer_level === 2) return 'Integrierte KI-Assistenten: KI-Funktionen innerhalb bestehender Software (z. B. Microsoft Copilot, Salesforce Einstein, SAP AI).';
        if (ans.answer_level === 3) return 'Low-Code / No-Code Plattformen: Tools zum Bau einfacher KI-Workflows ohne Programmierung (z. B. MS Power Platform, Make, Zapier).';
        if (ans.answer_level === 4) return 'Frameworks für Eigenentwicklungen: Programmumgebungen für eigene Modelle (z. B. Python-Libraries, Jupyter Notebooks, PyTorch).';
        if (ans.answer_level === 5) return 'Managed AI/ML Plattformen: Cloud-Umgebungen zur professionellen Entwicklung und Skalierung (z. B. Azure AI Studio, AWS SageMaker, Vertex AI).';
        if (ans.answer_level === 6) return 'Keine spezifischen KI-Tools: Wir nutzen aktuell keine dedizierten KI-Anwendungen.';
        if (ans.answer_level === 7) return 'Nicht sicher / Keine Angabe (Exklusive Option)';
    }

    // Override for question 27 answers
    if (lang === 'de' && currentQ?.question_id === 27) {
        if (ans.answer_level === 1) return 'Manuell (Hoher Aufwand)';
        if (ans.answer_level === 2) return 'Komplex (Einzelfall-Lösung)';
        if (ans.answer_level === 3) return 'Standardisiert (IT-Regelprozess)';
        if (ans.answer_level === 4) return 'Modular (Plug & Play)';
        if (ans.answer_level === 5) return 'Automatisiert (Skalierung per Klick)';
    }

    // Override for question 28 answers
    if (lang === 'de' && currentQ?.question_id === 28) {
        if (ans.answer_level === 1) return 'Marktanpassung: Orientierung an aktuellen Trends und Wettbewerbern.';
        if (ans.answer_level === 2) return 'Effizienzsteigerung: Fokus auf Kostensenkung und Automatisierung.';
        if (ans.answer_level === 3) return 'Strategische Planung: Erstellung einer fundierten Roadmap.';
        if (ans.answer_level === 4) return 'Befähigungs-Check: Analyse von technischer und personeller Reife.';
        if (ans.answer_level === 5) return 'Innovationsführerschaft: Ausbau von echten Wettbewerbsvorteilen.';
    }

    // Override for question 29 answers
    if (lang === 'de' && currentQ?.question_id === 29) {
        if (ans.answer_level === 1) return 'Exzellenz im Kundenservice: Effizienzsteigerung im Support (z. B. durch intelligente Chatbots/Assistenten).';
        if (ans.answer_level === 2) return 'Operative Effizienz: Automatisierung repetitiver Aufgaben und Backoffice-Prozesse.';
        if (ans.answer_level === 3) return 'Data-Driven Insights: Gewinnung tieferer Erkenntnisse aus vorhandenen Datenbeständen.';
        if (ans.answer_level === 4) return 'Intelligente Suche & Knowledge Management: Schnelleres Auffinden von Informationen und Expertenwissen.';
        if (ans.answer_level === 5) return 'Automatisierte Dokumentenanalyse: Intelligente Erfassung und Verarbeitung von Verträgen, Rechnungen etc.';
        if (ans.answer_level === 6) return 'Hyper-Personalisierung: Individuelle Kundenansprache und maßgeschneiderte Angebote.';
        if (ans.answer_level === 7) return 'Direkte Kostensenkung: Reduzierung der Betriebskosten durch Prozessoptimierung.';
    }

    // Override for question 30 answers
    if (lang === 'de' && currentQ?.question_id === 30) {
        if (ans.answer_level === 1) return 'Keine Verankerung: KI-Trends wurden bisher nicht systematisch bewertet; es existiert keine schriftliche Strategie.';
        if (ans.answer_level === 2) return 'Marktgetriebene Reaktion: Wir reagieren punktuell auf Entwicklungen im Marktumfeld oder bei Mitbewerbern.';
        if (ans.answer_level === 3) return 'Explorative Erprobung: Trends werden aktiv beobachtet und erste Pilotprojekte zur strategischen Validierung durchgeführt.';
        if (ans.answer_level === 4) return 'Strategische Integration: Eine formelle KI-Roadmap mit klaren Zielen ist fester Bestandteil der Unternehmensplanung.';
        if (ans.answer_level === 5) return 'Transformatorische Führung: KI definiert unser Geschäftsmodell neu und dient als primärer Treiber für Brancheninnovationen.';
    }

    // Override for question 31 answers
    if (lang === 'de' && currentQ?.question_id === 31) {
        if (ans.answer_level === 1) return 'Geschäftsführung / Vorstand (Top-Down): KI wird als strategische Priorität von der Unternehmensleitung forciert.';
        if (ans.answer_level === 2) return 'IT- & Technologie-Abteilung: Die Initiative liegt primär in der Verantwortung der IT (technologiegetrieben).';
        if (ans.answer_level === 3) return 'Digital Transformation / Innovation Team: Ein dediziertes Team steuert die KI-Initiativen abteilungsübergreifend.';
        if (ans.answer_level === 4) return 'Operative Fachabteilungen (z. B. Marketing, Vertrieb, HR): Die Nachfrage nach KI kommt direkt aus dem Kerngeschäft.';
        if (ans.answer_level === 5) return 'Operations & Supply Chain: Der Fokus liegt auf der Optimierung von Produktion, Logistik und Lieferketten.';
        if (ans.answer_level === 6) return 'Data Science & Analytics Team: Spezialisten für Datenanalyse treiben die Entwicklung von KI-Modellen voran.';
        if (ans.answer_level === 7) return 'Einzelne Early Adopter (Bottom-Up): Motivierte Mitarbeiter nutzen KI-Tools eigeninitiativ in ihrem Arbeitsalltag.';
        if (ans.answer_level === 8) return 'Externe Partner & Berater: Die Impulse und die Umsetzung kommen maßgeblich von außen.';
        if (ans.answer_level === 9) return 'Kein definierter interner Treiber: Es gibt aktuell keine klare Zuständigkeit oder treibende Kraft.';
    }

    // Override for question 32 answers
    if (lang === 'de' && currentQ?.question_id === 32) {
        if (ans.answer_level === 1) return 'Keine (Interessierter Beobachter)';
        if (ans.answer_level === 2) return 'Operativ (Verantwortung auf Projekt- oder Teamebene)';
        if (ans.answer_level === 3) return 'Strategisch (Gesamtverantwortung / Geschäftsführung)';
    }

    // Override for question 33 answers
    if (lang === 'de' && currentQ?.question_id === 33) {
        if (ans.answer_level === 1) return 'Unternehmensleitung / C-Level (Geschäftsführung, Vorstand, Inhaber)';
        if (ans.answer_level === 2) return 'IT-Management / Technologie-Leitung (CIO, CTO, IT-Leiter)';
        if (ans.answer_level === 3) return 'Fachbereichsleitung / Prozessverantwortung (z. B. Marketing, Vertrieb, Produktion)';
        if (ans.answer_level === 4) return 'Strategie, Innovation & Business Analyse';
        if (ans.answer_level === 5) return 'Data Science & KI-Spezialisierung';
        if (ans.answer_level === 6) return 'Projekt- & Programmmanagement';
        if (ans.answer_level === 7) return 'Fachexperte / Key User (Anwenderebene)';
        if (ans.answer_level === 8) return 'Externer Berater';
    }

    // Anwenden auf "statement" Fragen
    const isStatement = (currentQ?.type || '').toLowerCase() === 'statement';

    if (isStatement && lang === 'de') {
        return text.replace(/\s+[-–—]\s+/, ': ');
    }
    return text;
};

export default function QuestionnaireWizard() {
    const { t, i18n } = useTranslation();
    const { responseId } = useParams();
    const navigate = useNavigate();
    const [questions, setQuestions] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [selectedAnswers, setSelectedAnswers] = useState([]);
    // Map<questionId, Array<answerId>>
    const [allAnswers, setAllAnswers] = useState({});

    // Track answered questions for progress calculation
    // Map<questionId, boolean>
    const [answeredMap, setAnsweredMap] = useState({});

    // Load progress from local storage on mount
    useEffect(() => {
        const savedProgress = localStorage.getItem(`assessment_progress_${responseId}`);
        if (savedProgress) {
            try {
                const { index, answered, answers } = JSON.parse(savedProgress);
                if (typeof index === 'number') setCurrentIndex(index);
                if (answered) setAnsweredMap(answered);
                if (answers) setAllAnswers(answers);
            } catch (e) {
                console.error("Failed to parse saved progress", e);
            }
        }
    }, [responseId]);

    // Set page title
    useEffect(() => {
        document.title = "AI Compass: Assessment";
    }, []);

    // Save progress to local storage
    useEffect(() => {
        if (questions.length > 0) {
            localStorage.setItem(`assessment_progress_${responseId}`, JSON.stringify({
                index: currentIndex,
                answered: answeredMap,
                answers: allAnswers
            }));
        }
    }, [currentIndex, answeredMap, allAnswers, questions.length, responseId]);

    useEffect(() => {
        async function fetchQuestions() {
            try {
                // 1. Try Cache
                // 1. Try Cache
                const cached = sessionStorage.getItem('cached_questionnaire_data_v4');
                if (cached) {
                    console.log("Found cached data in sessionStorage");
                    try {
                        const data = JSON.parse(cached);
                        console.log("Parsed cached data:", data);
                        if (data && data.questions && Array.isArray(data.questions)) {
                            console.log(`Using cached questionnaire with ${data.questions.length} questions.`);
                            setQuestions(data.questions);
                            setLoading(false);
                            return;
                        } else {
                            console.warn("Cached data format invalid:", data);
                        }
                    } catch (e) {
                        console.error("Failed to parse cached questionnaire:", e);
                    }
                } else {
                    console.log("No cached questionnaire found in sessionStorage.");
                }

                // 2. Fallback to Network
                const data = await api.getQuestionnaire();
                if (data && data.questions) {
                    setQuestions(data.questions);
                    // Update cache for persistence on refresh
                    sessionStorage.setItem('cached_questionnaire_data_v4', JSON.stringify(data));
                }
            } catch (error) {
                console.error("Failed to load questions", error);
                toast.error(t('wizard.toasts.loadError', "Failed to load questionnaire."));
            } finally {
                setLoading(false);
            }
        }
        fetchQuestions();
    }, []);

    useEffect(() => {
        const currentQ = questions[currentIndex];
        if (!currentQ) return;

        // 1. Check if we have a persisted answer in our local session state
        if (allAnswers[currentQ.question_id] && allAnswers[currentQ.question_id].length > 0) {
            setSelectedAnswers(allAnswers[currentQ.question_id]);
            return;
        }

        // 2. Fallback: Pre-select slider default if applicable and no previous answer
        if ((currentQ.type || 'choice').toLowerCase() === 'slider' && currentQ.answers?.length > 0) {
            // Default to the answer with the lowest answer_level (first in sorted order)
            const sortedAnswers = [...currentQ.answers].sort((a, b) => a.answer_level - b.answer_level);
            setSelectedAnswers([sortedAnswers[0].answer_id]);
        } else {
            setSelectedAnswers([]);
        }
    }, [currentIndex, questions, allAnswers]);

    // Group questions by dimension
    const dimensions = useMemo(() => {
        if (!questions.length) return [];

        const groups = {};
        questions.forEach(q => {
            const dId = q.dimension_id || 0;
            const dName = getDimensionName(q, i18n.language);
            if (!groups[dId]) {
                groups[dId] = {
                    id: dId,
                    name: dName || `Dimension ${dId}`,
                    questions: [],
                    total: 0,
                    answered: 0
                };
            }
            groups[dId].questions.push(q);
            groups[dId].total++;
            if (answeredMap[q.question_id]) {
                groups[dId].answered++;
            }
        });

        // Convert to array and sort by ID
        return Object.values(groups).sort((a, b) => a.id - b.id);
    }, [questions, answeredMap, i18n.language]);

    const handleNext = async () => {
        // Validation skip for slider is implicit if we pre-select, but good safety check
        if (selectedAnswers.length === 0) {
            const currentQ = questions[currentIndex];
            if ((currentQ.type || 'choice').toLowerCase() === 'slider') {
                // Should be pre-selected, but just in case
            } else {
                toast.warning(t('wizard.toasts.selectWarning', "Please select an answer to continue."));
                return;
            }
        }

        if (saving) return;
        setSaving(true);

        try {
            const currentQ = questions[currentIndex];
            // Only save to DB if we have answers (for slider/choice)
            if (selectedAnswers.length > 0) {
                await api.saveAnswer(parseInt(responseId), currentQ.question_id, selectedAnswers);
            }

            // Mark as answered locally for progress bar and persistence
            setAnsweredMap(prev => ({ ...prev, [currentQ.question_id]: true }));
            setAllAnswers(prev => ({ ...prev, [currentQ.question_id]: selectedAnswers }));

            if (currentIndex < questions.length - 1) {
                setCurrentIndex(prev => prev + 1);
            } else {
                // Do NOT complete assessment yet. Navigate to Company Snapshot for details.
                toast.success(t('wizard.toasts.completeSuccess', "Questions complete! Just one last step."));
                navigate('/snapshot');
            }
        } catch (error) {
            console.error("Failed to save answer", error);
            if (error.message && (error.message.includes("404") || error.message.toLowerCase().includes("not found"))) {
                toast.error(t('wizard.toasts.sessionExpired', "Session expired. Please start over."));
                navigate('/');
                return;
            }
            toast.error(error.message || t('wizard.toasts.saveError', "Failed to save answer."));
        } finally {
            setSaving(false);
        }
    };

    const toggleCheckbox = (answerId) => {
        setSelectedAnswers(prev =>
            prev.includes(answerId)
                ? prev.filter(id => id !== answerId)
                : [...prev, answerId]
        );
    };

    const handleRadioChange = (val) => {
        const ansId = parseInt(val);
        setSelectedAnswers([ansId]);
    };

    const handleSliderChange = (val) => {
        const index = val[0];
        // Use the sorted answers array (same order as displayed slider)
        const sortedAnswers = [...(questions[currentIndex].answers || [])].sort((a, b) => a.answer_level - b.answer_level);
        if (sortedAnswers[index]) {
            setSelectedAnswers([sortedAnswers[index].answer_id]);
        }
    };

    const handleSkipDimension = async () => {
        if (saving) return;
        setSaving(true);
        try {
            const remaining = questions.slice(currentIndex);
            const d8Questions = remaining.filter(q => q.dimension_id === 8);

            await Promise.all(d8Questions.map(q =>
                api.saveAnswer(parseInt(responseId), q.question_id, [])
            ));

            // Mark skipped as answered (or handled)
            const newAnswered = { ...answeredMap };
            d8Questions.forEach(q => newAnswered[q.question_id] = true);
            setAnsweredMap(newAnswered);

            let nextIndex = -1;
            for (let i = currentIndex + 1; i < questions.length; i++) {
                if (questions[i].dimension_id !== 8) {
                    nextIndex = i;
                    break;
                }
            }

            if (nextIndex !== -1) {
                setCurrentIndex(nextIndex);
                toast.info(t('wizard.toasts.skipInfo', "Skipped remaining Dimension 8 questions."));
            } else {
                // Do NOT complete assessment yet. Navigate to Company Snapshot.
                toast.success(t('wizard.toasts.completeSuccess', "Questions complete! Just one last step."));
                navigate('/snapshot');
            }
        } catch (error) {
            console.error("Skip failed", error);
            if (error.message && (error.message.includes("404") || error.message.toLowerCase().includes("not found"))) {
                toast.error(t('wizard.toasts.sessionExpired', "Session expired. Please start over."));
                navigate('/');
                return;
            }
            toast.error(error.message || t('wizard.toasts.skipError', "Failed to skip dimension."));
        } finally {
            setSaving(false);
        }
    };

    if (loading) return (
        <div className="flex justify-center items-center h-screen bg-slate-50 text-slate-500 font-medium animate-pulse">
            {t('wizard.loading', "Loading assessment...")}
        </div>
    );

    if (!questions.length) return (
        <div className="flex justify-center items-center h-screen bg-slate-50 text-slate-500">
            {t('wizard.noQuestions', "No questions found.")}
        </div>
    );

    const currentQuestion = questions[currentIndex];
    const currentDimensionId = currentQuestion.dimension_id || 0;

    const renderAnswers = () => {
        const answers = [...(currentQuestion.answers || [])].sort((a, b) => a.answer_level - b.answer_level);
        const type = (currentQuestion.type || 'choice').toLowerCase();

        if (type === 'slider') {
            const maxIndex = answers.length - 1;
            const currentSelectedId = selectedAnswers[0];
            const currentIndexVal = answers.findIndex(a => a.answer_id === currentSelectedId);
            const safeIndex = currentIndexVal !== -1 ? currentIndexVal : 0;

            return (
                <div className="flex flex-col justify-center h-full px-4 md:px-8 py-4">
                    <div className="mb-4 text-center">
                        <motion.div
                            key={answers[safeIndex]?.answer_text}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="inline-block px-6 py-2 rounded-2xl bg-blue-50 text-blue-700 text-xl font-bold border border-blue-100 shadow-sm"
                        >
                            {answers[safeIndex] ? formatAnswerText(answers[safeIndex], i18n.language, currentQuestion) : (i18n.language === 'de' ? 'Ziehen zum Auswählen' : 'Drag to select')}
                        </motion.div>
                    </div>
                    <Slider
                        value={[safeIndex]}
                        max={maxIndex}
                        step={1}
                        onValueChange={handleSliderChange}
                        className="w-full cursor-pointer py-4"
                    />
                    <div className="flex justify-between mt-8 text-sm font-semibold text-slate-400 uppercase tracking-wider">
                        <span className="text-left w-1/2 pe-4">{answers[0] ? formatAnswerText(answers[0], i18n.language, currentQuestion) : ''}</span>
                        <span className="text-right w-1/2 ps-4">{answers[maxIndex] ? formatAnswerText(answers[maxIndex], i18n.language, currentQuestion) : ''}</span>
                    </div>
                </div>
            );
        }

        if (type === 'checklist') {
            return (
                <div className="flex flex-col gap-2 w-full">
                    {answers.map(ans => (
                        <motion.div
                            key={ans.answer_id}
                            whileHover={{ scale: 1.005 }}
                            whileTap={{ scale: 0.995 }}
                            className={cn(
                                "flex items-start space-x-3 p-3 border rounded-xl cursor-pointer transition-all duration-200 h-full",
                                selectedAnswers.includes(ans.answer_id)
                                    ? "border-blue-600 bg-blue-50/50 shadow-md"
                                    : "border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50 hover:shadow-sm"
                            )}
                            onClick={() => toggleCheckbox(ans.answer_id)}
                        >
                            <Checkbox
                                id={`ans-${ans.answer_id}`}
                                checked={selectedAnswers.includes(ans.answer_id)}
                                onCheckedChange={() => toggleCheckbox(ans.answer_id)}
                                className="mt-0.5 h-4 w-4 border-2 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 shrink-0"
                            />
                            <Label
                                htmlFor={`ans-${ans.answer_id}`}
                                className="text-[13px] font-medium leading-snug cursor-pointer flex-1 select-none text-slate-700"
                            >
                                {formatAnswerText(ans, i18n.language, currentQuestion)}
                            </Label>
                        </motion.div>
                    ))}
                </div>
            );
        }

        // Default: Choice / Statement (Radio)
        const isShortText = answers.every(a => (a.answer_text || '').length < 60);

        return (
            <RadioGroup
                value={selectedAnswers[0]?.toString()}
                onValueChange={handleRadioChange}
                className="w-full gap-1.5 flex flex-col"
            >
                {answers.map(ans => (
                    <motion.div
                        key={ans.answer_id}
                        whileHover={{ scale: 1.005 }}
                        whileTap={{ scale: 0.995 }}
                        className={cn(
                            "flex space-x-3 border rounded-xl cursor-pointer transition-all duration-200 h-full",
                            isShortText ? "p-3 items-center" : "p-3 items-start",
                            selectedAnswers.includes(ans.answer_id)
                                ? "border-blue-600 bg-blue-50/50 shadow-md ring-1 ring-blue-600/20"
                                : "border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50 hover:shadow-sm"
                        )}
                        onClick={() => handleRadioChange(ans.answer_id.toString())}
                    >
                        <RadioGroupItem
                            value={ans.answer_id.toString()}
                            id={`ans-${ans.answer_id}`}
                            className="mt-0.5 h-4 w-4 border-2 text-blue-600 border-slate-300 data-[state=checked]:border-blue-600 shrink-0"
                        />
                        <Label
                            htmlFor={`ans-${ans.answer_id}`}
                            className="text-[13px] font-medium leading-snug flex-1 cursor-pointer select-none text-slate-700"
                        >
                            {formatAnswerText(ans, i18n.language, currentQuestion)}
                        </Label>
                        {selectedAnswers.includes(ans.answer_id) && (
                            <CheckCircle2 className="w-4 h-4 text-blue-600 animate-in zoom-in spin-in-90 duration-300 shrink-0" />
                        )}
                    </motion.div>
                ))}
            </RadioGroup>
        );
    };

    const DimensionList = () => (
        <div className="space-y-2 py-1 w-full px-3 flex-1">
            <div className="px-4 mb-3">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest bg-white/30 w-fit px-2 py-1 rounded-md backdrop-blur-sm">{i18n.language === 'de' ? 'Ihr Fortschritt' : 'Your Progress'}</h3>
            </div>
            {dimensions.filter(d => d.id !== 8).map((dim, idx) => {
                const isActive = dim.id === currentDimensionId;
                const isCompleted = dim.answered === dim.total;
                const progress = (dim.answered / dim.total) * 100;

                return (
                    <div key={dim.id} className={cn(
                        "relative px-3 py-1 flex items-center gap-3 transition-all duration-500 rounded-xl mx-2 group",
                        isActive
                            ? "glass-premium translate-x-1"
                            : "bg-slate-50/50 hover:bg-slate-100/50 hover:translate-x-1"
                    )}>
                        {/* Active Indicator Color Splash */}
                        {isActive && (
                            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 rounded-2xl pointer-events-none" />
                        )}
                        {/* Active Line */}
                        {isActive && (
                            <div className="absolute left-0 top-1/2 -translate-y-1/2 h-8 w-1 bg-gradient-to-b from-indigo-500 to-violet-600 rounded-r-full shadow-[0_0_12px_rgba(99,102,241,0.6)]" />
                        )}

                        <div className="flex-none relative z-10">
                            {isCompleted ? (
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center text-white shadow-lg shadow-emerald-500/30 ring-2 ring-white/80">
                                    <Check className="w-5 h-5" />
                                </div>
                            ) : isActive ? (
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-600 to-violet-600 flex items-center justify-center text-white shadow-xl shadow-indigo-500/40 ring-2 ring-white animate-pulse-slow">
                                    <Disc className="w-5 h-5" />
                                </div>
                            ) : (
                                <div className="w-10 h-10 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500 group-hover:bg-slate-200 group-hover:shadow-sm transition-all">
                                    <span className="text-xs font-bold font-heading">{idx + 1}</span>
                                </div>
                            )}
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className={cn("text-sm font-bold truncate mb-1 transition-colors", isActive ? "text-slate-800" : "text-slate-500 group-hover:text-slate-700")}>
                                {dim.name}
                            </div>
                            <div className="flex items-center gap-3">
                                <Progress
                                    value={progress}
                                    className="h-1.5 bg-slate-200 flex-1"
                                    indicatorClassName={isCompleted ? "bg-emerald-500" : isActive ? "bg-gradient-to-r from-indigo-500 to-violet-500" : "bg-slate-400"}
                                />
                                <span className={cn("text-[10px] font-semibold tabular-nums", isActive ? "text-indigo-600" : "text-slate-400")}>
                                    {Math.round(progress)}%
                                </span>
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );

    return (
        <div className="h-screen w-screen overflow-hidden flex relative font-sans">
            <PageBackground />

            {/* Desktop Sidebar */}
            <aside className="hidden lg:flex flex-col w-96 bg-white/10 backdrop-blur-3xl border-r border-white/20 z-20 h-full overflow-y-auto custom-scrollbar shadow-[20px_0_40px_rgba(0,0,0,0.02)]">
                <div className="p-6 pb-2">
                    <Link to="/" className="flex items-center gap-3 mb-2 hover:opacity-80 transition-opacity group">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20 ring-2 ring-white/10 group-hover:shadow-blue-500/40 transition-shadow">
                            <Compass className="w-6 h-6 text-white" />
                        </div>
                        <div className="flex flex-col justify-center">
                            <span className="text-xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent font-heading tracking-tight leading-none">
                                AI Compass
                            </span>
                        </div>
                    </Link>
                </div>
                <DimensionList />

                {/* Sidebar Footer Links */}
                <div className="p-6 mt-auto border-t border-white/20">
                    <div className="flex flex-row gap-4 text-xs font-medium text-slate-500">
                        <Link to="/imprint" className="hover:text-slate-800 transition-colors w-fit">{i18n.language === 'de' ? 'Impressum' : 'Imprint'}</Link>
                        <Link to="/privacy" className="hover:text-slate-800 transition-colors w-fit">{i18n.language === 'de' ? 'Datenschutzerklärung' : 'Privacy Policy'}</Link>
                    </div>
                </div>
            </aside>

            {/* Mobile Header with Drawer */}
            <div className="lg:hidden absolute top-0 left-0 w-full glass-premium z-30 flex justify-between items-center px-4 py-3">
                <div className="font-bold text-slate-800 truncate max-w-[200px]">
                    {getDimensionName(currentQuestion, i18n.language)}
                </div>
                <Sheet>
                    <SheetTrigger asChild>
                        <Button variant="ghost" size="icon" className="hover:bg-white/20">
                            <Menu className="w-6 h-6 text-slate-600" />
                        </Button>
                    </SheetTrigger>
                    <SheetContent side="left" className="w-80 p-0 bg-white/95 backdrop-blur-xl">
                        <div className="p-6 border-b border-slate-100">
                            <div className="text-xl font-bold text-slate-900">Dimensions</div>
                        </div>
                        <DimensionList />
                    </SheetContent>
                </Sheet>
            </div>

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col h-full relative z-10 pt-16 lg:pt-0 overflow-hidden">
                <div className="flex-1 flex flex-col w-full h-full max-w-3xl mx-auto p-1 md:p-2 justify-center overflow-hidden">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={currentIndex}
                            initial={{ opacity: 0, scale: 0.98, y: 10 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 1.02 }}
                            transition={{ duration: 0.4, ease: [0.19, 1.0, 0.22, 1.0] }} // Authentic iOS ease
                            className="w-full flex flex-col h-full max-h-full"
                        >
                            <Card className="flex flex-col glass-premium rounded-[1.5rem] overflow-hidden w-full h-full max-h-full border-white/50 ring-1 ring-white/60">
                                {/* Question Header */}
                                <CardHeader className="flex-none border-b border-white/20 bg-white/20 pb-0 pt-3 px-4 md:px-6 backdrop-blur-md">
                                    <div className="flex items-center justify-between mb-3 md:mb-4">
                                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/50 border border-white/60 shadow-sm text-indigo-900 text-[10px] font-bold uppercase tracking-widest backdrop-blur-sm">
                                            <span className="relative flex h-1.5 w-1.5 mr-0.5">
                                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                                                <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-indigo-600"></span>
                                            </span>
                                            {i18n.language === 'de' ? 'Frage' : 'Question'} {currentIndex + 1} / {currentQuestion.dimension_id === 8 ? 33 : 27}
                                        </div>
                                    </div>

                                    <CardTitle className="text-lg md:text-xl font-black text-slate-800 tracking-tight font-heading leading-tight mb-1">
                                        {(() => {
                                            let text = i18n.language === 'de' && currentQuestion.question_text_de ? currentQuestion.question_text_de : currentQuestion.question_text;
                                            if (i18n.language === 'de' && text.includes('Inwieweit sind KI-Fähigkeiten und technische Kompetenz in Ihrer Belegschaft etabliert?')) {
                                                text = text.replace('Kompetenz', 'Kompetenzen');
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 1) {
                                                text = 'Welchen strategischen Stellenwert nimmt KI in Ihren Gremien-Sitzungen ein?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 2) {
                                                text = 'Wie weit ist Ihre KI-Strategie dokumentiert und im Unternehmen verankert?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 3) {
                                                text = 'Nach welcher Logik erfolgt die Budgetierung Ihrer KI-Investitionen?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 4) {
                                                text = 'Welche wettbewerbsstrategische Positionierung streben Sie im Bereich KI an?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 5) {
                                                text = 'Wie bewerten Sie die aktuelle Akzeptanz und kulturelle Bereitschaft Ihrer Belegschaft gegenüber KI?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 7) {
                                                text = 'Wie systematisch ist die KI-Weiterbildung in Ihrem Unternehmen verankert?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 9) {
                                                text = 'Welche Datenbestände liegen in Ihrem Unternehmen digital und verwertbar vor? (Alles Zutreffende auswählen)';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 10) {
                                                text = 'Welche Bausteine bilden das Fundament Ihrer aktuellen IT-Landschaft? (Alles Zutreffende auswählen)';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 11) {
                                                text = 'Wie bewerten Sie die Qualität und Konsistenz Ihrer Geschäftsdaten?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 12) {
                                                text = 'Wie sicher ist Ihr Team darin, Daten für tägliche Entscheidungen zu nutzen?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 13) {
                                                text = 'Wie systematisch prüfen Sie die Machbarkeit von KI-Projekten vor dem Start?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 14) {
                                                text = 'In welchem Stadium befinden sich Ihre KI-Initiativen?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 15) {
                                                text = 'Wie messen Sie den Erfolg und Wertbeitrag Ihrer KI-Projekte?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 16) {
                                                text = 'Wie stark ist der Fokus Ihrer KI-Projekte auf die Lösung kritischer Engpässe im Kerngeschäft?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 17) {
                                                text = 'Wie hoch ist der Standardisierungsgrad Ihrer Kernprozesse?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 18) {
                                                text = 'Wie strukturiert ist Ihr Prozess für die Planung und Umsetzung von KI-Projekten?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 20) {
                                                text = 'Wie strukturiert erfolgt der Übergang von der KI-Idee in den produktiven Live-Betrieb?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 21) {
                                                text = 'Wie verbindlich ist der regulatorische Rahmen für den KI-Einsatz in Ihrem Unternehmen?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 22) {
                                                text = 'Wie konform und sicher ist Ihre Datenverarbeitung im Kontext des EU AI Acts?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 23) {
                                                text = 'Wie klar ist die Verantwortung für die Ergebnisse und Risiken von KI-Anwendungen geregelt?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 24) {
                                                text = 'Wie transparent müssen externe Partner den Einsatz und die Funktionsweise ihrer KI-Lösungen gegenüber Ihrem Unternehmen offenlegen?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 26) {
                                                text = 'Welche Tools und Plattformen stehen Ihren Teams für die Arbeit mit KI zur Verfügung? (Alles Zutreffende auswählen)';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 28) {
                                                text = 'Welches Hauptziel verfolgen Sie mit dieser KI-Bewertung?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 29) {
                                                text = 'In welchen Bereichen sehen Sie das größte Potenzial für eine KI-gestützte Optimierung? (Wählen Sie bis zu 3 Schwerpunkte)';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 30) {
                                                text = 'Inwieweit ist KI bereits fest in Ihre Unternehmensstrategie integriert?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 31) {
                                                text = 'Wer sind die treibenden Kräfte hinter der KI-Adaption in Ihrem Unternehmen? (Alles Zutreffende auswählen)';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 32) {
                                                text = 'In welchem Umfang steuern oder verantworten Sie KI-Initiativen?';
                                            }
                                            if (i18n.language === 'de' && currentQuestion.question_id === 33) {
                                                text = 'Welche Rolle beschreibt Ihre Position und Entscheidungsbefugnis am besten? (Alles Zutreffende auswählen)';
                                            }
                                            const applyText = t('wizard.selectAllThatApply', "(Select all that apply)");

                                            let parts = text.split('(Select all that apply)');
                                            if (parts.length === 1) {
                                                parts = text.split('(Mehrfachauswahl möglich)');
                                            }

                                            const renderText = (str) => {
                                                const qMarkIndex = str.indexOf('?');
                                                if (qMarkIndex !== -1 && qMarkIndex < str.trim().length - 1) {
                                                    const mainQuestion = str.substring(0, qMarkIndex + 1);
                                                    const explanation = str.substring(qMarkIndex + 1);
                                                    return (
                                                        <>
                                                            <span>{mainQuestion}</span>
                                                            <span className="font-normal text-sm md:text-base text-slate-600 block mt-1.5 leading-snug">{explanation}</span>
                                                        </>
                                                    );
                                                }
                                                return <span>{str}</span>;
                                            };

                                            if (parts.length > 1) {
                                                return (
                                                    <>
                                                        {renderText(parts[0])}
                                                        <span className="font-normal text-sm text-slate-500 block mt-1">{applyText}</span>
                                                        {parts[1] && <span className="font-normal text-sm md:text-base text-slate-600 block mt-1.5 leading-snug">{parts[1]}</span>}
                                                    </>
                                                );
                                            }
                                            return renderText(text);
                                        })()}
                                    </CardTitle>
                                </CardHeader>

                                {/* Answers Area */}
                                <CardContent className="flex-1 overflow-y-auto px-4 py-0 md:px-6 custom-scrollbar">
                                    <div className="max-w-3xl mx-auto h-full flex flex-col gap-1.5 pt-2">
                                        {renderAnswers()}
                                    </div>
                                </CardContent>

                                {/* Persistent Footer */}
                                <CardFooter className="flex-none border-t border-slate-100/50 bg-white/40 px-4 py-1.5 md:px-6 backdrop-blur-md">
                                    <div className="flex justify-between w-full items-center">
                                        <div className="flex gap-4">
                                            <Button
                                                variant="outline"
                                                disabled={currentIndex === 0}
                                                onClick={() => setCurrentIndex(prev => prev - 1)}
                                                className="border-slate-300 text-slate-600 hover:text-slate-900 hover:bg-slate-100/50 px-3 h-9 text-xs rounded-lg transition-all hover:border-slate-400"
                                            >
                                                <ChevronLeft className="w-3 h-3 mr-1" />
                                                {t('wizard.back', "Back")}
                                            </Button>
                                        </div>

                                        <div className="flex items-center gap-3">
                                            {saving && <span className="text-xs font-medium text-indigo-600 animate-pulse hidden sm:inline-block">{t('wizard.loadingSaving', "Saving...")}</span>}
                                            {currentQuestion.dimension_id === 8 && (
                                                <Button
                                                    variant="outline"
                                                    onClick={handleSkipDimension}
                                                    disabled={saving}
                                                    className="border-amber-300 bg-amber-50 text-amber-700 hover:text-amber-800 hover:bg-amber-100 px-4 h-10 text-sm font-semibold rounded-xl transition-all hover:border-amber-400 shadow-sm"
                                                >
                                                    <SkipForward className="w-4 h-4 mr-2" />
                                                    {t('wizard.skipSection', "Skip Section")}
                                                </Button>
                                            )}
                                            <Button
                                                size="lg"
                                                onClick={handleNext}
                                                disabled={saving || selectedAnswers.length === 0}
                                                className="relative px-5 h-10 text-sm font-bold rounded-xl transition-all shadow-[0_4px_10px_-2px_rgba(79,70,229,0.5)] active:scale-95 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 text-white border-0 ring-1 ring-white/20 overflow-hidden group"
                                            >
                                                {/* Shimmer Effect */}
                                                <div className="absolute inset-0 -translate-x-full group-hover:animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/20 to-transparent z-10" />

                                                <span className="relative z-20 flex items-center font-bold tracking-wide">
                                                    {currentIndex === questions.length - 1 ? t('wizard.finish', "Finish") : t('wizard.next', "Next")}
                                                    {!saving && (currentIndex === questions.length - 1 ? <CheckCircle2 className="w-4 h-4 ml-2" /> : <ArrowRight className="w-4 h-4 ml-2" />)}
                                                </span>
                                            </Button>
                                        </div>
                                    </div>
                                </CardFooter>

                            </Card>
                        </motion.div>
                    </AnimatePresence>
                </div>
            </main>
        </div>
    );
}
