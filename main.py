import pandas as pd
from jira import JIRA
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN ---
JIRA_SERVER = "https://tu-dominio.atlassian.net"
JIRA_USER = "tu-email@ejemplo.com"
JIRA_API_TOKEN = "tu_api_token"
PROJECT_KEY = "PROY"
STORY_POINTS_FIELD = 'customfield_10016'
SPRINT_FIELD = 'customfield_10020'

# --- LÓGICA DE PDF ---
class JiraReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Jira Automation Report', 0, 1, 'C')

# --- FUNCIONES ---
def get_jira_connection():
    return JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

def get_active_sprints(jira):
    sprint_map = {}
    boards = jira.boards(projectKey=PROJECT_KEY)
    if boards:
        sprints = jira.sprints(boards[0].id, state='active,future')
        for s in sprints:
            sprint_map[s.name.strip().lower()] = s.id
    return sprint_map

def run_automation():
    jira = get_jira_connection()
    df = pd.read_excel('historias_jira.xlsx')
    sprint_map = get_active_sprints(jira)
    results = []

    for _, row in df.iterrows():
        desc = (f"h2. 1. Narrative\n* *As a:* {row['Persona']}\n* *I want:* {row['Action']}\n"
                f"* *So that:* {row['Value']}\n\nh2. 2. Acceptance Criteria\n{row['Acceptance Criteria']}\n\n"
                f"h2. 3. QA Cases\n{row['QA Cases']}")
        
        issue_dict = {
            'project': PROJECT_KEY, 'summary': row['Summary'], 'description': desc, 'issuetype': 'Story'
        }

        # Validaciones de campos
        if pd.notna(row.get('Epic Key')): issue_dict['parent'] = row['Epic Key']
        if pd.notna(row.get('Labels')): 
            issue_dict['labels'] = [l.strip().replace(" ","-") for l in str(row['Labels']).split(',')]
        
        # Sprint Validation
        sn = str(row.get('Sprint Name')).lower()
        if sn in sprint_map: issue_dict[SPRINT_FIELD] = sprint_map[sn]

        try:
            new_issue = jira.create_issue(fields=issue_dict)
            results.append({'key': new_issue.key, 'summary': row['Summary'], 'status': 'Éxito'})
        except Exception as e:
            results.append({'key': 'ERROR', 'summary': row['Summary'], 'status': str(e)[:30]})

    # Generar PDF
    pdf = JiraReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    for res in results:
        pdf.cell(0, 10, f"{res['key']} - {res['summary']} [{res['status']}]", 1, 1)
    pdf.output("Reporte_Carga.pdf")
    print("🚀 Proceso terminado. Revisa Reporte_Carga.pdf")

if __name__ == "__main__":
    run_automation()
