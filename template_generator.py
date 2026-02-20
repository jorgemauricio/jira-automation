import pandas as pd

def generar_template():
    columns = [
        'Summary', 'Persona', 'Action', 'Value', 
        'Acceptance Criteria', 'QA Cases', 'Epic Key', 
        'Sprint Name', 'Story Points', 'Assignee Name', 'Labels'
    ]
    
    # Fila de ejemplo
    data = [{
        'Summary': 'Login con FaceID',
        'Persona': 'Usuario Premium',
        'Action': 'usar biometría',
        'Value': 'entrar más rápido',
        'Acceptance Criteria': '1. Sensor activo\n2. Feedback háptico',
        'QA Cases': '* Caso OK: Rostro reconocido',
        'Epic Key': 'PROJ-1',
        'Sprint Name': 'Sprint 1',
        'Story Points': 3,
        'Assignee Name': 'Jorge Ernesto',
        'Labels': 'Mobile, Seguridad'
    }]
    
    pd.DataFrame(data, columns=columns).to_excel('historias_jira.xlsx', index=False)
    print("✅ Archivo 'historias_jira.xlsx' creado.")

if __name__ == "__main__":
    generar_template()
