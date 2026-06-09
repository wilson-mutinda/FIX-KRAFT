
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER

# function to generate_quotation_pdf

def generate_quotation_pdf(quotation):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='RightAlign', parent=styles['Normal'], alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='CenterAlign', parent=styles['Normal'], alignment=TA_CENTER))

    flowables = []

    # HEADER
    flowables.append(Paragraph(f"Quotation #{quotation.quotation_number}", styles['Title']))
    flowables.append(Spacer(1,0.2*inch))

    # Client and Date Info
    client = quotation.inquiry.client
    client_info = [
        [Paragraph(f"<b>Client:</b> {client.name}", styles['Normal']), Paragraph(f"<b>Date:</b> {quotation.created_at.strftime('%Y-%m-%d')}", styles['RightAlign'])],
        [Paragraph(f"<b>Email:</b> {client.email}", styles['Normal']), Paragraph(f"<b>Valid Until:</b> {quotation.valid_until}", styles['RightAlign'])],
        [Paragraph(f"<b>Phone:</b> {client.phone or 'N/A'}", styles['Normal']), Paragraph(f"<b>Company:</b> {client.company or 'N/A'}", styles['RightAlign'])],
    ]
    client_table = Table(client_info, colWidths=[4*inch, 3*inch])
    client_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))

    flowables.append(client_table)
    flowables.append(Spacer(1,0.3*inch))

    # Description
    flowables.append(Paragraph("<b>Description of Work</b>", styles['Normal']))
    flowables.append(Spacer(1,0.1*inch))
    flowables.append(Paragraph(quotation.description or '-', styles['Normal']))
    flowables.append(Spacer(1,0.3*inch))

    # Line Items Table
    if quotation.line_items:
        data = [['Item', 'Amount (KSh)']]
        total = 0
        for item in quotation.line_items:
            data.append([item['service'], f"{item['price']:,.2f}"])
            total += item['price']
        data.append(['<b>Total</b>', f"<b>{total:,.2f}</b>"])

        line_table = Table(data, colWidths=[5*inch, 2*inch])
        line_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-2), 1, colors.black),
            ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ]))

        flowables.append(line_table)

    # TERMS
    flowables.append(Spacer(1,0.3*inch))
    terms = [
        "Terms & Conditions:",
        "- This quotation is valid until " + quotation.valid_until.strftime('%Y-%m-%d'),
        "- Payment is due within 14 days of acceptance",
        "- All prices are in Kenyan Shillings (KSh)",
        "- Additional work outside scope will be quoted separately",
        f"- Please reference quotation number {quotation.quotation_number} in all correspondence",
    ]
    for line in terms:
        flowables.append(Paragraph(line, styles['Normal']))
        flowables.append(Spacer(1, 0.05*inch))

    flowables.append(Spacer(1, 0.2*inch))
    flowables.append(Paragraph("Thank you for choosing FixKraft Digital.", styles['CenterAlign']))

    doc.build(flowables)
    buffer.seek(0)
    return buffer
