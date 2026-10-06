from models import CAMPOS_ESTUDIANTE

from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)

from views import (
    crear_estudiante,
    obtener_todos,
    obtener_por_id,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    agregar_nota,
    materias_ofertadas,
    estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):

    print(
        f"{'ID':<5}"
        f"{'NOMBRE':<25}"
        f"{'CARNET':<15}"
        f"{'EMAIL':<30}"
        f"{'PROMEDIO':<10}"
    )

    print("-" * 85)

    for estudiante in estudiantes:

        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.carnet:<15}"
            f"{estudiante.email:<30}"
            f"{estudiante.obtener_promedio():<10}"
        )

    print("-" * 85)

    imprimir_info(
        f"Total: {len(estudiantes)} estudiante(s)"
    )


def opcion_crear():

    imprimir_titulo(
        "CREAR NUEVO ESTUDIANTE"
    )

    datos = {}

    for campo in CAMPOS_ESTUDIANTE:

        datos[campo] = input(
            f"{campo.capitalize()}: "
        )

    exito, mensaje = crear_estudiante(
        datos
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


def opcion_ver_todos():

    imprimir_titulo(
        "LISTA DE ESTUDIANTES"
    )

    estudiantes = obtener_todos()

    if not estudiantes:

        imprimir_info(
            "Todavía no hay estudiantes."
        )

    else:

        mostrar_tabla(
            estudiantes
        )

    pausa()


def opcion_buscar():

    imprimir_titulo(
        "BUSCAR ESTUDIANTE"
    )

    termino = input(
        "Nombre, apellido, email o carnet: "
    )

    encontrados = buscar_estudiantes(
        termino
    )

    if not encontrados:

        imprimir_info(
            f"Ningún estudiante coincide "
            f"con '{termino}'."
        )

    else:

        mostrar_tabla(
            encontrados
        )

    pausa()


def opcion_ver_por_id():

    imprimir_titulo(
        "VER ESTUDIANTE POR ID"
    )

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    estudiante = obtener_por_id(
        id_estudiante
    )

    if not estudiante:

        imprimir_error(
            f"No existe un estudiante "
            f"con id {id_estudiante}"
        )

    else:

        print(
            f"ID: {estudiante.id}"
        )

        print(
            f"Nombre: "
            f"{estudiante.obtener_nombre_completo()}"
        )

        print(
            f"Email: "
            f"{estudiante.email}"
        )

        print(
            f"Carnet: "
            f"{estudiante.carnet}"
        )

        print(
            f"Promedio: "
            f"{estudiante.obtener_promedio()}"
        )

        print(
            f"Materias: "
            f"{', '.join(sorted(estudiante.materias))}"
        )

        print(
            f"Notas: "
            f"{estudiante.notas}"
        )

    pausa()


def opcion_actualizar():

    imprimir_titulo(
        "ACTUALIZAR ESTUDIANTE"
    )

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    estudiante = obtener_por_id(
        id_estudiante
    )

    if not estudiante:

        imprimir_error(
            f"No existe un estudiante "
            f"con id {id_estudiante}"
        )

        return pausa()

    imprimir_info(
        f"Editando a "
        f"{estudiante.obtener_nombre_completo()}"
    )

    print(
        "Deje vacío el campo que "
        "no quiera cambiar.\n"
    )

    cambios = {}

    for campo in CAMPOS_ESTUDIANTE:

        actual = getattr(
            estudiante,
            campo
        )

        nuevo = input(
            f"{campo.capitalize()} "
            f"[{actual}]: "
        ).strip()

        if nuevo:

            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(
        id_estudiante,
        cambios
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


def opcion_eliminar():

    imprimir_titulo(
        "ELIMINAR ESTUDIANTE"
    )

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    estudiante = obtener_por_id(
        id_estudiante
    )

    if not estudiante:

        imprimir_error(
            f"No existe un estudiante "
            f"con id {id_estudiante}"
        )

        return pausa()

    imprimir_info(
        f"Se eliminará: {estudiante}"
    )

    if confirmar(
        "¿Confirma la eliminación?"
    ):

        exito, mensaje = eliminar_estudiante(
            id_estudiante
        )

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    else:

        imprimir_info(
            "Operación cancelada"
        )

    pausa()


def opcion_agregar_nota():

    imprimir_titulo(
        "AGREGAR NOTA"
    )

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

        nota = float(
            input("Nota (0-20): ")
        )

    except ValueError:

        imprimir_error(
            "El id y la nota deben "
            "ser números"
        )

        return pausa()

    materia = input(
        "Materia: "
    ).strip()

    if not materia:

        imprimir_error(
            "Debe ingresar una materia"
        )

        return pausa()

    exito, mensaje = agregar_nota(
        id_estudiante,
        materia,
        nota
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# =========================================================
# VER PROMEDIO
# =========================================================

def opcion_ver_promedio():

    imprimir_titulo(
        "PROMEDIO DEL ESTUDIANTE"
    )

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    estudiante = obtener_por_id(
        id_estudiante
    )

    if not estudiante:

        imprimir_error(
            f"No existe el estudiante "
            f"con id {id_estudiante}"
        )

    else:

        print(
            f"\nEstudiante: "
            f"{estudiante.obtener_nombre_completo()}"
        )

        print(
            f"Promedio: "
            f"{estudiante.obtener_promedio()}"
        )

    pausa()


def opcion_materias_comun():

    imprimir_titulo(
        "MATERIAS EN COMÚN"
    )

    try:

        id_a = int(
            input("Id del primer estudiante: ")
        )

        id_b = int(
            input("Id del segundo estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "Los IDs deben ser números enteros"
        )

        return pausa()

    exito, resultado = estudiantes_en_comun(
        id_a,
        id_b
    )

    if not exito:

        imprimir_error(
            resultado
        )

    elif resultado:

        imprimir_info(
            "Materias en común: "
            + ", ".join(
                sorted(resultado)
            )
        )

    else:

        imprimir_info(
            "No tienen materias en común."
        )

    pausa()


# =========================================================
# MATERIAS OFERTADAS
# =========================================================

def opcion_materias_ofertadas():

    imprimir_titulo(
        "MATERIAS REGISTRADAS"
    )

    materias = materias_ofertadas()

    if materias:

        for materia in sorted(materias):
            print(
                f" - {materia}"
            )

    else:

        imprimir_info(
            "Todavía no hay materias registradas."
        )

    pausa()


def salir():

    imprimir_info(
        "¡Hasta luego! 👋"
    )

    return "salir"


OPCIONES = {

    "1": (
        "Crear estudiante",
        opcion_crear
    ),

    "2": (
        "Ver todos",
        opcion_ver_todos
    ),

    "3": (
        "Buscar estudiante",
        opcion_buscar
    ),

    "4": (
        "Ver por ID",
        opcion_ver_por_id
    ),

    "5": (
        "Actualizar estudiante",
        opcion_actualizar
    ),

    "6": (
        "Eliminar estudiante",
        opcion_eliminar
    ),

    "7": (
        "Agregar nota",
        opcion_agregar_nota
    ),

    "8": (
        "Ver promedio",
        opcion_ver_promedio
    ),

    "9": (
        "Materias en común",
        opcion_materias_comun
    ),

    "10": (
        "Materias registradas",
        opcion_materias_ofertadas
    ),

    "0": (
        "Salir",
        salir
    )
}


def mostrar_menu():

    imprimir_titulo(
        "SISTEMA DE GESTIÓN DE ESTUDIANTES"
    )

    for tecla, (texto, _funcion) in OPCIONES.items():

        print(
            f"  {tecla}. {texto}"
        )

    print()


def main():

    while True:

        mostrar_menu()

        tecla = input(
            "Seleccione una opción: "
        ).strip()

        if tecla not in OPCIONES:

            imprimir_error(
                "Opción no válida"
            )

            pausa()
            continue

        _texto, funcion = OPCIONES[
            tecla
        ]

        if funcion() == "salir":
            break


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\nPrograma interrumpido "
            "por el usuario."
        )