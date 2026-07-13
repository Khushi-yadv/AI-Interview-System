from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(questions, answers, overall_score):

    doc = SimpleDocTemplate("Interview_Report.pdf")

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Interview Report</b>", styles["Heading1"]))

    story.append(
        Paragraph(
            f"<b>Overall Score:</b> {overall_score:.1f}/10",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    for i, q in enumerate(questions):

        story.append(
            Paragraph(f"<b>Q{i+1}:</b> {q}", styles["Heading3"])
        )

        story.append(
            Paragraph(
                answers.get(i, "No Answer"),
                styles["Normal"]
            )
        )

        story.append(Paragraph("<br/>", styles["Normal"]))

    doc.build(story)

    return "Interview_Report.pdf"