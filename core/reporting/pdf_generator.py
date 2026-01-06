"""
PDF report generator using ReportLab.
Creates executive-friendly AI maturity assessment reports.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from io import BytesIO
from typing import Dict, Any, List
from datetime import datetime


class PDFReportGenerator:
    """
    Generates PDF reports for AI maturity assessments.
    """
    
    def __init__(self):
        """Initialize PDF generator."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Define custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            textColor=colors.HexColor('#333333')
        ))
    
    def generate(
        self,
        assessment_data: Dict[str, Any],
        results: Dict[str, Any]
    ) -> bytes:
        """
        Generate PDF report from assessment results.
        
        Args:
            assessment_data: Assessment metadata (company_meta, etc.)
            results: Complete assessment results (scores, benchmark, recommendations)
            
        Returns:
            PDF bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Build content
        story = []
        
        # Title page
        story.extend(self._build_title_page(assessment_data))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._build_executive_summary(results))
        story.append(PageBreak())
        
        # Overall Results
        story.extend(self._build_overall_results(results))
        story.append(Spacer(1, 0.5*cm))
        
        # Dimension Scores
        story.extend(self._build_dimension_scores(results))
        story.append(PageBreak())
        
        # Benchmark Comparison
        story.extend(self._build_benchmark_section(results))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._build_recommendations(results))
        
        # Build PDF
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _build_title_page(self, assessment_data: Dict[str, Any]) -> List:
        """Build title page."""
        elements = []
        
        elements.append(Spacer(1, 3*cm))
        elements.append(Paragraph("AI-Compass", self.styles['CustomTitle']))
        elements.append(Paragraph("AI Maturity Assessment Report", self.styles['Heading2']))
        elements.append(Spacer(1, 2*cm))
        
        # Company info
        company_meta = assessment_data.get("company_meta", {})
        info_data = [
            ["Branche:", company_meta.get("industry", "N/A")],
            ["Mitarbeiter:", company_meta.get("employee_band", "N/A")],
            ["Datum:", datetime.now().strftime("%d.%m.%Y")]
        ]
        
        info_table = Table(info_data, colWidths=[5*cm, 10*cm])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(info_table)
        
        return elements
    
    def _build_executive_summary(self, results: Dict[str, Any]) -> List:
        """Build executive summary section."""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        
        recommendations = results.get("recommendations", {})
        summary = recommendations.get("executive_summary", "N/A")
        elements.append(Paragraph(summary, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.5*cm))
        
        return elements
    
    def _build_overall_results(self, results: Dict[str, Any]) -> List:
        """Build overall results section."""
        elements = []
        
        elements.append(Paragraph("Gesamtergebnis", self.styles['CustomHeading']))
        
        overall = results.get("overall", {})
        score = overall.get("score_0_100", 0)
        level = overall.get("level_1_5", 1)
        
        result_data = [
            ["Gesamtscore:", f"{score:.1f} / 100"],
            ["Reifestufe:", f"Level {level} / 5"]
        ]
        
        result_table = Table(result_data, colWidths=[6*cm, 10*cm])
        result_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 12),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(result_table)
        
        return elements
    
    def _build_dimension_scores(self, results: Dict[str, Any]) -> List:
        """Build dimension scores table."""
        elements = []
        
        elements.append(Paragraph("Reife nach Dimensionen", self.styles['CustomHeading']))
        
        dimension_scores = results.get("dimension_scores", [])
        
        # Build table data
        table_data = [["Dimension", "Score", "Level"]]
        for dim in dimension_scores:
            table_data.append([
                dim["title"],
                f"{dim['score_0_100']:.1f}",
                f"{dim['level_1_5']}"
            ])
        
        dim_table = Table(table_data, colWidths=[10*cm, 3*cm, 3*cm])
        dim_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 11),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        elements.append(dim_table)
        
        return elements
    
    def _build_benchmark_section(self, results: Dict[str, Any]) -> List:
        """Build benchmark comparison section."""
        elements = []
        
        elements.append(Paragraph("Benchmark-Vergleich", self.styles['CustomHeading']))
        
        benchmark = results.get("benchmark", {})
        cluster_label = benchmark.get("cluster_label", "N/A")
        percentile = benchmark.get("percentile", 0)
        
        bench_text = f"Ihr Unternehmen wurde dem Cluster <b>'{cluster_label}'</b> zugeordnet. "
        bench_text += f"Sie liegen im <b>{percentile:.0f}. Perzentil</b> verglichen mit synthetischen Peer-Unternehmen."
        
        elements.append(Paragraph(bench_text, self.styles['CustomBody']))
        
        if benchmark.get("mismatch_flag"):
            mismatch_note = benchmark.get("mismatch_note", "")
            elements.append(Spacer(1, 0.3*cm))
            elements.append(Paragraph(f"<i>Hinweis: {mismatch_note}</i>", self.styles['CustomBody']))
        
        return elements
    
    def _build_recommendations(self, results: Dict[str, Any]) -> List:
        """Build recommendations section."""
        elements = []
        
        recommendations = results.get("recommendations", {})
        
        # Quick Wins
        elements.append(Paragraph("Quick Wins (0–30 Tage)", self.styles['CustomHeading']))
        quick_wins = recommendations.get("quick_wins", [])
        for item in quick_wins:
            elements.append(Paragraph(f"• {item}", self.styles['CustomBody']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Roadmap
        roadmap = recommendations.get("roadmap", {})
        
        elements.append(Paragraph("Roadmap: 90 Tage", self.styles['CustomHeading']))
        for item in roadmap.get("days_90", []):
            elements.append(Paragraph(f"• {item}", self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*cm))
        
        elements.append(Paragraph("Roadmap: 6 Monate", self.styles['CustomHeading']))
        for item in roadmap.get("months_6", []):
            elements.append(Paragraph(f"• {item}", self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*cm))
        
        elements.append(Paragraph("Roadmap: 12 Monate", self.styles['CustomHeading']))
        for item in roadmap.get("months_12", []):
            elements.append(Paragraph(f"• {item}", self.styles['CustomBody']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Risks
        elements.append(Paragraph("Hauptrisiken", self.styles['CustomHeading']))
        risks = recommendations.get("risks", [])
        for item in risks:
            elements.append(Paragraph(f"• {item}", self.styles['CustomBody']))
        
        return elements
