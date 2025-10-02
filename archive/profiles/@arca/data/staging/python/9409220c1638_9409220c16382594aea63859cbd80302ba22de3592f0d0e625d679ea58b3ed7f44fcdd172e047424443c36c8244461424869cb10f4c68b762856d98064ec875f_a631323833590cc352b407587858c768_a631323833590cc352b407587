#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema centralizado de memorias replicadas en YAML y JSON
"""

import os
import yaml
import json
import fcntl
from pathlib import Path

# Rutas base
BASE_DIR = "/home/bird/alma_resist"
MEMORIAS_DIR = os.path.join(BASE_DIR, "control_central/memorias")
MEMORIAS_YAML = os.path.join(MEMORIAS_DIR, "memorias.yaml")
MEMORIAS_JSON = os.path.join(MEMORIAS_DIR, "memorias.json")

class GestorMemorias:
    def __init__(self):
        self.verificar_estructura()
        self.memorias = self.cargar()
        
    def verificar_estructura(self):
        """Asegura que los directorios y archivos existan"""
        os.makedirs(MEMORIAS_DIR, exist_ok=True)
        
        if not os.path.exists(MEMORIAS_YAML):
            with open(MEMORIAS_YAML, 'w') as f:
                yaml.dump({}, f)
                
        if not os.path.exists(MEMORIAS_JSON):
            with open(MEMORIAS_JSON, 'w') as f:
                json.dump({}, f)
    
    def cargar(self):
        """Carga las memorias desde los archivos, verificando consistencia"""
        with open(MEMORIAS_YAML, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data_yaml = yaml.safe_load(f) or {}
            fcntl.flock(f, fcntl.LOCK_UN)
            
        with open(MEMORIAS_JSON, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data_json = json.load(f) or {}
            fcntl.flock(f, fcntl.LOCK_UN)
            
        if data_yaml != data_json:
            raise ValueError("Inconsistencia entre archivos YAML y JSON de memorias")
            
        return data_yaml
    
    def guardar(self):
        """Guarda las memorias en ambos formatos atómicamente"""
        # Primero guardar en un archivo temporal
        temp_yaml = MEMORIAS_YAML + ".tmp"
        temp_json = MEMORIAS_JSON + ".tmp"
        
        with open(temp_yaml, 'w') as f:
            yaml.dump(self.memorias, f)
            
        with open(temp_json, 'w') as f:
            json.dump(self.memorias, f, indent=2)
        
        # Luego mover los temporales a los archivos reales (operación atómica)
        os.replace(temp_yaml, MEMORIAS_YAML)
        os.replace(temp_json, MEMORIAS_JSON)
    
    def actualizar(self, nuevas_memorias):
        """Actualiza las memorias con nuevos datos"""
        self.memorias.update(nuevas_memorias)
        self.guardar()
    
    def obtener(self, clave, default=None):
        """Obtiene un valor específico de las memorias"""
        return self.memorias.get(clave, default)
    
    def limpiar(self):
        """Limpia todas las memorias"""
        self.memorias = {}
        self.guardar()

# Instancia global para uso en todo el ecosistema
gestor_memorias = GestorMemorias()

# Funciones de conveniencia para compatibilidad con código existente
def cargar_memorias():
    """Carga las memorias y las devuelve (para compatibilidad)"""
    return gestor_memorias.cargar()

def guardar_memorias(data):
    """Guarda nuevas memorias (para compatibilidad)"""
    gestor_memorias.actualizar(data)

if __name__ == "__main__":
    # Ejemplo de uso
    print("Memorias actuales:", gestor_memorias.memorias)
    
    # Agregar nueva memoria
    gestor_memorias.actualizar({"ejemplo": {"valor": 123, "nota": "dato de prueba"}})
    
    # Obtener un valor
    print("Valor ejemplo:", gestor_memorias.obtener("ejemplo"))