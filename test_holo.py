import sys
sys.stdout.reconfigure(encoding='utf-8')
import importlib
import plantillas.holograma_3d
importlib.reload(plantillas.holograma_3d)
from plantillas.holograma_3d import generar_laboratorio_holografico_3d

try:
    result = generar_laboratorio_holografico_3d(modelo_inicial='brazo')
    print('SUCCESS, length:', len(result))
    print('First 200 chars:', result[:200])
except Exception as e:
    import traceback
    print('ERROR:', type(e).__name__, e)
    traceback.print_exc()
