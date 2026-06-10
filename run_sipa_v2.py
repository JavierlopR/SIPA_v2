# -*- coding: utf-8 -*-
"""
SIPA v2 - Script de Arranque Rápido y Verificación
Inicia el servidor local de Streamlit e indica al usuario cómo entrar a la app.
"""

import os
import sys
import subprocess

# Forzar codificación UTF-8 para consola en Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    print("=" * 60)
    print("🧠 INICIANDO SIPA V2: BEHAVIORAL & MARKET COACH")
    print("=" * 60)
    
    # Directorio raíz del proyecto
    project_root = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(project_root, "src", "app.py")
    
    # Verificar si el archivo app.py existe
    if not os.path.exists(app_path):
        print(f"❌ Error: No se encontró app.py en {app_path}")
        sys.exit(1)
        
    print("📦 Verificando dependencias instaladas...")
    try:
        import streamlit
        import sklearn
        import joblib
        import plotly
        import yfinance
        print("✅ Todas las dependencias (Streamlit, Scikit-Learn, Joblib, Plotly, yfinance) están listas.")
    except ImportError as e:
        print(f"❌ Falta alguna dependencia: {str(e)}")
        print("💡 Sugerencia: Ejecuta 'pip install -r requirements.txt' antes de arrancar.")
        sys.exit(1)
        
    print("\n🚀 Iniciando el Dashboard de Streamlit en tu navegador...")
    print("👉 Si tu navegador no se abre automáticamente, entra a: http://localhost:8501")
    print("=" * 60)
    
    try:
        # Ejecutar 'streamlit run src/app.py' en el directorio correcto
        # shell=True es requerido en Windows para resolver comandos de scripts como streamlit
        subprocess.run(["streamlit", "run", "src/app.py"], cwd=project_root, check=True, shell=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor SIPA v2 detenido por el usuario. ¡Hasta pronto!")
    except Exception as e:
        print(f"\n❌ Error al arrancar Streamlit: {str(e)}")

if __name__ == "__main__":
    main()
