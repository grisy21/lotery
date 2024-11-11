import random
import time
import concurrent.futures
from casparcg.protocol import Client

# Configuración inicial
caspar_client = Client('localhost', 5250)

# Lista de nombres de loterías
lotteries = ["Lotería A", "Lotería B", "Lotería C", "Lotería D"]

# Función para generar y actualizar los resultados de una lotería
def generate_lottery_results(lottery_name, layer):
    while True:
        # Genera tres números aleatorios
        numbers = [random.randint(1, 50) for _ in range(3)]
        print(f"{lottery_name}: {numbers}")

        # Envía los resultados a CasparCG en el formato HTML o gráfico que prefieras
        caspar_client.play(layer, "template_folder/lottery_template")
        caspar_client.cg_update(layer, {
            "lottery_name": lottery_name,
            "number_1": numbers[0],
            "number_2": numbers[1],
            "number_3": numbers[2]
        })

    
        caspar_client.cg_invoke(layer, "animateIn")

        # Espera unos segundos antes de actualizar
        time.sleep(5)

# Ejecución paralela de las tareas para cada lotería
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for i, lottery_name in enumerate(lotteries):
        # Cada lotería usa una capa distinta en CasparCG
        futures.append(executor.submit(generate_lottery_results, lottery_name, i+1))
    
    # Mantiene el programa activo mientras se ejecutan los threads
    concurrent.futures.wait(futures)
