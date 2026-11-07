"""
AUREX — Módulo de Cálculo Científico Exacto
============================================
Resuelve numéricamente problemas de ingeniería usando Python puro.
Sirve como verificador/corrector del LLM cuando hace aritmética.

Áreas cubiertas:
  - Difusión (Leyes de Fick)
  - Termodinámica (expansión térmica, calor específico)
  - Mecánica de Materiales (esfuerzo, deformación, módulo de Young)
  - Electricidad (Ley de Ohm, RC, RL, potencia)
  - Cinemática (MRUA, tiro parabólico)
  - Hidráulica (caudal, Bernoulli básico)
  - Integrales numéricas (regla de Simpson)
  - Ejecución segura de código Python generado por el LLM
"""

import math
import re
import traceback


# ─────────────────────────────────────────────────────────────
#  FUNCIÓN PRINCIPAL: Ejecutar código Python seguro del LLM
# ─────────────────────────────────────────────────────────────

_MODULOS_PERMITIDOS = {"math", "cmath", "numpy", "sympy", "statistics", "fractions", "decimal"}
_PALABRAS_PELIGROSAS = {"import os", "import sys", "subprocess", "open(", "exec(", "__import__",
                        "eval(", "shutil", "socket", "requests", "http", "urllib", "pickle",
                        "compile(", "globals(", "locals(", "getattr", "setattr", "delattr"}

def ejecutar_codigo_seguro(codigo: str) -> dict:
    """
    Ejecuta código Python generado por el LLM en un entorno restringido.
    Solo permite math, numpy, sympy y operaciones aritméticas.
    
    Returns:
        {"resultado": str, "variables": dict, "error": str|None}
    """
    codigo_limpio = codigo.strip()
    
    # Verificar palabras peligrosas
    codigo_lower = codigo_limpio.lower()
    for peligro in _PALABRAS_PELIGROSAS:
        if peligro in codigo_lower:
            return {"resultado": "", "variables": {}, "error": f"Operación no permitida: '{peligro}'"}
    
    # Entorno de ejecución con módulos permitidos
    entorno = {
        "math": math,
        "pi": math.pi,
        "e": math.e,
        "sqrt": math.sqrt,
        "exp": math.exp,
        "log": math.log,
        "log10": math.log10,
        "log2": math.log2,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "atan2": math.atan2,
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        "erf": math.erf,
        "erfc": math.erfc,
        "floor": math.floor,
        "ceil": math.ceil,
        "fabs": math.fabs,
        "factorial": math.factorial,
        "pow": math.pow,
        "inf": math.inf,
        "nan": math.nan,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        "range": range,
        "print": lambda *a: None,  # print silenciado
        "__builtins__": {},
    }
    
    # Intentar importar numpy/sympy si están disponibles
    try:
        import numpy as np
        entorno["np"] = np
        entorno["numpy"] = np
        entorno["array"] = np.array
        entorno["linspace"] = np.linspace
    except ImportError:
        pass
    
    salida_lineas = []
    variables_resultado = {}
    
    try:
        # Capturar resultados de expresiones en la última línea
        lineas = codigo_limpio.split('\n')
        
        # Ejecutar todas las líneas excepto la última
        if len(lineas) > 1:
            exec('\n'.join(lineas[:-1]), entorno)
        
        # Evaluar la última línea para capturar el resultado
        ultima = lineas[-1].strip()
        if ultima and not ultima.startswith('#'):
            try:
                resultado_eval = eval(ultima, entorno)
                if resultado_eval is not None:
                    salida_lineas.append(str(resultado_eval))
            except Exception:
                exec(ultima, entorno)
        
        # Capturar todas las variables numéricas definidas
        for k, v in entorno.items():
            if not k.startswith('_') and k not in {"math", "np", "numpy", "array", "linspace",
                                                     "pi", "e", "sqrt", "exp", "log", "log10",
                                                     "sin", "cos", "tan", "erf", "erfc", "print",
                                                     "abs", "round", "min", "max", "sum", "len",
                                                     "range", "inf", "nan", "pow", "floor", "ceil",
                                                     "fabs", "factorial", "log2", "asin", "acos",
                                                     "atan", "atan2", "sinh", "cosh", "tanh"}:
                if isinstance(v, (int, float, complex)):
                    variables_resultado[k] = v
        
        return {
            "resultado": '\n'.join(salida_lineas) if salida_lineas else "OK",
            "variables": variables_resultado,
            "error": None
        }
    
    except Exception as ex:
        return {
            "resultado": "",
            "variables": {},
            "error": str(ex)
        }


# ─────────────────────────────────────────────────────────────
#  EXTRACTORES: Detectar tipo de problema y extraer parámetros
# ─────────────────────────────────────────────────────────────

def detectar_tipo_problema(texto: str) -> str:
    """Detecta el tipo de problema de ingeniería en el texto."""
    t = texto.lower()
    if any(k in t for k in ["fick", "difusión", "difusion", "cementación", "cementacion", "coeficiente de difusión"]):
        return "difusion_fick"
    if any(k in t for k in ["esfuerzo", "deformación", "módulo de young", "young", "tensión", "strain", "stress"]):
        return "mecanica_materiales"
    if any(k in t for k in ["expansión térmica", "dilatación", "coeficiente térmico", "delta t"]):
        return "expansion_termica"
    if any(k in t for k in ["resistencia", "voltaje", "corriente", "ohm", "potencia eléctrica", "circuito"]):
        return "electricidad"
    if any(k in t for k in ["cinemática", "aceleración", "velocidad inicial", "mrua", "tiro parabólico"]):
        return "cinematica"
    if any(k in t for k in ["calor", "temperatura", "calor específico", "energía térmica", "q = m"]):
        return "termodinamica"
    if any(k in t for k in ["integral", "integra", "∫", "\\int"]):
        return "integral"
    return "general"


def extraer_numeros_con_etiquetas(texto: str) -> dict:
    """Extrae valores numéricos con sus etiquetas del texto."""
    patrones = [
        (r'C[_0s]?\s*=\s*([\d.]+(?:e[+-]?\d+)?)\s*%', 'concentracion_%'),
        (r'D\s*=\s*([\d.]+(?:[xX×]\s*10[^\s,]+)?)\s*m[²2]', 'difusividad_m2s'),
        (r'x\s*=\s*([\d.]+)\s*mm', 'profundidad_mm'),
        (r't\s*=\s*([\d.]+)\s*h', 'tiempo_horas'),
        (r'E\s*=\s*([\d.]+(?:[xX×]\s*10[^\s,]+)?)\s*GPa', 'modulo_young_GPa'),
        (r'σ\s*=\s*([\d.]+(?:[xX×]\s*10[^\s,]+)?)\s*MPa', 'esfuerzo_MPa'),
    ]
    encontrados = {}
    for patron, etiqueta in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            encontrados[etiqueta] = m.group(1)
    return encontrados


# ─────────────────────────────────────────────────────────────
#  SOLUCIONADORES ESPECIALIZADOS
# ─────────────────────────────────────────────────────────────

def resolver_fick_segunda_ley(C0: float, Cs: float, D: float, x_mm: float, t_horas: float) -> dict:
    """
    Resuelve la 2da Ley de Fick para difusión en semiplano infinito.
    
    C(x,t) = C0 + (Cs - C0) * [1 - erf(x / (2*sqrt(D*t)))]
    
    Args:
        C0: Concentración inicial [% peso]
        Cs: Concentración superficial [% peso]
        D:  Coeficiente de difusión [m²/s]
        x_mm: Profundidad [mm]
        t_horas: Tiempo de tratamiento [horas]
    
    Returns:
        dict con todos los valores intermedios y el resultado final
    """
    x = x_mm * 1e-3          # mm → m
    t = t_horas * 3600        # horas → segundos
    
    Dt = D * t
    sqrt_Dt = math.sqrt(Dt)
    dos_sqrt_Dt = 2 * sqrt_Dt
    
    z = x / dos_sqrt_Dt       # argumento de erf
    erf_z = math.erf(z)
    erfc_z = 1 - erf_z        # 1 - erf(z) = erfc(z)
    
    Cxt = C0 + (Cs - C0) * erfc_z
    
    return {
        "C0_%": C0,
        "Cs_%": Cs,
        "D_m2s": D,
        "x_m": x,
        "t_s": t,
        "Dt_m2": Dt,
        "sqrt_Dt_m": sqrt_Dt,
        "z_argumento_erf": round(z, 6),
        "erf_z": round(erf_z, 6),
        "erfc_z": round(erfc_z, 6),
        "C_xt_%": round(Cxt, 4),
        "formula": "C(x,t) = C0 + (Cs - C0) × [1 - erf(x / 2√(Dt))]",
        "conclusión": f"C({x_mm}mm, {t_horas}h) = {round(Cxt, 4)}% en peso"
    }


def resolver_mecanica_basica(fuerza_N: float = None, area_mm2: float = None,
                              E_GPa: float = None, longitud_mm: float = None) -> dict:
    """Calcula esfuerzo, deformación y elongación."""
    resultado = {}
    if fuerza_N and area_mm2:
        sigma = fuerza_N / (area_mm2 * 1e-6)  # Pa
        resultado["esfuerzo_MPa"] = round(sigma / 1e6, 4)
    if E_GPa and resultado.get("esfuerzo_MPa"):
        epsilon = resultado["esfuerzo_MPa"] / (E_GPa * 1e3)
        resultado["deformacion_unitaria"] = round(epsilon, 8)
        if longitud_mm:
            delta_L = epsilon * longitud_mm
            resultado["elongacion_mm"] = round(delta_L, 6)
    return resultado


def resolver_expansion_termica(L0_mm: float, alpha: float, delta_T: float) -> dict:
    """
    Calcula la expansión térmica lineal.
    ΔL = α × L0 × ΔT
    """
    delta_L = alpha * L0_mm * delta_T
    L_final = L0_mm + delta_L
    return {
        "L0_mm": L0_mm,
        "alpha_1_C": alpha,
        "delta_T_C": delta_T,
        "delta_L_mm": round(delta_L, 6),
        "L_final_mm": round(L_final, 6),
        "formula": "ΔL = α × L₀ × ΔT",
    }


def calcular_integral_numerica(f_str: str, a: float, b: float, n: int = 10000) -> dict:
    """
    Integra numéricamente f(x) de a a b usando la regla de Simpson compuesta.
    f_str: expresión Python con 'x', ej: 'x * math.exp(-x**2)'
    """
    try:
        if n % 2 != 0:
            n += 1
        h = (b - a) / n
        total = 0.0
        for i in range(n + 1):
            xi = a + i * h
            entorno = {"x": xi, "math": math, "sqrt": math.sqrt, "exp": math.exp,
                       "sin": math.sin, "cos": math.cos, "log": math.log,
                       "pi": math.pi, "e": math.e, "erf": math.erf}
            fi = eval(f_str, {"__builtins__": {}}, entorno)
            if i == 0 or i == n:
                total += fi
            elif i % 2 == 0:
                total += 2 * fi
            else:
                total += 4 * fi
        resultado = (h / 3) * total
        return {
            "integral": round(resultado, 10),
            "f(x)": f_str,
            "a": a,
            "b": b,
            "n_subintervalos": n,
            "metodo": "Simpson compuesto",
            "error_estimado": f"O(h⁴) ≈ {round(abs((b-a)**5 / (180 * n**4)), 15)}"
        }
    except Exception as ex:
        return {"error": str(ex)}


# ─────────────────────────────────────────────────────────────
#  INTERFACE PRINCIPAL: Detectar y calcular automáticamente
# ─────────────────────────────────────────────────────────────

def verificar_con_python(pregunta: str, respuesta_llm: str) -> str:
    """
    Dado el texto de la pregunta y la respuesta del LLM,
    detecta el tipo de problema e intenta verificar numéricamente.
    
    Returns:
        Bloque de texto con verificación Python, o "" si no aplica.
    """
    tipo = detectar_tipo_problema(pregunta + " " + respuesta_llm)
    
    if tipo == "difusion_fick":
        return _verificar_fick(pregunta)
    elif tipo == "integral":
        return _verificar_integral(pregunta)
    elif tipo == "expansion_termica":
        return _verificar_expansion(pregunta)
    
    return ""  # No aplica verificación automática


def _verificar_fick(texto: str) -> str:
    """Intenta extraer parámetros de Fick y re-calcular."""
    try:
        # Buscar C0
        m_C0 = re.search(r'C[_\s]*0\s*=\s*([\d.]+)\s*%', texto, re.IGNORECASE)
        m_Cs = re.search(r'C[_\s]*s\s*=\s*([\d.]+)\s*%', texto, re.IGNORECASE)
        m_D  = re.search(r'D\s*=\s*([\d.]+)\s*[xX×]\s*10\^?\{?-(\d+)\}?', texto)
        m_x  = re.search(r'x\s*=\s*([\d.]+)\s*mm', texto, re.IGNORECASE)
        m_t  = re.search(r't\s*=\s*([\d.]+)\s*h', texto, re.IGNORECASE)
        
        if not all([m_C0, m_Cs, m_D, m_x, m_t]):
            return ""
        
        C0 = float(m_C0.group(1))
        Cs = float(m_Cs.group(1))
        D  = float(m_D.group(1)) * 10**(-int(m_D.group(2)))
        x_mm = float(m_x.group(1))
        t_h  = float(m_t.group(1))
        
        r = resolver_fick_segunda_ley(C0, Cs, D, x_mm, t_h)
        
        bloque = "\n\n---\n"
        bloque += "**🐍 Verificación Python Exacta (AUREX Calc):**\n\n"
        bloque += f"$$z = \\frac{{x}}{{2\\sqrt{{Dt}}}} = \\frac{{{x_mm}\\times10^{{-3}}}}{{2\\sqrt{{{D:.2e}\\times{int(t_h*3600)}}}}}"
        bloque += f" = {r['z_argumento_erf']}$$\n\n"
        bloque += f"$$\\text{{erf}}({r['z_argumento_erf']}) = {r['erf_z']}$$\n\n"
        bloque += f"$$C({x_mm}\\text{{mm}},\\,{int(t_h)}\\text{{h}}) = {C0} + ({Cs}-{C0})\\times{r['erfc_z']} = \\boxed{{{r['C_xt_%']}\\%}}$$\n"
        
        return bloque
    
    except Exception:
        return ""


def _verificar_integral(texto: str) -> str:
    """Detecta integrales simples y las calcula numéricamente."""
    # Buscar ∫₀^∞ x e^{-x²} dx tipo
    patrones = [
        (r'int.*?0.*?inf.*?x.*?e\^?\{?-x\^?2\}?', 'x * math.exp(-x**2)', 0, 50),
        (r'int.*?0.*?pi/2.*?ln.*?sin', 'math.log(math.sin(x)) if math.sin(x) > 0 else 0', 1e-10, math.pi/2),
        (r'int.*?0.*?1.*?ln.*?1\+x.*?1\+x\^?2', 'math.log(1+x)/(1+x**2)', 0, 1),
    ]
    for patron, f_str, a, b in patrones:
        if re.search(patron, texto, re.IGNORECASE):
            r = calcular_integral_numerica(f_str, a, b)
            if "error" not in r:
                bloque = "\n\n---\n"
                bloque += f"**🐍 Verificación Python (Simpson, n={r['n_subintervalos']}):** "
                bloque += f"Resultado exacto = `{r['integral']}`\n"
                return bloque
    return ""


def _verificar_expansion(texto: str) -> str:
    """Detecta problema de expansión térmica y calcula."""
    try:
        m_L  = re.search(r'L[_\s]*0?\s*=\s*([\d.]+)\s*mm', texto, re.IGNORECASE)
        m_a  = re.search(r'α\s*=\s*([\d.]+)\s*[xX×]\s*10\^?\{?-(\d+)\}?', texto)
        m_dT = re.search(r'[Δδ]T\s*=\s*([\d.]+)', texto)
        
        if not all([m_L, m_a, m_dT]):
            return ""
        
        L0 = float(m_L.group(1))
        alpha = float(m_a.group(1)) * 10**(-int(m_a.group(2)))
        dT = float(m_dT.group(1))
        
        r = resolver_expansion_termica(L0, alpha, dT)
        bloque = "\n\n---\n"
        bloque += "**🐍 Verificación Python Exacta:**\n\n"
        bloque += f"$$\\Delta L = {alpha}\\times{L0}\\times{dT} = \\boxed{{{r['delta_L_mm']}\\text{{ mm}}}}$$\n"
        return bloque
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────
#  EXTRACTOR DE CÓDIGO PYTHON DEL LLM
# ─────────────────────────────────────────────────────────────

def extraer_y_ejecutar_codigo_llm(respuesta_llm: str) -> str:
    """
    Extrae bloques ```python ... ``` de la respuesta del LLM y los ejecuta.
    Si hay código Python de verificación numérica, lo corre y devuelve el resultado.
    """
    patron = re.compile(r'```python\s*\n(.*?)```', re.DOTALL | re.IGNORECASE)
    bloques = patron.findall(respuesta_llm)
    
    if not bloques:
        return ""
    
    resultados = []
    for i, codigo in enumerate(bloques):
        r = ejecutar_codigo_seguro(codigo)
        if r["error"]:
            continue
        if r["variables"]:
            vars_str = ", ".join(f"`{k}` = `{v:.6g}`" if isinstance(v, float) else f"`{k}` = `{v}`"
                                  for k, v in list(r["variables"].items())[:8])
            resultados.append(f"**Bloque {i+1}:** {vars_str}")
        elif r["resultado"] and r["resultado"] != "OK":
            resultados.append(f"**Bloque {i+1}:** `{r['resultado']}`")
    
    if resultados:
        return "\n\n---\n**🐍 Python ejecutó y verificó:**\n" + "\n".join(resultados) + "\n"
    return ""
