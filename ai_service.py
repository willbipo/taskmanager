import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_simple_tasks(description):
    if not client.api_key:
        return ["Error: La API key de OpenAI no está configurada."]
    
    try:
        prompt = f"""Desglosa la siguiente tarea compleja en una lista de 3 a 5 subtareas simples y accionables.
                  
Tarea: {description}
                  
Formato de respuesta:
- Subtarea 1
- Subtarea 2
- Subtarea 3
                  
Responde solo con la lista de subtareas, una por línea, empezando cada línea con un guion."""
        
        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {"role": "developer", "content": "Eres un asistente experto en gestión de tareas."},
                {"role": "user", "content": prompt},
            ], 
            max_completion_tokens=300,
            reasoning_effort="low", 
        )

        content = response.choices[0].message.content.strip()

        subtasks = [
            line.lstrip("- ").strip() 
            for line in content.split("\n") 
            if line.strip().startswith("-")
        ]

        return subtasks if subtasks else ["Error: No se han podido generar las subtareas."]

    except Exception as e:
        return [f"Error de conexión o parámetros: {str(e)}"]