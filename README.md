# jira-automation
---

# 🚀 Jira Story Automator

A professional Python-based automation tool to bulk-create structured **Jira User Stories** from Excel files. Designed for Product Managers and Data Scientists who need to maintain a high-quality backlog with speed and precision.

## ✨ Key Features

- **Automated Formatting:** Automatically builds descriptions using the "As a / I want / So that" narrative, plus Acceptance Criteria and QA Cases sections.
- **Sprint & Epic Integration:** Validates and assigns stories to active Sprints and parent Epics.
- **Smart Assignment:** Searches for the correct `accountId` using names or emails.
- **Data Validation:** Cleans labels (removes spaces, handles commas) and validates story points.
- **PDF Reporting:** Generates a professional summary report of the creation process for stakeholders.

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/jorgemauricio/jira-automation.git](https://github.com/jorgemauricio/jira-automation.git)
   cd jira-story-automator



2. **Install dependencies:**
```bash
pip install -r requirements.txt

```

3. **Configure your credentials:**
Open `main.py` and update the following variables:
* `JIRA_SERVER`: `https://your-domain.atlassian.net`
* `JIRA_USER`: `your-email@company.com`
* `JIRA_API_TOKEN`: Your Atlassian API Token.

---

## 🚀 Usage Workflow

### 1. Generate the Template

Run the generator to create the standard Excel file:

```bash
python template_generator.py

```

### 2. Fill the Backlog

Open `historias_jira.xlsx` and fill in your stories.
*Tip: Use `Alt + Enter` for line breaks within cells for Acceptance Criteria.*

### 3. Run the Automation

Upload everything to Jira and get your report:

```bash
python main.py

```

---

## 📂 Project Structure

* `main.py`: Core logic for Jira connection, data processing, and PDF generation.
* `template_generator.py`: Utility to create the Excel file with the correct headers.
* `requirements.txt`: Project dependencies.
* `.gitignore`: Ensures your tokens and local data stay private.
* `Reporte_Carga_Jira.pdf`: Summary generated after each run.

---

## 📋 Excel Schema

| Column | Description |
| --- | --- |
| **Summary** | Ticket title. |
| **Persona / Action / Value** | Narrative components. |
| **Acceptance Criteria** | Requirements for the "Definition of Done". |
| **QA Cases** | Specific testing scenarios. |
| **Epic Key** | Parent Epic ID (e.g., PROJ-123). |
| **Sprint Name** | Exact name of the target Sprint. |
| **Story Points** | Numerical complexity value. |
| **Assignee Name** | Full name or email of the owner. |
| **Labels** | Comma-separated tags. |

---

## 🛡️ Security

This project uses a `.gitignore` file to prevent sensitive data (like your `API_TOKEN` or Excel files) from being pushed to public repositories. Always handle your tokens with care.

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

```

