---

# 📘 User Manual: Jira Story Automator

Welcome to the **Jira Story Automator**. This guide will walk you through how to use this tool to transform your Excel backlog into structured Jira User Stories with a single command.

---

## 📋 1. Prerequisites

Before running the tool, ensure you have:

1. **Python 3.8+** installed.
2. **Atlassian API Token**: [Generate it here](https://id.atlassian.com/manage-profile/security/api-tokens).
3. **Permissions**: Ensure your Jira user has "Create Issue" and "Edit Issue" permissions in the target project.

---

## 🛠️ 2. Installation & Setup

1. **Clone the repository** (or copy the files to a local folder).
2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Configure `main.py**`:
Open the script and update the configuration section with your credentials:
* `JIRA_SERVER`: Your organization's URL (e.g., `https://company.atlassian.net`).
* `JIRA_USER`: Your login email.
* `PROJECT_KEY`: The 3-4 letter code of your project (e.g., `PROJ`).



---

## 📝 3. Preparing the Data

### Step 1: Generate the Template

Run the generator script to create the standardized Excel file:

```bash
python template_generator.py

```

### Step 2: Fill the Excel (`historias_jira.xlsx`)

Fill the columns according to these rules:

| Column | Description | Format Example |
| --- | --- | --- |
| **Summary** | The title of the Story. | *User Profile Picture Upload* |
| **Persona/Action/Value** | Used for the "As a... I want... So that..." narrative. | *User / Upload a photo / Personalize profile* |
| **Acceptance Criteria** | Requirements for the story to be done. | *Use Alt+Enter for line breaks.* |
| **Epic Key** | The ID of the parent Epic. | *PROJ-10* |
| **Sprint Name** | Name of an active or future Sprint. | *Sprint 15* |
| **Labels** | Tags for categorization. | *Mobile, UI, Backend* |

---

## 🚀 4. Running the Automation

Once your Excel is ready, execute the main script:

```bash
python main.py

```

### What happens behind the scenes?

1. **Connection**: The script connects to your Jira instance.
2. **Validation**: It checks if the Sprints and Users provided in the Excel actually exist.
3. **Creation**: It creates the Story with rich-text formatting (Bold headers, bullet points).
4. **Reporting**: A PDF report (`Reporte_Carga.pdf`) is generated with the status of every row.

---

## ⚠️ 5. Troubleshooting

* **"Field 'customfield_XXXXX' cannot be set"**: This usually means your Jira instance uses a different ID for Story Points or Sprints. Contact your Jira Admin or use the `jira.fields()` check mentioned in the documentation.
* **User Not Found**: Ensure the "Assignee Name" in Excel matches the Display Name or Email in Jira exactly.
* **SSL Errors**: If you are behind a corporate VPN, you might need to disable SSL verification or add your company's certificate to your Python environment.

---

## 📄 6. Support

For bugs or feature requests, please open an **Issue** in the GitHub repository or contact the project maintainer.

---
