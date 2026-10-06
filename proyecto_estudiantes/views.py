from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# AHORA GUARDA ESTUDIANTES
gestor = GestorJSON("data/estudiantes.json")


# TUPLAS DE CONFIGURACIÓN
CAMPOS_OBLIGATORIOS = (
    "nombre",
    "apellido",
    "email",
    "carnet"
)

CAMPOS_BUSCABLES = (
    "nombre",
    "apellido",
    "email",
    "carnet"
)


def carnets_registrados(excepto_id=None):
    """SET con los carnets registrados."""

    return {
        registro["carnet"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def emails_registrados(excepto_id=None):
    """SET con los emails registrados."""

    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():

    ids = [
        registro["id"]
        for registro in gestor.leer()
    ]

    if ids:
        return max(ids) + 1

    return 1


def crear_estudiante(datos):

    try:

        valores = {
            campo: str(
                datos.get(campo, "")
            ).strip()

            for campo in CAMPOS_ESTUDIANTE
        }

        faltantes = [
            campo
            for campo in CAMPOS_OBLIGATORIOS
            if not valores[campo]
        ]

        if faltantes:
            return (
                False,
                "Faltan campos obligatorios: "
                + ", ".join(faltantes)
            )

        if not es_email_valido(
            valores["email"]
        ):
            return (
                False,
                "El email no tiene un formato válido"
            )

        # VALIDAR CARNET REPETIDO
        if valores["carnet"].lower() in carnets_registrados():
            return (
                False,
                "Ese carnet ya está registrado"
            )

        # VALIDAR EMAIL REPETIDO
        if valores["email"].lower() in emails_registrados():
            return (
                False,
                "Ese email ya está registrado"
            )

        estudiante = Estudiante(
            siguiente_id(),
            valores["nombre"],
            valores["apellido"],
            valores["email"],
            valores["carnet"]
        )

        registros = gestor.leer()

        registros.append(
            estudiante.a_diccionario()
        )

        if not gestor.guardar(registros):
            return (
                False,
                "No se pudo guardar el estudiante"
            )

        return (
            True,
            f"Estudiante "
            f"{estudiante.obtener_nombre_completo()} "
            f"creado con id {estudiante.id}"
        )

    except Exception as error:

        return (
            False,
            f"Error inesperado: {error}"
        )


def obtener_todos():

    return [
        Estudiante.desde_diccionario(registro)
        for registro in gestor.leer()
    ]


def obtener_por_id(id_estudiante):

    for estudiante in obtener_todos():

        if estudiante.id == id_estudiante:
            return estudiante

    return None


def buscar_estudiantes(termino):

    termino = termino.strip().lower()

    if not termino:
        return []

    encontrados = []

    for registro in gestor.leer():

        for campo in CAMPOS_BUSCABLES:

            valor = str(
                registro.get(campo, "")
            ).lower()

            if termino in valor:

                encontrados.append(
                    Estudiante.desde_diccionario(
                        registro
                    )
                )

                break

    return encontrados


def actualizar_estudiante(
    id_estudiante,
    cambios
):

    try:

        campos_validos = set(
            CAMPOS_ESTUDIANTE
        )

        campos_recibidos = set(
            cambios.keys()
        )

        desconocidos = (
            campos_recibidos
            - campos_validos
        )

        if desconocidos:

            return (
                False,
                "Campos no válidos: "
                + ", ".join(
                    sorted(desconocidos)
                )
            )

        if not cambios:

            return (
                False,
                "No se indicó ningún cambio"
            )

        # VALIDAR EMAIL
        if "email" in cambios:

            if not es_email_valido(
                cambios["email"]
            ):
                return (
                    False,
                    "El email no tiene "
                    "un formato válido"
                )

            if (
                cambios["email"].lower()
                in emails_registrados(
                    excepto_id=id_estudiante
                )
            ):
                return (
                    False,
                    "Ese email ya lo usa "
                    "otro estudiante"
                )

        # VALIDAR CARNET
        if "carnet" in cambios:

            if (
                cambios["carnet"].lower()
                in carnets_registrados(
                    excepto_id=id_estudiante
                )
            ):
                return (
                    False,
                    "Ese carnet ya lo usa "
                    "otro estudiante"
                )

        registros = gestor.leer()

        posicion = None

        for indice, registro in enumerate(registros):

            if registro["id"] == id_estudiante:

                posicion = indice
                break

        if posicion is None:

            return (
                False,
                f"No existe un estudiante "
                f"con id {id_estudiante}"
            )

        registros[posicion].update(cambios)

        if not gestor.guardar(registros):

            return (
                False,
                "No se pudo guardar el cambio"
            )

        return (
            True,
            f"Estudiante {id_estudiante} "
            f"actualizado"
        )

    except Exception as error:

        return (
            False,
            f"Error inesperado: {error}"
        )


def eliminar_estudiante(id_estudiante):

    registros = gestor.leer()

    quedan = [
        registro
        for registro in registros
        if registro["id"] != id_estudiante
    ]

    if len(quedan) == len(registros):

        return (
            False,
            f"No existe un estudiante "
            f"con id {id_estudiante}"
        )

    gestor.guardar(quedan)

    return (
        True,
        f"Estudiante {id_estudiante} eliminado"
    )


def agregar_nota(
    id_estudiante,
    materia,
    nota
):

    try:

        # La guía pide notas de 0 a 20
        if nota < 0 or nota > 20:

            return (
                False,
                "La nota debe estar "
                "entre 0 y 20"
            )

        registros = gestor.leer()

        for registro in registros:

            if registro["id"] == id_estudiante:

                notas = registro.get(
                    "notas",
                    {}
                )

                materias = set(
                    registro.get(
                        "materias",
                        []
                    )
                )

                materias.add(materia)

                notas.setdefault(
                    materia,
                    []
                ).append(nota)

                registro["notas"] = notas
                registro["materias"] = sorted(
                    materias
                )

                gestor.guardar(
                    registros
                )

                return (
                    True,
                    f"Nota {nota} agregada "
                    f"en {materia}"
                )

        return (
            False,
            f"No existe un estudiante "
            f"con id {id_estudiante}"
        )

    except Exception as error:

        return (
            False,
            f"Error inesperado: {error}"
        )


def materias_ofertadas():

    materias = set()

    for registro in gestor.leer():

        materias.update(
            registro.get(
                "materias",
                []
            )
        )

    return materias


def estudiantes_en_comun(
    id_a,
    id_b
):

    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    if not estudiante_a:
        return (
            False,
            f"No existe el estudiante "
            f"con id {id_a}"
        )

    if not estudiante_b:
        return (
            False,
            f"No existe el estudiante "
            f"con id {id_b}"
        )

    comunes = (
        estudiante_a.materias
        &
        estudiante_b.materias
    )

    return True, comunes