#!/usr/bin/env python3
"""
Script de verificación para IntelliAgent
Este script verifica que todas las configuraciones necesarias estén en su lugar.
"""

import os
import sys
from pathlib import Path


def check_env_file():
    """Verifica que el archivo .env exista"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        print("   Ejecuta: cp .env.example .env")
        return False
    print("✅ Archivo .env encontrado")
    return True


def check_env_variables():
    """Verifica las variables de entorno críticas"""
    required_vars = [
        "OPENAI_API_KEY",
        "API_KEY",
        "DATABASE_URL"
    ]

    optional_vars = [
        "EMAIL_ADDRESS",
        "EMAIL_PASSWORD",
        "TRELLO_API_KEY",
        "TRELLO_API_TOKEN"
    ]

    # Cargar .env si existe
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

    all_ok = True

    print("\n📋 Variables obligatorias:")
    for var in required_vars:
        value = os.environ.get(var, "")
        if not value or value.startswith("your-") or value.startswith("sk-your-"):
            print(f"   ❌ {var} - NO CONFIGURADO")
            all_ok = False
        else:
            masked = value[:10] + "..." if len(value) > 10 else "***"
            print(f"   ✅ {var} - {masked}")

    print("\n📋 Variables opcionales:")
    for var in optional_vars:
        value = os.environ.get(var, "")
        if value and not value.startswith("your-"):
            masked = value[:10] + "..." if len(value) > 10 else "***"
            print(f"   ✅ {var} - {masked}")
        else:
            print(f"   ⚠️  {var} - No configurado (opcional)")

    return all_ok


def check_docker():
    """Verifica que Docker esté instalado"""
    import subprocess
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"\n✅ Docker instalado: {result.stdout.strip()}")
            return True
        else:
            print("\n❌ Docker no está instalado correctamente")
            return False
    except FileNotFoundError:
        print("\n❌ Docker no encontrado. Instálalo desde https://www.docker.com/")
        return False


def check_docker_compose():
    """Verifica que Docker Compose esté disponible"""
    import subprocess
    try:
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Docker Compose instalado: {result.stdout.strip()}")
            return True
        else:
            # Intentar con 'docker compose' (nueva versión)
            result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ Docker Compose instalado: {result.stdout.strip()}")
                return True
            print("❌ Docker Compose no está instalado")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose no encontrado")
        return False


def check_project_structure():
    """Verifica que los directorios principales existan"""
    print("\n📁 Estructura del proyecto:")

    required_dirs = [
        "backend",
        "backend/src",
        "backend/src/api",
        "frontend",
        "frontend/src"
    ]

    required_files = [
        "compose.yaml",
        "backend/Dockerfile",
        "backend/requirements.txt",
        "frontend/Dockerfile",
        "frontend/package.json"
    ]

    all_ok = True

    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ - NO ENCONTRADO")
            all_ok = False

    for file_path in required_files:
        if Path(file_path).is_file():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - NO ENCONTRADO")
            all_ok = False

    return all_ok


def print_summary(checks):
    """Imprime un resumen de las verificaciones"""
    print("\n" + "="*60)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*60)

    total = len(checks)
    passed = sum(checks.values())

    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")

    print(f"\nResultado: {passed}/{total} verificaciones pasadas")

    if passed == total:
        print("\n🎉 ¡Todo está listo! Puedes ejecutar:")
        print("   docker-compose up --build")
    else:
        print("\n⚠️  Hay problemas que deben resolverse antes de continuar.")
        print("   Revisa los errores arriba y corrígelos.")


def main():
    """Función principal"""
    print("="*60)
    print("IntelliAgent - Verificación de Configuración")
    print("="*60)

    checks = {
        "Archivo .env": check_env_file(),
        "Variables de entorno": check_env_variables(),
        "Docker": check_docker(),
        "Docker Compose": check_docker_compose(),
        "Estructura del proyecto": check_project_structure()
    }

    print_summary(checks)

    # Salir con código de error si algo falla
    if not all(checks.values()):
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
