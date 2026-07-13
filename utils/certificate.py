from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_certificate(
    name,
    company,
    role,
    ats_score,
    interview_score,
    filename="certificate.pdf"
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Interview Completion Certificate</b>", styles["Title"]))

    story.append(Paragraph(f"<br/><b>Candidate:</b> {name}", styles["Normal"]))

    story.append(Paragraph(f"<b>Company:</b> {company}", styles["Normal"]))

    story.append(Paragraph(f"<b>Role:</b> {role}", styles["Normal"]))

    story.append(Paragraph(f"<b>ATS Score:</b> {ats_score}%", styles["Normal"]))

    story.append(Paragraph(f"<b>Interview Score:</b> {interview_score:.1f}/10", styles["Normal"]))

    story.append(Paragraph("<br/>Congratulations on successfully completing the AI Mock Interview!", styles["Normal"]))

    doc.build(story)

    return filename