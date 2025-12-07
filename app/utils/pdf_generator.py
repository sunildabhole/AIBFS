from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
from datetime import datetime

from app import models

def generate_invoice_pdf(order: models.Order):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(inch, height - inch, f"Invoice for Order #{order.id}")

    # Customer Info
    c.setFont("Helvetica", 12)
    c.drawString(inch, height - 1.5 * inch, "Customer Information:")
    c.drawString(1.2 * inch, height - 1.75 * inch, f"Name: {order.customer.name}")
    c.drawString(1.2 * inch, height - 2.0 * inch, f"Contact: {order.customer.contact}")

    # Order Info
    c.drawString(inch, height - 2.5 * inch, "Order Details:")
    c.drawString(1.2 * inch, height - 2.75 * inch, f"Order Date: {order.date.strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(1.2 * inch, height - 3.0 * inch, f"Total Price: ${order.total_price:.2f}")

    # Order Items
    c.drawString(inch, height - 3.5 * inch, "Order Items:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1.2 * inch, height - 3.75 * inch, "Product")
    c.drawString(3.5 * inch, height - 3.75 * inch, "Quantity")
    c.drawString(4.5 * inch, height - 3.75 * inch, "Price")
    c.setFont("Helvetica", 10)

    y = height - 4.0 * inch
    for item in order.items:
        c.drawString(1.2 * inch, y, item.product.name)
        c.drawString(3.5 * inch, y, str(item.quantity))
        c.drawString(4.5 * inch, y, f"${item.price:.2f}")
        y -= 0.25 * inch

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer


def generate_sales_report_pdf(sales_data: list, start_date: datetime, end_date: datetime):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_text = f"Sales Report from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    story.append(Paragraph(title_text, styles['h1']))
    story.append(Paragraph(" ", styles['Normal'])) # Add some space

    # Table Header
    data = [["Order ID", "Customer ID", "Total Price", "Date"]]

    # Table Data
    for sale in sales_data:
        data.append([
            str(sale.id),
            str(sale.customer_id),
            f"${sale.total_price:.2f}",
            sale.date.strftime('%Y-%m-%d %H:%M:%S')
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')), # Green header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')), # Lighter background for rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_low_stock_report_pdf(products: list):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_text = "Low Stock Report"
    story.append(Paragraph(title_text, styles['h1']))
    story.append(Paragraph(" ", styles['Normal'])) # Add some space

    # Table Header
    data = [["Product ID", "Name", "Stock"]]

    # Table Data
    for product in products:
        data.append([
            str(product.id),
            product.name,
            str(product.stock)
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F44336')), # Red header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')), # Lighter background for rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_top_selling_report_pdf(products: list):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_text = "Top Selling Products Report"
    story.append(Paragraph(title_text, styles['h1']))
    story.append(Paragraph(" ", styles['Normal'])) # Add some space

    # Table Header
    data = [["Product ID", "Name", "Total Quantity Sold"]]

    # Table Data
    for product, total_quantity in products:
        data.append([
            str(product.id),
            product.name,
            str(total_quantity)
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')), # Blue header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')), # Lighter background for rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_total_revenue_report_pdf(total_revenue: float):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_text = "Total Revenue Report"
    story.append(Paragraph(title_text, styles['h1']))
    story.append(Paragraph(" ", styles['Normal'])) # Add some space

    # Content
    content_text = f"Total Revenue: ${total_revenue:.2f}"
    story.append(Paragraph(content_text, styles['h2']))

    doc.build(story)
    buffer.seek(0)
    return buffer