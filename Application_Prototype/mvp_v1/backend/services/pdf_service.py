import os
import re
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Polygon, Line
from reportlab.graphics.charts.spider import SpiderChart
from reportlab.graphics.charts.legends import Legend
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Frame, PageTemplate, NextPageTemplate, KeepTogether
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class PDFService:
    def __init__(self):
        pass

    def _header_footer(self, canvas, doc):
        """
        Draws the header and footer on every page (except cover).
        """
        canvas.saveState()
        
        # Only draw header/footer if not page 1
        page_num = canvas.getPageNumber()
        if page_num > 1:
            # Header Line
            canvas.setStrokeColor(colors.HexColor('#e2e8f0'))
            canvas.setLineWidth(1)
            canvas.line(1.5*cm, A4[1] - 1.5*cm, A4[0] - 1.5*cm, A4[1] - 1.5*cm)
            
            # Header Text
            canvas.setFont('Helvetica-Bold', 8)
            canvas.setFillColor(colors.HexColor('#94a3b8'))
            canvas.drawString(1.5*cm, A4[1] - 1.2*cm, "AI EVOLUTION BLUEPRINT")
            
            canvas.setFont('Helvetica', 8)
            canvas.drawRightString(A4[0] - 1.5*cm, A4[1] - 1.2*cm, "CONFIDENTIAL")
            
            # Footer Line
            canvas.line(1.5*cm, 1.5*cm, A4[0] - 1.5*cm, 1.5*cm)
            
            # Footer Text
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.HexColor('#94a3b8'))
            canvas.drawString(1.5*cm, 1.0*cm, "© 2024 AI-Compass Intelligence")
            
            canvas.drawRightString(A4[0] - 1.5*cm, 1.0*cm, f"Page {page_num}")
        
        canvas.restoreState()

    def _format_text(self, text):
        """
        Cleans and formats Markdown-style text for ReportLab Paragraphs.
        Handles bold (**), headers (#), and bullets (*/-).
        """
        if not text:
            return ""
        
        # 1. Bold: **text** -> <b>text</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # 2. Italic: *text* -> <i>text</i> (Basic handling, careful with bullets)
        # We'll skip simple italics for now to avoid Bullet confusion or handle bullets first.
        
        # 3. Headers: # Header -> <b>Header</b><br/>
        # Handle #, ##, ### at start of line or string
        text = re.sub(r'(?m)^#{1,6}\s*(.*)$', r'<b>\1</b><br/>', text)
        
        # 4. Bullets: * or - at start of line -> • 
        # Using non-breaking space for indentation
        text = re.sub(r'(?m)^[\*\-]\s+(.*)$', r'&nbsp;&nbsp;• \1<br/>', text)
        
        # 5. Newlines to <br/> (collapse multiple to avoid large gaps)
        text = re.sub(r'\n+', '\n', text)
        text = text.replace('\n', '<br/>')
        
        return text

    def generate_pdf(self, data):
        """
        Generates PDF bytes using ReportLab Platypus with Luxury Design.
        """
        import datetime
        import re
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5*cm, leftMargin=1.5*cm,
            topMargin=2.5*cm, bottomMargin=2.5*cm,
            title="AI-Compass Maturity Report"
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # --- Brand Colors ---
        col_primary = colors.HexColor('#4338ca')   # Indigo 700
        col_accent = colors.HexColor('#6366f1')    # Indigo 500
        col_text = colors.HexColor('#0f172a')      # Slate 900
        col_subtext = colors.HexColor('#64748b')   # Slate 500
        col_bg_light = colors.HexColor('#f8fafc')  # Slate 50
        col_light_border = colors.HexColor('#e2e8f0')
        col_amber_bg = colors.HexColor('#fffbeb')  # Amber 50
        col_amber_text = colors.HexColor('#b45309') # Amber 700
        col_red_bg = colors.HexColor('#fef2f2')    # Red 50
        col_red_text = colors.HexColor('#b91c1c')  # Red 700
        
        # --- Custom Styles ---
        style_cover_title = ParagraphStyle('CoverTitle', parent=styles['Heading1'], fontSize=32, leading=40, textColor=col_primary, alignment=TA_CENTER, spaceAfter=20)
        style_cover_sub = ParagraphStyle('CoverSub', parent=styles['Normal'], fontSize=14, textColor=col_subtext, alignment=TA_CENTER)
        
        style_h1 = ParagraphStyle('H1', parent=styles['Heading2'], fontSize=15, leading=18, textColor=col_primary, spaceBefore=10, spaceAfter=8, fontName='Helvetica-Bold')
        style_h2 = ParagraphStyle('H2', parent=styles['Heading3'], fontSize=12, textColor=col_text, spaceBefore=12, spaceAfter=6, fontName='Helvetica-Bold')
        style_normal = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=15, textColor=col_text)
        
        style_score_label = ParagraphStyle('ScoreLabel', parent=styles['Normal'], fontSize=9, textColor=col_subtext, alignment=TA_CENTER, textTransform='uppercase', letterSpacing=1)
        style_score_val = ParagraphStyle('ScoreVal', parent=styles['Normal'], fontSize=42, textColor=col_primary, alignment=TA_CENTER, leading=46, fontName='Helvetica-Bold')
        style_score_sub = ParagraphStyle('ScoreSub', parent=styles['Normal'], fontSize=11, textColor=col_text, alignment=TA_CENTER)

        # --- Data Prep ---
        company = data.get("company", {})
        date_str = datetime.date.today().strftime("%B %d, %Y")
        overall_score = data.get("overall_score", 0.0)
        pct_data = data.get("percentile", {})
        percentile_rank = pct_data.get("percentage", "N/A") if isinstance(pct_data, dict) else "N/A"
        peer_group = pct_data.get("industry", "Global") if isinstance(pct_data, dict) else "Global"
        cluster = data.get("cluster", {})
        cluster_name = str(cluster.get("cluster_name") or "Unknown").replace(" - ", ": ")
        
        # ====================
        # PAGE 1: COVER PAGE
        # ====================
        story.append(Spacer(1, 3*cm))
        
        # --- Logo - Use PNG from assets ---
        import os
        from reportlab.platypus import Image as RLImage
        
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'public', 'ai_compass_logo.png')
        
        if os.path.exists(logo_path):
            # Use actual PNG logo with text next to it (like webapp)
            # Match logo height with text height for unified appearance
            logo_img = RLImage(logo_path, width=0.85*cm, height=0.85*cm, kind='proportional')
            # Set explicit alignment to prevent any inherited spacing issues
            logo_text = Paragraph("AI Compass", ParagraphStyle('LogoText', parent=styles['Normal'], fontSize=22, fontName='Helvetica-Bold', textColor=col_primary, leading=26, alignment=TA_LEFT))
            
            # Create a tight branding component (snug width to ensure centering)
            # 1.1cm for logo + 5.2cm for text is calculated to be snug for "AI Compass" at 22pt
            branding_component = Table([[logo_img, logo_text]], colWidths=[1.1*cm, 5.2*cm])
            branding_component.setStyle(TableStyle([
                ('ALIGN', (0,0), (0,0), 'RIGHT'),
                ('ALIGN', (1,0), (1,0), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING', (1,0), (1,0), 10),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('LEFTPADDING', (0,0), (0,0), 0),
                ('RIGHTPADDING', (1,0), (1,0), 0),
            ]))
            
            # Wrap in a full-width table to force absolute horizontal centering
            logo_outer_table = Table([[branding_component]], colWidths=[18*cm])
            logo_outer_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            story.append(logo_outer_table)
        else:
            # Fallback to drawn logo if PNG not found
            logo_drawing = Drawing(200, 50)
            box_size = 40
            box_x = 80
            box_y = 5
            logo_drawing.add(Rect(box_x, box_y, box_size, box_size, fillColor=col_primary, strokeColor=None, rx=8, ry=8))
            logo_drawing.add(Circle(box_x + box_size/2, box_y + box_size/2, 12, fillColor=colors.white, strokeColor=None))
            text_x = box_x + box_size + 15
            text_y = box_y + box_size/2 - 8
            logo_drawing.add(String(text_x, text_y, "AI COMPASS", fontName='Helvetica-Bold', fontSize=20, fillColor=col_primary, textAnchor='start'))
            
            logo_table = Table([[logo_drawing]], colWidths=[16*cm])
            logo_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
            story.append(logo_table)
        
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("Executive Results Report", style_cover_title))
        story.append(Paragraph("STRATEGIC MATURITY ASSESSMENT", style_cover_sub))
        
        story.append(Spacer(1, 2.5*cm))
        
        cover_info = [
            [Paragraph(f"PREPARED FOR:", ParagraphStyle('C1', parent=style_score_label, alignment=TA_CENTER))],
            [Paragraph(f"<b>{company.get('name', 'Confidential Company')}</b>", ParagraphStyle('C2', parent=style_normal, fontSize=14, alignment=TA_CENTER))],
            [Spacer(1, 10)],
            [Paragraph(f"{date_str}", ParagraphStyle('C3', parent=style_normal, fontSize=11, textColor=col_subtext, alignment=TA_CENTER))]
        ]
        t_cover = Table(cover_info, colWidths=[10*cm])
        t_cover.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        story.append(t_cover)
        story.append(PageBreak())
        
        # ====================
        # PAGE 2: MATURITY HERO & VALUE GROWTH
        # ====================
        
        # 1. Hero Score Block
        left_score_block = [
            [Paragraph("OVERALL MATURITY", style_score_label)],
            [Paragraph(f"{overall_score}", style_score_val)],
            [Paragraph("/ 5.0", ParagraphStyle('tiny', parent=style_score_label, fontSize=10))],
        ]
        
        # Clean cluster name
        clean_cluster_name = re.sub(r'^\d+\s*[-:]\s*', '', cluster_name)
        
        right_metrics_block = [
            [Paragraph("INDUSTRY BENCHMARK", style_score_label)],
            [Paragraph(f"Top <b>{percentile_rank}%</b>", style_score_sub)],
            [Paragraph(f"vs {peer_group} Peers", ParagraphStyle('tiny', parent=style_score_label, textTransform='none'))],
            [Spacer(1, 15)],
            [Paragraph("CLUSTER PROFILE", style_score_label)],
            [Paragraph(f"<b>{clean_cluster_name}</b>", style_score_sub)],
        ]
        
        hero_table = Table([[Table(left_score_block, colWidths=[6*cm]), Table(right_metrics_block, colWidths=[6*cm])]], colWidths=[8*cm, 8*cm])
        hero_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LINEAFTER', (0,0), (0,0), 0.5, col_light_border),
            ('BACKGROUND', (0,0), (-1,-1), col_bg_light),
            ('BOX', (0,0), (-1,-1), 0.5, col_light_border),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(hero_table)
        story.append(Spacer(1, 0.35*cm))

        # 2. Cluster Profile
        kp_analysis = []
        display_cluster_name = re.sub(r'^\d+\s*[-:]\s*', '', cluster_name)
        kp_analysis.append(Paragraph(f"Your Cluster Profile: <b>{display_cluster_name}</b>", style_h1))
        
        clusters_def = [
            {"id": 1, "name": "Traditionalist", "h": 0.2},
            {"id": 2, "name": "Explorer", "h": 0.4},
            {"id": 3, "name": "Builder", "h": 0.6},
            {"id": 4, "name": "Scaler", "h": 0.8},
            {"id": 5, "name": "Leader", "h": 1.0},
        ]
        active_id = 1
        c_name_raw = cluster.get("cluster_name")
        if c_name_raw:
             m = re.match(r"(\d+)", str(c_name_raw))
             if m: active_id = int(m.group(1))
        
        vg_drawing = Drawing(453, 75)
        bar_gap = 10
        avail_w = 453 - (bar_gap * 4)
        single_bar_w = avail_w / 5
        x_cursor = 0
        for c_def in clusters_def:
            is_active = (c_def['id'] == active_id)
            fill_c = colors.HexColor('#4f46e5') if is_active else colors.HexColor('#f1f5f9')
            vg_drawing.add(Rect(x_cursor, 12, single_bar_w, c_def['h'] * 55, fillColor=fill_c, strokeColor=None, rx=4, ry=4))
            
            lbl_color = colors.HexColor('#4338ca') if is_active else colors.HexColor('#64748b')
            font_n = 'Helvetica-Bold' if is_active else 'Helvetica'
            vg_drawing.add(String(x_cursor + single_bar_w/2, 5, c_def['name'], textAnchor='middle', fontName=font_n, fontSize=8, fillColor=lbl_color))
            x_cursor += single_bar_w + bar_gap
            
        kp_analysis.append(vg_drawing)
        # Remove cluster description to save space
        
        story.append(Paragraph(f"Your Cluster Profile: <b>{display_cluster_name}</b>", style_h1))
        story.append(vg_drawing)
        story.append(Spacer(1, 0.35*cm))

        # 3. Dimension Profile (Same Page as Cluster)
        # ====================
        
        story.append(Paragraph("The Multi-Dimensional Maturity Profile", style_h1))
        
        dim_scores = data.get("dimension_scores", {})
        if dim_scores:
            dim_rows = []
            bar_width_pts = 160
            for dim, score in dim_scores.items():
                d = Drawing(bar_width_pts, 8)
                d.add(Rect(0, 1, bar_width_pts, 5, fillColor=colors.HexColor('#f1f5f9'), strokeColor=None, rx=2, ry=2))
                
                pct = max(0, min(1, score / 5.0))
                w = pct * bar_width_pts
                c = colors.HexColor('#6366f1')
                if score < 2.5: c = colors.HexColor('#fb923c')
                if score > 4.0: c = colors.HexColor('#4338ca')
                
                if w > 0: d.add(Rect(0, 1, w, 5, fillColor=c, strokeColor=None, rx=2, ry=2))
                    
                dim_rows.append([
                    Paragraph(dim, ParagraphStyle('DL', parent=style_normal, fontSize=8)),
                    d,
                    Paragraph(f"{score:.1f}", ParagraphStyle('DS', parent=style_normal, fontSize=8, alignment=TA_RIGHT))
                ])
            
            dim_table = Table(dim_rows, colWidths=[5.5*cm, 8.5*cm, 1.5*cm])
            dim_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
            story.append(dim_table)
            
        story.append(PageBreak())  # Force Page 3 to start here

        # ====================
        # PAGE 3: STRATEGIC GAP ANALYSIS
        # ====================
        
        # Main heading: Strategic Gap Analysis
        story.append(Paragraph("Strategic Gap Analysis", style_h1))
        story.append(Spacer(1, 0.4*cm))
        
        # 1. Executive Briefing (as subheading)
        kp_briefing = []
        kp_briefing.append(Paragraph("Executive Briefing", style_h2))
        briefing = data.get("executive_briefing", "No detailed briefing available.")
        
        # Card-style design with icon and label
        clean_briefing = self._format_text(briefing)
        
        # Header with icon and label
        briefing_header = Table([[
            Paragraph("<font color='#4f46e5' size=16><b>📋</b></font>", style_normal),
            Paragraph("<font color='#4f46e5'><b>KEY INSIGHTS</b></font>", ParagraphStyle('BriefingLabel', parent=style_normal, fontSize=9, textTransform='uppercase'))
        ]], colWidths=[1*cm, 14.5*cm])
        briefing_header.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (0,0), 0),
        ]))
        
        # Content
        briefing_text = Paragraph(clean_briefing, ParagraphStyle('BriefingText', parent=style_normal, fontSize=10, leading=16, textColor=colors.HexColor('#334155')))
        
        # Combine into card
        briefing_card = Table([
            [briefing_header],
            [briefing_text]
        ], colWidths=[15.5*cm])
        briefing_card.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('BOX', (0,0), (-1,-1), 0.5, col_light_border),
            ('LINEABOVE', (0,0), (-1,0), 2, col_primary),
            ('TOPPADDING', (0,0), (-1,0), 8),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,1), (-1,1), 6),
            ('BOTTOMPADDING', (0,1), (-1,1), 8),
        ]))
        kp_briefing.append(briefing_card)
        story.append(KeepTogether(kp_briefing))
        story.append(Spacer(1, 0.5*cm))

        # 2. Strategic Gaps (no heading - already set above)
        kp_gaps = []
        kp_gaps.append(Paragraph("Critical Findings", style_h2))
        gaps = data.get("strategic_gaps", []) or []

        if gaps:
            for gap in gaps:
                g_type = (gap.get("type", "")).lower()
                if 'structural' in g_type or 'anomaly' in g_type:
                    card_bg = col_amber_bg
                    card_border = colors.HexColor('#fed7aa')
                    icon_char = "!"
                    icon_color = col_amber_text
                    badge_text = "STRUCTURAL IMBALANCE"
                else:
                    card_bg = col_red_bg
                    card_border = colors.HexColor('#fecaca')
                    icon_char = "▼"
                    icon_color = col_red_text
                    badge_text = "CRITICAL WEAKNESS"
                
                header_row = [
                    Paragraph(f"<font color='{icon_color.hexval()}' size=14><b>{icon_char}</b></font>", style_normal),
                    Paragraph(f"<font color='{icon_color.hexval()}'><b>{badge_text}</b></font>", ParagraphStyle('Badge', parent=style_normal, fontSize=8)),
                    Paragraph(f"<b>{gap.get('title', 'Gap').replace('Critical Gap: ', '')}</b>", ParagraphStyle('GapTitle', parent=style_normal, fontSize=12)),
                    Paragraph(f"<b>{gap.get('score', 0):.1f}</b>", ParagraphStyle('GapScore', parent=style_normal, fontSize=14, alignment=TA_CENTER, textColor=col_subtext))
                ]
                
                context_row = [
                    Paragraph(self._format_text(gap.get("context", "")), ParagraphStyle('GapBody', parent=style_normal, fontSize=10, leading=11, textColor=colors.HexColor('#334155')))
                ]

                risk_rows = []
                if gap.get("strategic_risk"):
                    risk_content = Paragraph(f"<b>STRATEGIC IMPLICATION:</b> <i>{gap.get('strategic_risk')}</i>", ParagraphStyle('Risk', parent=style_normal, fontSize=9, leading=10, textColor=colors.HexColor('#475569')))
                    risk_rows.append([risk_content])

                t_head = Table([[header_row[0], header_row[1], header_row[2], header_row[3]]], colWidths=[0.8*cm, 3.2*cm, 9.5*cm, 1.5*cm])
                t_head.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('ALIGN', (3,0), (3,0), 'CENTER'),
                ]))

                rows = [[t_head], [context_row[0]]]
                if risk_rows:
                    t_risk = Table(risk_rows, colWidths=[15*cm])
                    t_risk.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,-1), colors.white),
                        ('BOX', (0,0), (-1,-1), 0.5, card_border),
                        ('PADDING', (0,0), (-1,-1), 8),
                    ]))
                    rows.append([t_risk])

                card_table = Table(rows, colWidths=[15.5*cm])
                card_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), card_bg),
                    ('BOX', (0,0), (-1,-1), 0.5, card_border),
                    ('TOPPADDING', (0,0), (-1,-1), 8),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                    ('LEFTPADDING', (0,0), (-1,-1), 10),
                    ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ]))
                
                kp_gaps.append(card_table)
                kp_gaps.append(Spacer(1, 0.4*cm))

        else:
            kp_gaps.append(Paragraph("No critical gaps detected.", style_normal))

        story.append(KeepTogether(kp_gaps))
        story.append(PageBreak())

        # ====================
        # PAGE 4: TRANSFORMATION ROADMAP
        # ====================
        
        story.append(Paragraph("\"Next Best Action\" Roadmap", style_h1))
        roadmap = data.get("roadmap", {}) or {}
        
        for i, (phase, items) in enumerate(roadmap.items()):
            kp_phase = []
            kp_phase.append(Paragraph(phase.upper(), ParagraphStyle('PhaseHeader', parent=style_normal, fontName='Helvetica-Bold', fontSize=10, textColor=col_primary, spaceAfter=8)))
            
            if items:
                item_rows = []
                for item in items:
                    theme = item.get("theme", "Action")
                    explanation_raw = item.get("explanation", "")
                    
                    parts = [p.strip() for p in explanation_raw.split('\n') if p.strip()]
                    analysis_text = ""
                    actions = []
                    
                    analysis_part = next((p for p in parts if 'analysis' in p.lower()), None) or parts[0] if parts else ""
                    if analysis_part:
                        analysis_text = analysis_part.replace('**Analysis**', '').replace('Analysis:', '').replace('**', '').strip().lstrip(':').strip()
                         
                    action_parts = [p for p in parts if 'action' in p.lower() and ('-' in p or '*' in p or '•' in p)]
                    for act in action_parts:
                        clean_act = act.replace('-', '').replace('*', '').replace('•', '').strip()
                        if ':' in clean_act and 'action' in clean_act.lower().split(':')[0]: clean_act = clean_act.split(':', 1)[1].strip()
                        actions.append(clean_act)

                    content_stack = []
                    content_stack.append(Paragraph(f"<b>{theme}</b>", ParagraphStyle('RecTitle', parent=style_normal, fontSize=10, leading=11)))
                    if analysis_text:
                        content_stack.append(Paragraph(f"<font color='#475569'>{analysis_text}</font>", ParagraphStyle('Analysis', parent=style_normal, fontSize=9, leading=10)))
                        content_stack.append(Spacer(1, 2))
                         
                    if actions:
                        for idx, action_text in enumerate(actions):
                            act_row = [
                                Paragraph("→", ParagraphStyle('Arrow', parent=style_normal, textColor=col_primary, fontSize=10, alignment=TA_CENTER)),
                                Paragraph(f"<b>ACTION {idx+1}</b>: <font color='#64748b'>{action_text}</font>", ParagraphStyle('ActTxt', parent=style_normal, fontSize=9, leading=10))
                            ]
                            content_stack.append(Table([act_row], colWidths=[0.6*cm, 12*cm]))
                            content_stack.append(Spacer(1, 1))
                            
                    item_rows.append([Paragraph("•", ParagraphStyle('Bullet', parent=style_normal, textColor=col_accent, fontSize=14, alignment=TA_CENTER)), content_stack])
                    item_rows.append([None, Spacer(1, 8)])
                
                items_table = Table(item_rows, colWidths=[0.8*cm, 14.2*cm])
                items_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
                
                card_table = Table([[items_table]], colWidths=[16*cm])
                card_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.white), ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 10)]))
                kp_phase.append(card_table)
            else:
                 kp_phase.append(Paragraph("No immediate actions.", style_normal))
            
            story.append(KeepTogether(kp_phase))
            story.append(Spacer(1, 0.6*cm))

        # Build
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal', showBoundary=0)
        template = PageTemplate(id='StandardParams', frames=frame, onPage=self._header_footer)
        doc.addPageTemplates([template])
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()
