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
        
        # 5. Newlines to <br/>
        text = text.replace('\n', '<br/>')
        
        return text

    def generate_pdf(self, data):
        """
        Generates PDF bytes using ReportLab Platypus with Luxury Design.
        """
        import datetime
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5*cm, leftMargin=1.5*cm,
            topMargin=2.5*cm, bottomMargin=2.5*cm, # Increased margins for header/footer space
            title="AI-Compass Maturity Report"
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # --- Brand Colors ---
        col_primary = colors.HexColor('#4338ca')   # Indigo 700 (Darker/Richer)
        col_accent = colors.HexColor('#6366f1')    # Indigo 500
        col_text = colors.HexColor('#0f172a')      # Slate 900
        col_subtext = colors.HexColor('#64748b')   # Slate 500
        col_bg_light = colors.HexColor('#f8fafc')  # Slate 50
        col_light_border = colors.HexColor('#e2e8f0')
        
        # --- Custom Styles ---
        style_cover_title = ParagraphStyle(
            'CoverTitle', 
            parent=styles['Heading1'], 
            fontSize=32, 
            leading=40,
            textColor=col_primary, 
            alignment=TA_CENTER,
            spaceAfter=20
        )
        style_cover_sub = ParagraphStyle(
            'CoverSub', 
            parent=styles['Normal'], 
            fontSize=14, 
            textColor=col_subtext, 
            alignment=TA_CENTER
        )
        
        style_h1 = ParagraphStyle(
            'H1', 
            parent=styles['Heading2'], 
            fontSize=16, 
            leading=20,
            textColor=col_primary, 
            spaceBefore=24, 
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        style_h2 = ParagraphStyle(
            'H2', 
            parent=styles['Heading3'], 
            fontSize=12, 
            textColor=col_text, 
            spaceBefore=12, 
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        style_normal = ParagraphStyle(
            'Body', 
            parent=styles['Normal'], 
            fontSize=10, 
            leading=15, 
            textColor=col_text
        )
        
        style_score_label = ParagraphStyle('ScoreLabel', parent=styles['Normal'], fontSize=9, textColor=col_subtext, alignment=TA_CENTER, textTransform='uppercase', letterSpacing=1)
        style_score_val = ParagraphStyle('ScoreVal', parent=styles['Normal'], fontSize=48, textColor=col_primary, alignment=TA_CENTER, leading=50, fontName='Helvetica-Bold')
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
        # We want the cover page to be centered vertically, so we add spacers
        story.append(Spacer(1, 3*cm))
        
        # AI Compass Logo (matching frontend design)
        # Create a horizontal layout with gradient box + icon + text
        logo_drawing = Drawing(300, 60)
        
        # Calculate centering - total logo width is approximately 180 (box 40 + gap 15 + text ~125)
        # Center this within the 300pt drawing width
        total_logo_width = 180
        start_x = (300 - total_logo_width) / 2
        
        # Gradient background box (blue-600 to purple-600)
        box_size = 40
        box_x = start_x
        box_y = 10
        
        # Create gradient effect with overlapping rectangles
        logo_drawing.add(Rect(box_x, box_y, box_size, box_size, 
                              fillColor=colors.HexColor('#2563eb'), strokeColor=None, rx=6, ry=6))
        logo_drawing.add(Rect(box_x, box_y, box_size, box_size, 
                              fillColor=colors.HexColor('#9333ea'), strokeColor=None, rx=6, ry=6, 
                              fillOpacity=0.5))
        
        # Compass icon (simplified - circle with directional lines)
        icon_center_x = box_x + box_size/2
        icon_center_y = box_y + box_size/2
        icon_radius = 12
        
        # Outer circle
        logo_drawing.add(Circle(icon_center_x, icon_center_y, icon_radius, 
                               fillColor=None, strokeColor=colors.white, strokeWidth=2))
        # North pointer
        logo_drawing.add(Polygon([icon_center_x, icon_center_y + icon_radius - 2,
                                 icon_center_x + 3, icon_center_y,
                                 icon_center_x, icon_center_y - icon_radius + 2,
                                 icon_center_x - 3, icon_center_y],
                                fillColor=colors.white, strokeColor=None))
        # Center dot
        logo_drawing.add(Circle(icon_center_x, icon_center_y, 2, 
                               fillColor=colors.white, strokeColor=None))
        
        # "AI COMPASS" text next to the box
        text_x = box_x + box_size + 15
        text_y = box_y + box_size/2 - 8
        logo_drawing.add(String(text_x, text_y, "AI COMPASS", 
                               fontName='Helvetica-Bold', fontSize=20, 
                               fillColor=col_primary, textAnchor='start'))
        
        # Wrap in table to center on page
        logo_table = Table([[logo_drawing]], colWidths=[16*cm])
        logo_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(logo_table)
        
        story.append(Spacer(1, 2*cm))
        
        story.append(Paragraph("Executive Results Report", style_cover_title))
        story.append(Paragraph("STRATEGIC MATURITY ASSESSMENT", style_cover_sub))
        
        story.append(Spacer(1, 4*cm))
        
        # Company Info Box
        cover_info = [
            [Paragraph(f"PREPARED FOR:", ParagraphStyle('C1', parent=style_score_label, alignment=TA_CENTER))],
            [Paragraph(f"<b>{company.get('name', 'Confidential Company')}</b>", ParagraphStyle('C2', parent=style_normal, fontSize=14, alignment=TA_CENTER))],
            [Spacer(1, 10)],
            [Paragraph(f"{date_str}", ParagraphStyle('C3', parent=style_normal, fontSize=11, textColor=col_subtext, alignment=TA_CENTER))]
        ]
        
        t_cover = Table(cover_info, colWidths=[10*cm])
        t_cover.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        story.append(t_cover)
        
        import re
        
        story.append(PageBreak())
        
        # ====================
        # PAGE 2: EXECUTIVE SUMMARY & SCORE
        # ====================
        
        # Score Board
        # Layout: Left side Score, Right side Cluster/Percentile
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
        
        t_left = Table(left_score_block, colWidths=[6*cm])
        t_right = Table(right_metrics_block, colWidths=[6*cm])
        
        hero_table = Table([[t_left, t_right]], colWidths=[8*cm, 8*cm])
        hero_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (0,0), 'CENTER'), # Left cell center
            ('ALIGN', (1,0), (1,0), 'CENTER'), # Right cell center
            ('LINEAFTER', (0,0), (0,0), 0.5, col_light_border), # Vertical divider
            ('BACKGROUND', (0,0), (-1,-1), col_bg_light),
            ('BOX', (0,0), (-1,-1), 0.5, col_light_border),
            # ('ROUNDEDCORNERS', [10,10,10,10]), # Not always supported, ignore errors
            ('TOPPADDING', (0,0), (-1,-1), 20),
            ('BOTTOMPADDING', (0,0), (-1,-1), 20),
        ]))
        story.append(hero_table)
        story.append(Spacer(1, 0.8*cm))

        # ====================
        # VALUE GROWTH CHART (New)
        # ====================
        kp_vg = []
        kp_vg.append(Paragraph("Value Growth Profile", style_h1))
        
        # Cluster Definitions for Chart logic
        clusters_def = [
            {"id": 1, "name": "Traditionalist", "h": 0.2},
            {"id": 2, "name": "Explorer", "h": 0.4},
            {"id": 3, "name": "Builder", "h": 0.6},
            {"id": 4, "name": "Scaler", "h": 0.8},
            {"id": 5, "name": "Leader", "h": 1.0},
        ]
        
        # Determine active ID from cluster name
        # Determine active ID from cluster name
        active_id = 1
        c_name_raw = cluster.get("cluster_name")
        if c_name_raw:
             # Try to find leading digit
             import re
             m = re.match(r"(\d+)", str(c_name_raw))
             if m:
                 active_id = int(m.group(1))
        
        # Drawing
        chart_w = 16*cm
        chart_h = 4*cm
        bar_gap = 10
        # Convert cm to pts for Shapes
        total_w_pts = chart_w
        total_h_pts = chart_h
        
        # Calculate bar widths in PTS
        # 16cm is approx 453 pts
        avail_w = 453 - (bar_gap * 4)
        single_bar_w = avail_w / 5
        
        vg_drawing = Drawing(453, 130) # slight height adjustment
        
        x_cursor = 0
        for c_def in clusters_def:
            is_active = (c_def['id'] == active_id)
            
            # simple logic: max height 100 pts
            max_bar_h = 100
            b_height = c_def['h'] * max_bar_h 
            y_start = 20 # space for text below
            
            # Color
            if is_active:
                fill_c = colors.HexColor('#4f46e5') # Indigo
            else:
                fill_c = colors.HexColor('#f1f5f9') # Slate 100
                
            # Bar Rect
            bar = Rect(x_cursor, y_start, single_bar_w, b_height, fillColor=fill_c, strokeColor=None, rx=4, ry=4)
            vg_drawing.add(bar)
            
            # Label
            label_text = c_def['name']
            
            lbl_color = colors.HexColor('#4338ca') if is_active else colors.HexColor('#64748b')
            font_n = 'Helvetica-Bold' if is_active else 'Helvetica'
            
            # Text centered under bar
            s = String(x_cursor + single_bar_w/2, 5, label_text, textAnchor='middle', fontName=font_n, fontSize=8, fillColor=lbl_color)
            vg_drawing.add(s)
            
            x_cursor += single_bar_w + bar_gap
            
        kp_vg.append(vg_drawing)
        story.append(KeepTogether(kp_vg))
        story.append(Spacer(1, 1*cm))

        # ====================
        # DIMENSION PROFILE SECTION (Moved Up)
        # ====================
        kp_maturity = []
        kp_maturity.append(Paragraph("The Multi-Dimensional Maturity Profile", style_h1))
        kp_maturity.append(Paragraph("Breakdown of performance across core capabilities.", ParagraphStyle('DimSub', parent=style_normal, fontSize=10, textColor=col_subtext)))
        kp_maturity.append(Spacer(1, 10))
        
        dim_scores = data.get("dimension_scores", {})
        if dim_scores:
            dim_rows = []
            # Width for the bar chart part
            bar_width_pts = 200 
            
            for dim, score in dim_scores.items():
                # Create a simple bar chart drawing
                d = Drawing(bar_width_pts, 12)
                
                # Background track (light grey)
                d.add(Rect(0, 3, bar_width_pts, 6, fillColor=colors.HexColor('#f1f5f9'), strokeColor=None, rx=3, ry=3))
                
                # Value bar (colored)
                pct = max(0, min(1, score / 5.0))
                w = pct * bar_width_pts
                
                # Color logic: Low=Orange, Mid=Indigo, High=Dark Indigo
                c = colors.HexColor('#6366f1') # Default Indigo
                if score < 2.5: c = colors.HexColor('#fb923c') # Orange
                if score > 4.0: c = colors.HexColor('#4338ca') # Dark Indigo
                
                if w > 0:
                    d.add(Rect(0, 3, w, 6, fillColor=c, strokeColor=None, rx=3, ry=3))
                    
                row = [
                    Paragraph(dim, ParagraphStyle('DL', parent=style_normal, fontSize=9, textColor=col_text)),
                    d,
                    Paragraph(f"{score:.1f}/5.0", ParagraphStyle('DS', parent=style_normal, fontSize=9, textColor=col_subtext, alignment=TA_RIGHT))
                ]
                dim_rows.append(row)
            
            dim_table = Table(dim_rows, colWidths=[6*cm, 8*cm, 2*cm])
            dim_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            kp_maturity.append(dim_table)
        
        story.append(KeepTogether(kp_maturity))
        
        story.append(Spacer(1, 0.5*cm))
        
        # ====================
        # EXECUTIVE BRIEFING (Moved Down)
        # ====================
        kp_briefing = []
        kp_briefing.append(Paragraph("Executive Summary", style_h1))
        briefing = data.get("executive_briefing", "No detailed briefing available.")
        
        # Premium Design: Two-column layout with visual accent
        # Col 1: Decorative Quote Icon (simulated with large text for now, or a Drawing)
        # Col 2: Text content
        
        # Large Quote Mark
        quote_style = ParagraphStyle('QuoteMark', parent=style_normal, fontSize=50, leading=60, textColor=col_primary, alignment=TA_CENTER)
        quote_col = Paragraph("“", quote_style)
        
        # Main Text - Larger, more readable, dark slate
        text_style = ParagraphStyle('BriefingText', parent=style_normal, fontSize=11, leading=18, textColor=colors.HexColor('#1e293b'))
        clean_briefing = self._format_text(briefing)
        text_col = Paragraph(clean_briefing, text_style)
        
        briefing_data = [[quote_col, text_col]]
        
        briefing_table = Table(briefing_data, colWidths=[1.5*cm, 14*cm])
        briefing_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), # Very light background
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')), # Subtle border
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 15),
            ('TOPPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,0), (-1,-1), 20),
            
            # Accent line on top instead of left
            ('LINEABOVE', (0,0), (-1,0), 3, col_primary),
        ]))
        
        kp_briefing.append(briefing_table)
        story.append(KeepTogether(kp_briefing))
        
        story.append(Spacer(1, 0.5*cm))
        
        # Cluster Description Detail
        story.append(Paragraph("Analysis", style_h2))
        # Cluster Description Detail
        story.append(Paragraph("Analysis", style_h2))
        cluster_desc = cluster.get('description', 'Your organization aligns with this pattern of AI adoption.')
        
        display_name = re.sub(r'^\d+\s*[-:]\s*', '', cluster_name)
        clean_desc = self._format_text(cluster_desc)
        story.append(Paragraph(f"<b>{display_name}:</b> {clean_desc}", style_normal))
        
        story.append(PageBreak())
        
        # ====================
        # PAGE 3: GAPS & ROADMAP
        # ====================
        
        # Strategic Gaps
        story.append(Paragraph("Strategic Gaps & Risks", style_h1))
        gaps = data.get("strategic_gaps", []) or []
        
        if gaps:
            # We use a clean list style instead of a heavy grid
            for gap in gaps:
                title = gap.get("title", "Gap")
                score = round(gap.get("score", 0), 1)
                context = gap.get("context", "")
                
                # Header Row
                gap_color = colors.HexColor('#ef4444') if score > 3 else colors.HexColor('#f97316')
                
                # Title
                story.append(Paragraph(f"<font color='{gap_color.hexval()}'>●</font> <b>{title}</b> <font size=8 color='#64748b'>(Impact Score: {score})</font>", style_normal))
                
                # Context
                story.append(Spacer(1, 2))
                clean_context = self._format_text(context)
                story.append(Paragraph(clean_context, ParagraphStyle('Indented', parent=style_normal, leftIndent=12, textColor=col_subtext)))
                story.append(Spacer(1, 10))
        else:
            story.append(Paragraph("No critical findings.", style_normal))
            
        story.append(Spacer(1, 1*cm))
        
        # Transformation Roadmap (Redesigned)
        story.append(Paragraph("Transformation Roadmap", style_h1))
        roadmap = data.get("roadmap", {}) or {}
        
        for i, (phase, items) in enumerate(roadmap.items()):
            kp_phase = []
            
            # Phase Header
            kp_phase.append(Paragraph(phase.upper(), ParagraphStyle('PhaseHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=col_primary, spaceAfter=8)))
            
            # Content Box
            if items:
                # Build list of items
                item_rows = []
                for item in items:
                    theme = item.get("theme", "Action")
                    explanation_raw = item.get("explanation", "")
                    
                    # --- PARSING LOGIC ---
                    parts = [p.strip() for p in explanation_raw.split('\n') if p.strip()]
                    
                    analysis_text = ""
                    actions = []
                    
                    # 1. Analysis
                    analysis_part = next((p for p in parts if 'analysis' in p.lower()), None)
                    if not analysis_part and parts: 
                         analysis_part = parts[0]
                    
                    if analysis_part:
                         clean_an = analysis_part.replace('**Analysis**', '').replace('Analysis:', '').replace('**', '').strip()
                         if clean_an.startswith(':'): clean_an = clean_an[1:].strip()
                         analysis_text = clean_an
                         
                    # 2. Actions
                    action_parts = [p for p in parts if 'action' in p.lower() and ('-' in p or '*' in p or '•' in p)]
                    for act in action_parts:
                        clean_act = act.replace('-', '').replace('*', '').replace('•', '').strip()
                        if ':' in clean_act and 'action' in clean_act.lower().split(':')[0]:
                            clean_act = clean_act.split(':', 1)[1].strip()
                        actions.append(clean_act)

                    # --- RENDER LOGIC ---
                    
                    # 1. Bullet
                    bullet_cell = Paragraph("•", ParagraphStyle('Bullet', parent=style_normal, textColor=col_accent, fontSize=14, alignment=TA_CENTER))
                    
                    # 2. Content Stack
                    content_stack = []
                    content_stack.append(Paragraph(f"<b>{theme}</b>", ParagraphStyle('RecTitle', parent=style_normal, fontSize=10, textColor=col_text)))
                    
                    if analysis_text:
                        lbl = f"<font color='#1e293b'><b>Analysis:</b></font> <font color='#475569'>{analysis_text}</font>"
                        content_stack.append(Spacer(1, 3))
                        content_stack.append(Paragraph(lbl, ParagraphStyle('Analysis', parent=style_normal, fontSize=9, leading=12)))
                        content_stack.append(Spacer(1, 6))
                         
                    if actions:
                        for idx, action_text in enumerate(actions):
                            # Action Box: Arrow + [Label / Text]
                            label_html = f"<font color='#0f172a' size=7><b>ACTION {idx+1}</b></font>"
                            
                            act_row = [
                                Paragraph("→", ParagraphStyle('Arrow', parent=style_normal, textColor=col_primary, fontSize=10, alignment=TA_CENTER)),
                                [
                                    Paragraph(label_html, ParagraphStyle('ActLbl', parent=style_normal, spaceAfter=2)),
                                    Paragraph(action_text, ParagraphStyle('ActTxt', parent=style_normal, fontSize=9, textColor=col_subtext))
                                ]
                            ]
                            
                            act_table = Table([act_row], colWidths=[0.6*cm, 12*cm])
                            act_table.setStyle(TableStyle([
                                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
                                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                                ('TOPPADDING', (0,0), (-1,-1), 6),
                                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                                ('LEFTPADDING', (0,0), (0,0), 2),
                            ]))
                            content_stack.append(act_table)
                            content_stack.append(Spacer(1, 4))
                            
                    item_rows.append([bullet_cell, content_stack])
                    item_rows.append([None, Spacer(1, 8)]) # Separator
                
                # Wrapper Table for the whole Phase
                items_table = Table(item_rows, colWidths=[0.8*cm, 14.2*cm])
                items_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ]))
                
                card_table = Table([[items_table]], colWidths=[16*cm])
                card_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.white),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                    ('TOPPADDING', (0,0), (-1,-1), 10),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                    ('LEFTPADDING', (0,0), (-1,-1), 10),
                    ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ]))
                card_table.hAlign = 'LEFT'
                kp_phase.append(card_table)
            else:
                 kp_phase.append(Paragraph("No immediate actions for this phase.", style_normal))
            
            story.append(KeepTogether(kp_phase))
            story.append(Spacer(1, 0.6*cm))


        # --- Build PDF ---
        # Define Templates
        frame = Frame(
            doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
            id='normal', showBoundary=0
        )
        
        # We attach the header/footer function to the 'StandardParams' template
        template = PageTemplate(id='StandardParams', frames=frame, onPage=self._header_footer)
        doc.addPageTemplates([template])
        
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()
