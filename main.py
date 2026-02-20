import pandas as pd
from jira import JIRA
from fpdf import FPDF
from datetime import datetime
import sys
import os

# --- CONFIGURACIÓN ---
JIRA_SERVER = "https://tu-dominio.atlassian.net"
JIRA_USER = "tu-email@ejemplo.com"
JIRA_API_TOKEN = "tu_api_token"
PROJECT_KEY = "PROY"
STORY_POINTS_FIELD = 'customfield_10016'
SPRINT_FIELD = 'customfield_10020'
FILE_PATH = 'historias_jira.xlsx'

# --- CLASE PARA EL REPORTE PDF ---
class JiraReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Jira Automation Report - Execution Summary', 0, 1, 'C')
        self.ln(5)

# --- VALIDACIÓN AUTOMÁTICA (UNIT TEST INTEGRADO) ---
def validate_excel_integrity(file_path):
    print("🔍 Validating Excel integrity...")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found.")
        return False

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"❌ Error: Could not read Excel file. {e}")
        return False

    required_columns = [
        'Summary', 'Persona', 'Action', 'Value', 
        'Acceptance Criteria', 'QA Cases', 'Epic Key', 
        'Sprint Name', 'Story Points', 'Assignee Name', 'Labels'
    ]
    
    # 1. Verificar nombres de columnas
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"❌ Error: Missing columns in Excel: {missing_cols}")
        return False

    # 2. Verificar que haya al menos una historia
    if df.empty:
        print("❌ Error: The Excel file is empty.")
        return False

    # 3. Verificar que todos los 'Summary' tengan valor
    if df['Summary'].isnull().any():
        print("❌ Error: Some rows are missing the 'Summary' (Title).")
        return False

    print("✅ Validation successful. Proceeding to Jira upload...\n")
    return True

# --- FUNCIONES DE JIRA ---
def get_active_sprints(jira):
    sprint_map = {}
    try:
        boards = jira.boards(projectKey=PROJECT_KEY)
        if boards:
            sprints = jira.sprints(boards[0].id, state='active,future')
            for s in sprints:
                sprint_map[s.name.strip().lower()] = s.id
    except: pass
    return sprint_map

def get_assignee_id(jira, name_query):
    if not name_query or pd.isna(name_query): return None
    users = jira.search_users(query=str(name_query))
    return users[0].accountId if users else None

# --- PROCESO PRINCIPAL ---
def run_automation():
    # Paso 0: Validar Excel antes de conectar
    if not validate_excel_integrity(FILE_PATH):
        print("🛑 Automation stopped due to validation errors.")
        sys.exit(1)

    # Paso 1: Conexión
    try:
        jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        sys.exit(1)

    df = pd.read_excel(FILE_PATH)
    sprint_map = get_active_sprints(jira)
    results = []

    # Paso 2: Procesamiento
    for index, row in df.iterrows():
        description_text = (
            "h2. 1. Narrative\n"
            f"* *As a:* {row['Persona']}\n"
            f"* *I want:* {row['Action']}\n"
            f"* *So that:* {row['Value']}\n\n"
            "h2. 2. Acceptance Criteria\n"
            f"{row['Acceptance Criteria']}\n\n"
            "h2. 3. QA Cases\n"
            f"{row['QA Cases']}"
        )

        issue_dict = {
            'project': PROJECT_KEY,
            'summary': row['Summary'],
            'description': description_text,
            'issuetype': {'name': 'Story'},
        }

        # Campos Opcionales
        if pd.notna(row.get('Epic Key')): issue_dict['parent'] = {'key': row['Epic Key']}
        if pd.notna(row.get('Story Points')): issue_dict[STORY_POINTS_FIELD] = float(row['Story Points'])
        if pd.notna(row.get('Labels')):
            issue_dict['labels'] = [l.strip().replace(" ", "-") for l in str(row['Labels']).split(',')]

        # Validación de Sprint y Assignee
        sprint_name = str(row.get('Sprint Name')).strip().lower()
        if sprint_name in sprint_map:
            issue_dict[SPRINT_FIELD] = sprint_map[sprint_name]

        assignee_id = get_assignee_id(jira, row.get('Assignee Name'))
        if assignee_id:
            issue_dict['assignee'] = {'accountId': assignee_id}

        try:
            new_issue = jira.create_issue(fields=issue_dict)
            results.append({'key': new_issue.key, 'summary': row['Summary'], 'status': 'Success ✅'})
            print(f"✔️ Created: {new_issue.key}")
        except Exception as e:
            results.append({'key': 'FAILED', 'summary': row['Summary'], 'status': f"Error: {str(e)[:40]}"})
            print(f"⚠️ Failed: {row['Summary']}")

    # Paso 3: Generación de Reporte PDF
    pdf = JiraReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
    pdf.ln(5)

    for res in results:
        pdf.multi_cell(0, 10, f"[{res['status']}] {res['key']} - {res['summary']}", 1)

    pdf.output("Reporte_Carga.pdf")
    print(f"\n🚀 Done! Report generated: Reporte_Carga.pdf")

if __name__ == "__main__":
    run_automation()
