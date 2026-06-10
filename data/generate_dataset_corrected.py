import pandas as pd
import random
from typing import List, Dict
import numpy as np

class DatasetGenerator:
    def __init__(self):
        self.intenciones = ['consultar_cartera', 'quiero_comprar', 'quiero_vender', 'explicar_concepto', 'pedir_recomendacion']
        self.sesgos = ['ninguno', 'panico', 'fomo', 'overconfidence', 'loss_aversion', 'anchoring']
        
        # Ejemplos base para cada intención
        self.ejemplos_base = {
            'consultar_cartera': [
                "¿cuánto vale mi cartera?", "¿cómo van mis acciones?", "quiero ver mi rendimiento",
                "¿cuál es el valor actual de mi portafolio?", "¿cuánto he ganado/perdido?", "muéstrame mis inversiones",
                "¿qué tal está mi portfolio?", "necesito ver el estado de mis activos", "¿cuánto dinero tengo invertido?",
                "dime el valor de mis acciones", "¿cómo está funcionando mi inversión?", "quiero revisar mi cartera",
                "¿cuál es mi patrimonio actual?", "muéstrame el rendimiento de mis fondos", "¿cómo van mis posiciones?",
                "necesito un resumen de mi cartera", "¿cuál es el valor total de mis activos?", "quiero saber cómo va mi dinero",
                "¿cuánto vale todo lo que tengo invertido?", "dime el estado de mis inversiones", "¿qué rendimiento tengo?"
            ],
            'quiero_comprar': [
                "¿debería meter dinero en NVDA?", "quiero invertir en tech", "estoy pensando en comprar acciones",
                "¿qué tal si compro Tesla?", "me gustaría invertir en criptomonedas", "¿es buen momento para comprar Apple?",
                "quiero entrar en el mercado", "¿dónde puedo invertir mi dinero?", "estoy considerando comprar ETFs",
                "¿qué me recomiendan comprar?", "quiero añadir más acciones a mi cartera", "¿es buena idea comprar ahora?",
                "estoy buscando oportunidades de inversión", "¿debería comprar más de esta acción?", "quiero diversificar mi portafolio",
                "¿qué acción recomiendan comprar?", "estoy pensando en invertir en biotecnología", "quiero comprar mi primera acción"
            ],
            'quiero_vender': [
                "quiero salirme de Apple", "voy a vender todo", "necesito vender mis acciones",
                "¿debería vender Tesla ahora?", "estoy pensando en liquidar mi cartera", "quiero vender mis posiciones",
                "¿es buen momento para vender?", "voy a salir del mercado", "necesito liquidez, quiero vender",
                "estoy considerando vender mis ganancias", "quiero vender mis pérdidas", "¿debería vender todo ahora?",
                "voy a reducir mi exposición", "quiero vender algunas acciones", "necesito vender para comprar otra cosa",
                "¿es buena idea vender ahora?", "estoy pensando en vender mis tech stocks", "quiero liquidar todo"
            ],
            'explicar_concepto': [
                "¿qué es el RSI?", "explícame qué es diversificación", "¿qué significa P/E ratio?",
                "¿cómo funciona el mercado de valores?", "¿qué es un ETF?", "explícame qué es una acción",
                "¿qué es la volatilidad?", "¿cómo se calcula el rendimiento?", "¿qué es el beta?",
                "explícame qué es un fondo mutuo", "¿qué significa diversificar?", "¿cómo funciona el interés compuesto?",
                "¿qué es el riesgo en inversiones?", "explícame qué es un bono", "¿qué es la capitalización bursátil?",
                "¿cómo funciona el trading?", "¿qué es un índice bursátil?", "explícame qué es el dividendo"
            ],
            'pedir_recomendacion': [
                "¿qué me recomiendas?", "¿dónde invierto?", "¿en qué debería poner mi dinero?",
                "¿qué acción me recomiendan comprar?", "¿dónde puedo invertir para ganar dinero?", "¿me pueden dar una recomendación?",
                "¿qué es buena inversión ahora?", "¿dónde me conviene invertir?", "¿qué me sugieren hacer con mi dinero?",
                "¿cuál es la mejor inversión?", "¿dónde debería poner mis ahorros?", "¿qué me recomiendan para principiantes?",
                "¿en qué sector debo invertir?", "¿dónde me recomiendan invertir a largo plazo?", "¿qué acción es buena compra?",
                "¿qué me dicen de invertir en crypto?", "¿dónde puedo obtener buenos rendimientos?", "¿qué recomiendan para mi cartera?"
            ]
        }
        
        # Ejemplos de sesgos obvios y sutiles
        self.ejemplos_sesgos = {
            'panico': {
                'obvio': [
                    "¡VENDO TODO! Esto se hunde", "¡esto es un desastre!", "no puedo más con estas pérdidas",
                    "¡estoy arruinado!", "el mercado se viene abajo", "tengo que salir antes de que sea peor",
                    "¡no puedo creer que esté perdiendo tanto!", "esto es una masacre", "voy a liquidar todo",
                    "¡estoy quebrando!", "no puedo aguantar más", "el mercado está colapsando"
                ],
                'sutil': [
                    "No sé, igual debería reducir un poco mi exposición antes de que pase algo",
                    "Quizás debería tomar algunas ganancias antes de que cambie el mercado",
                    "Tal vez sea prudente salirme de algunas posiciones volátiles",
                    "Estoy un poco preocupado por la volatilidad reciente",
                    "Quizás debería ser más conservador por un tiempo",
                    "No estoy seguro de mantener estas posiciones en este entorno",
                    "Tal vez deba reconsiderar mi exposición al riesgo",
                    "Estoy pensando en reducir mi riesgo un poco",
                    "Quizás sea bueno tener más efectivo disponible",
                    "No estoy muy cómodo con el nivel de riesgo actual"
                ]
            },
            'fomo': {
                'obvio': [
                    "¡Todos están ganando menos yo!", "¡voy a perderme la subida!", "todos mis amigos están ricos con Bitcoin",
                    "¡estoy perdiendo la oportunidad de mi vida!", "todo el mundo está ganando menos yo", "no quiero ser el único que no gana",
                    "¡la subida va a continuar sin mí!", "todos están entrando al mercado", "no puedo quedarme fuera",
                    "¡voy a arrepentirme si no entro ahora!", "todo el mundo está haciendo dinero fácil", "no puedo ser el tonto que no invierte"
                ],
                'sutil': [
                    "He visto que mucha gente está entrando en crypto, quizás debería echarle un ojo",
                    "Varios colegas han tenido buenos resultados con acciones de tecnología",
                    "He oído que el sector de energía está teniendo un buen momento",
                    "Mucha gente está hablando bien de las inversiones en IA",
                    "Varios expertos mencionan que las commodities están subiendo",
                    "He notado que muchos inversores están entrando a mercados emergentes",
                    "Varios amigos me han dicho que han ganado con ETFs",
                    "He leído que el sector inmobiliario está en alza",
                    "Mucha gente está optimista sobre las acciones de crecimiento",
                    "He visto que varios fondos están invirtiendo en sostenibilidad"
                ]
            },
            'overconfidence': {
                'obvio': [
                    "yo sé que esta acción va a subir seguro", "nunca me equivoco", "tengo un sexto sentido para las inversiones",
                    "esto es obvio, va a explotar", "mi intuición nunca falla", "soy un genio del mercado",
                    "esto es dinero fácil", "nadie conoce este mercado como yo", "voy a ser millonario con esto",
                    "es matemático, tiene que subir", "soy el mejor inversor", "esto es una ganga obvia"
                ],
                'sutil': [
                    "Tengo una buena sensación sobre esta inversión",
                    "Mi análisis me dice que esta acción tiene potencial",
                    "Estoy bastante seguro de que esta es una buena oportunidad",
                    "Basado en mi investigación, creo que va a funcionar bien",
                    "Mi experiencia me dice que este es el momento adecuado",
                    "He estudiado este sector y creo que hay oportunidades",
                    "Mi análisis fundamental me da señales positivas",
                    "Estoy confiado en mi estrategia de inversión",
                    "Basado en mis conocimientos, creo que es una buena decisión",
                    "Mi investigación me indica que hay upside potencial"
                ]
            },
            'loss_aversion': {
                'obvio': [
                    "no quiero vender con pérdidas", "prefiero esperar a que suba", "me duele demasiado vender ahora",
                    "no puedo vender por debajo de mi precio de compra", "voy a esperar a que recupere", "no voy a realizar esta pérdida",
                    "mejor espero a que vuelva a subir", "no vendo con pérdidas nunca", "prefiero mantenerlo a vender perdiendo"
                ],
                'sutil': [
                    "Prefiero esperar un poco antes de decidir sobre esta posición",
                    "No me conviene vender en este momento, mejor espero",
                    "Tal vez debería mantener esta posición un poco más",
                    "No estoy seguro de vender ahora, quizás es mejor esperar",
                    "Prefiero no tomar decisiones precipitadas con esta inversión",
                    "Mejor darle tiempo a que se recupere antes de actuar",
                    "No creo que sea el mejor momento para vender esta posición",
                    "Prefiero mantener mi estrategia actual por ahora",
                    "No me parece prudente vender en estas condiciones",
                    "Mejor esperar a ver cómo evoluciona la situación"
                ]
            },
            'anchoring': {
                'obvio': [
                    "la compré a 200, no vendo por debajo de eso", "compré a 50, tengo que esperar a que vuelva a 50",
                    "mi precio de compra fue 100, no vendo por menos", "compré a 150, necesito que vuelva a ese nivel",
                    "la compré a 30, mi punto de equilibrio es 30", "compré a 80, no puedo vender por debajo"
                ],
                'sutil': [
                    "A este precio no me convence, cuando vuelva al nivel donde compré ya vemos",
                    "No me parece justo vender a este nivel, prefiero esperar",
                    "Este precio está por debajo de lo que esperaba, mejor espero",
                    "No me gusta vender a este nivel, prefiero mantener",
                    "A este precio no estoy cómodo, prefiero esperar una mejora",
                    "No me parece un buen precio de salida, mejor aguardo",
                    "Este nivel no me parece adecuado para vender, prefiero esperar",
                    "No estoy convencido de vender a este precio, mejor mantengo",
                    "A este nivel no me siento cómodo vendiendo, prefiero esperar",
                    "No me parece el momento adecuado para vender a este precio"
                ]
            }
        }
    
    def generar_dataset_balanceado(self) -> pd.DataFrame:
        """Generar dataset balanceado con 150 ejemplos por intención y 120 por sesgo"""
        dataset = []
        
        # Para cada intención, generar 150 ejemplos con diferentes sesgos
        for intencion in self.intenciones:
            ejemplos_intencion = []
            
            # Generar combinaciones con sesgos (5-10 ejemplos por combinación)
            for sesgo in self.sesgos:
                num_ejemplos = random.randint(5, 10)
                
                for _ in range(num_ejemplos):
                    if sesgo == 'ninguno':
                        # Ejemplos neutros
                        texto = random.choice(self.ejemplos_base[intencion])
                        texto = self.variar_texto(texto)
                    else:
                        # Ejemplos con sesgo
                        texto = self.generar_ejemplo_con_sesgo(intencion, sesgo)
                    
                    ejemplos_intencion.append({
                        'texto': texto,
                        'intencion': intencion,
                        'sesgo': sesgo
                    })
            
            # Completar hasta 150 ejemplos por intención
            while len(ejemplos_intencion) < 150:
                sesgo_random = random.choice(self.sesgos)
                
                if sesgo_random == 'ninguno':
                    texto = random.choice(self.ejemplos_base[intencion])
                    texto = self.variar_texto(texto)
                else:
                    texto = self.generar_ejemplo_con_sesgo(intencion, sesgo_random)
                
                ejemplos_intencion.append({
                    'texto': texto,
                    'intencion': intencion,
                    'sesgo': sesgo_random
                })
            
            # Tomar solo 150 ejemplos
            dataset.extend(ejemplos_intencion[:150])
        
        # Mezclar dataset
        random.shuffle(dataset)
        
        # Crear DataFrame y verificar balance
        df = pd.DataFrame(dataset)
        
        # Ajustar para tener exactamente 120 por sesgo
        df_final = pd.DataFrame()
        for sesgo in self.sesgos:
            df_sesgo = df[df['sesgo'] == sesgo].head(120)
            df_final = pd.concat([df_final, df_sesgo], ignore_index=True)
        
        return df_final
    
    def generar_ejemplo_con_sesgo(self, intencion: str, sesgo: str) -> str:
        """Generar ejemplo combinando intención y sesgo"""
        base = random.choice(self.ejemplos_base[intencion])
        
        if sesgo in self.ejemplos_sesgos:
            # 50% obvio, 50% sutil
            tipo = random.choice(['obvio', 'sutil'])
            sesgo_ejemplo = random.choice(self.ejemplos_sesgos[sesgo][tipo])
            
            # Combinar base con sesgo
            if intencion == 'quiero_comprar':
                if sesgo == 'fomo':
                    return f"{sesgo_ejemplo}, quiero comprar {random.choice(['NVDA', 'Tesla', 'Apple', 'crypto'])}"
                elif sesgo == 'overconfidence':
                    return f"{sesgo_ejemplo}, voy a comprar {random.choice(['esta acción', 'este ETF', 'este crypto'])}"
                elif sesgo == 'loss_aversion':
                    return f"{base}, pero {sesgo_ejemplo.lower()}"
                elif sesgo == 'anchoring':
                    return f"{sesgo_ejemplo}, por eso no quiero comprar ahora"
                elif sesgo == 'panico':
                    return f"{sesgo_ejemplo}, no quiero comprar nada"
            
            elif intencion == 'quiero_vender':
                if sesgo == 'panico':
                    return f"{sesgo_ejemplo}, voy a vender todo ya"
                elif sesgo == 'loss_aversion':
                    return f"{sesgo_ejemplo}, no puedo vender"
                elif sesgo == 'anchoring':
                    return f"{sesgo_ejemplo}, no vendo por debajo"
                elif sesgo == 'fomo':
                    return f"{sesgo_ejemplo}, pero igual vendo para comprar otra cosa"
                elif sesgo == 'overconfidence':
                    return f"{sesgo_ejemplo}, sé cuándo vender"
            
            elif intencion == 'consultar_cartera':
                if sesgo == 'loss_aversion':
                    return f"¿Cuánto he perdido? {sesgo_ejemplo.lower()}"
                elif sesgo == 'panico':
                    return f"¿Cuánto he perdido? {sesgo_ejemplo.lower()}"
                elif sesgo == 'fomo':
                    return f"¿Cuánto he ganado? {sesgo_ejemplo.lower()}"
                elif sesgo == 'overconfidence':
                    return f"¿Cuánto he ganado? {sesgo_ejemplo.lower()}"
                elif sesgo == 'anchoring':
                    return f"¿Cuánto vale comparado con mi precio de compra? {sesgo_ejemplo.lower()}"
            
            elif intencion == 'explicar_concepto':
                if sesgo == 'overconfidence':
                    return f"{base}, {sesgo_ejemplo.lower()}"
                else:
                    return f"{base}, {sesgo_ejemplo.lower()}"
            
            elif intencion == 'pedir_recomendacion':
                return f"{base}, {sesgo_ejemplo.lower()}"
        
        return base
    
    def variar_texto(self, texto: str) -> str:
        """Variar el texto para hacerlo más diverso"""
        variaciones = [
            texto,
            texto.lower(),
            texto.upper(),
            texto.replace("¿", ""),
            texto + "!",
            texto + " por favor",
            "oye " + texto,
            texto + " urgente",
            texto.replace("quiero", "necesito"),
            texto.replace("¿", "disculpa, ¿")
        ]
        
        texto_variado = random.choice(variaciones)
        
        # Agregar errores ortográficos aleatorios
        if random.random() < 0.1:
            texto_variado = self.agregar_errores_ortograficos(texto_variado)
        
        return texto_variado
    
    def agregar_errores_ortograficos(self, texto: str) -> str:
        """Agregar errores ortográficos comunes"""
        errores = {
            'h': '',
            'que': 'ke',
            'quiero': 'kiero',
            'por': 'po',
            'para': 'pa',
            'también': 'tambien',
            'más': 'mas',
            'sí': 'si',
            'estoy': 'toy',
            'voy': 'boi',
            'está': 'ta',
            'con': 'kon'
        }
        
        for correcto, error in errores.items():
            if random.random() < 0.3:
                texto = texto.replace(correcto, error)
        
        return texto
    
    def mostrar_distribucion(self, df: pd.DataFrame):
        """Mostrar tabla cruzada intención × sesgo"""
        print("\n=== DISTRIBUCIÓN CRUZADA INTENCIÓN × SESGO ===")
        tabla_cruzada = pd.crosstab(df['intencion'], df['sesgo'], margins=True)
        print(tabla_cruzada)
        
        print("\n=== DISTRIBUCIÓN POR INTENCIÓN ===")
        print(df['intencion'].value_counts())
        
        print("\n=== DISTRIBUCIÓN POR SESGO ===")
        print(df['sesgo'].value_counts())
        
        print(f"\n=== TOTAL DE EJEMPLOS ===")
        print(f"Total: {len(df)}")
    
    def guardar_dataset(self, df: pd.DataFrame, ruta: str):
        """Guardar dataset verificado"""
        # Verificar formato
        assert all(col in df.columns for col in ['texto', 'intencion', 'sesgo']), "Faltan columnas requeridas"
        assert df['texto'].notna().all(), "Hay textos vacíos"
        assert df['intencion'].notna().all(), "Hay intenciones vacías"
        assert df['sesgo'].notna().all(), "Hay sesgos vacíos"
        
        # Verificar categorías
        assert set(df['intencion'].unique()) == set(self.intenciones), "Hay categorías de intención incorrectas"
        assert set(df['sesgo'].unique()) == set(self.sesgos), "Hay categorías de sesgo incorrectas"
        
        df.to_csv(ruta, index=False, encoding='utf-8')
        print(f"Dataset guardado en: {ruta}")
        self.mostrar_distribucion(df)

if __name__ == "__main__":
    import os
    generator = DatasetGenerator()
    df = generator.generar_dataset_balanceado()
    
    # Resolver la ruta de forma dinámica e independiente del directorio de trabajo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "datasets", "bias_intent_dataset_corrected.csv")
    
    # Crear el directorio datasets si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    generator.guardar_dataset(df, output_path)
