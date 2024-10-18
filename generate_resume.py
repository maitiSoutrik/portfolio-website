from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_resume():
    doc = SimpleDocTemplate("static/resume.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add custom styles
    styles.add(ParagraphStyle(name='CustomHeading1', parent=styles['Heading1'], fontSize=18, spaceAfter=12))
    styles.add(ParagraphStyle(name='CustomHeading2', parent=styles['Heading2'], fontSize=14, spaceAfter=8))
    styles.add(ParagraphStyle(name='CustomNormal', parent=styles['Normal'], fontSize=12, spaceAfter=6))

    # Add content
    story.append(Paragraph("Soutrik Maiti", styles['CustomHeading1']))
    story.append(Paragraph("Embedded Software Engineer", styles['CustomNormal']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Summary", styles['CustomHeading2']))
    story.append(Paragraph("Experienced Embedded Software Engineer with a strong background in developing firmware for various microcontrollers and embedded systems.", styles['CustomNormal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("Skills", styles['CustomHeading2']))
    skills = "C, C++, Python, Embedded Systems, RTOS, ARM, AVR, STM32, Arduino, I2C, SPI, UART, Git"
    story.append(Paragraph(skills, styles['CustomNormal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("Experience", styles['CustomHeading2']))
    experiences = [
        ("Senior Embedded Software Engineer", "TechCorp", "Jan 2020 - Present"),
        ("Embedded Software Engineer", "InnovativeSystems", "Jun 2017 - Dec 2019"),
        ("Junior Software Developer", "StartupTech", "Sep 2015 - May 2017")
    ]
    for title, company, period in experiences:
        story.append(Paragraph(f"<b>{title}</b>", styles['CustomNormal']))
        story.append(Paragraph(f"{company}, {period}", styles['CustomNormal']))
        story.append(Spacer(1, 0.05*inch))

    # Build the PDF
    doc.build(story)

if __name__ == "__main__":
    generate_resume()
