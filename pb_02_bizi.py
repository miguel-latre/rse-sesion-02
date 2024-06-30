"""Proporciona una función para listar los usuarios que más han usado el
sistema Bizi Zaragoza.

Examples of use:
>>> usos_por_usuario("session-1/datos/pruebas-10.csv")
<BLANKLINE>
Número usuarios distintos: 9
<BLANKLINE>
   Usuario Traslados  Circular     Total
 ========= ========= ========= =========
     53535         1         0         1
     68977         1         0         1
     74089         0         1         1
     79884         1         0         1
     82664         1         0         1
     82747         1         0         1
     88192         1         0         1
     88412         1         0         1
     89736         1         0         1

>>> usos_por_usuario("session-1/datos/pruebas-2000.csv")
<BLANKLINE>
Número usuarios distintos: 1857
<BLANKLINE>
   Usuario Traslados  Circular     Total
 ========= ========= ========= =========
     15381         4         0         4
     47794         4         0         4
     89629         4         0         4
      2301         3         0         3
      6224         3         0         3
     24082         3         0         3
     27904         3         0         3
     39168         3         0         3
     40354         3         0         3
     46340         3         0         3
     53082         3         0         3
     81121         3         0         3
     86213         3         0         3
     89258         3         0         3
     90978         3         0         3
"""

from collections import namedtuple
from io import TextIOWrapper
from typing import Final


NUM_MOSTRAR: Final = 15
DELIMITADOR: Final = ";"
ANCHO: Final = 10
RUTA_DATOS: Final = "datos/"

UsuarioBizi = namedtuple("UsuarioBizi", "id num_usos_traslado num_usos_circular")


def buscar(usuarios: list[UsuarioBizi], id_usuario: int) -> tuple[bool, int]:
    """Busca un usuario de identificador id_usuario en usuarios

    Args:
        usuarios: lista de usuarios ordenada por id crecientes
        id_usuario: identificador del usuario a buscar

    Return:
        Si entre los usuarios hay uno cuyo identificador es igual a
        id_usuario, devuelve True y el índice del usuario en la lista.
        si no lo hay, devuelve False y el índice donde habría que insertarlo de
        forma ordenada para mantener el orden
    """
    if len(usuarios) == 0:
        return False, 0
    inf = 0
    sup = len(usuarios) - 1
    while inf < sup:
        med = (inf + sup) // 2
        if id_usuario > usuarios[med].id:
            inf = med + 1
        else:
            sup = med
    return id_usuario == usuarios[inf].id, inf


def ubicar(usuarios: list[UsuarioBizi], id_usuario: int) -> int:
    """Localiza un usuario en la lista o lo añade y devuelve su índice.

    Args:
        usuarios: ordenada por id crecientes
        id_usuario: identificador del usuario a ubicar

    Return:
        Si entre los usuarios de la lista hay uno cuyo identificador es
        id_usuario, devuelve el índice de dicho usuario si no lo hay, lo
        ha añade en la posición correcta para mantener el orden de la lista,
        contabilizando de momento para ese usuario 0 usos del sistema Bizi
        (tanto de traslado como circulares) y devuelve el índice de la lista
        donde está el usuario cuyo identificador es id_usuario.
    """
    esta, posicion = buscar(usuarios, id_usuario)
    if esta:
        return posicion
    if posicion == len(usuarios) - 1 and id_usuario > usuarios[posicion].id:
        posicion += 1
    usuarios.insert(posicion, UsuarioBizi(id_usuario, 0, 0))
    return posicion


UsoBizi = namedtuple("UsoBizi", "id_usuario estacion_retirada estacion_devolucion")


def convertir(linea: str) -> UsoBizi:
    """Devuelve un UsoBizi de acuerdo con el contenido de linea

    Args:
        linea: tiene el formato de usos del sistema Bizi establecido en el
        enunciado.

    Returns:
        Un UsoBizi de acuerdo con el contenido de linea.
    """
    elementos = linea.split(DELIMITADOR)
    return UsoBizi(int(elementos[0]), int(elementos[2]), int(elementos[4]))


def incrementar_traslados(usuario: UsuarioBizi) -> UsuarioBizi:
    """Devuelve un usuario con un uso más de traslado"""
    return UsuarioBizi(
        usuario.id, usuario.num_usos_traslado + 1, usuario.num_usos_circular
    )


def incrementar_circulares(usuario: UsuarioBizi) -> UsuarioBizi:
    """Devuelve un usuario con un uso circular más"""
    return UsuarioBizi(
        usuario.id, usuario.num_usos_traslado, usuario.num_usos_circular + 1
    )


def obtener_usos_por_usuario_from_file(f: TextIOWrapper) -> list[UsuarioBizi]:
    """Lee de f la información relativa usuarios

    Args:
        f: asociado con un fichero del que se puede leer
        información sobre usos del sistema Bizi Zaragoza y con el formato
        establecido en el enunciado.

    Returns:
        la información de usuarios extraída de f. Es una lista con tantos
        elementos como número de usuarios distintos que aparecen en f.
    """
    f.readline()  # Línea de cabecera
    usuarios = []
    for linea in f:
        uso = convertir(linea)
        indice = ubicar(usuarios, uso.id_usuario)
        if uso.estacion_retirada == uso.estacion_devolucion:
            usuarios[indice] = incrementar_circulares(usuarios[indice])
        else:
            usuarios[indice] = incrementar_traslados(usuarios[indice])
    return usuarios


def num_usos_totales(usuario: UsuarioBizi) -> int:
    """Devuelve el número total de usos del sistema Bizi correspondiente a
    usuario.
    """
    return usuario.num_usos_traslado + usuario.num_usos_circular


def obtener_usos_por_usuario(nombre_fichero: str) -> list[UsuarioBizi]:
    """Lee de nombre_fichero la información relativa usuarios

    Args:
        nombre_fichero contiene la ruta y nombre de un fichero de texto con
        información sobre usos del sistema Bizi Zaragoza y con el formato
        establecido en el enunciado.

    Returns:
        la información de usuarios extraída de f. Es una lista con tantos
        elementos como número de usuarios distintos que aparecen en f (sin
        ningún orden concreto)

    Raises:
        OSError: si nombre_fichero no existe o no puede abrirse.
    """
    with open(nombre_fichero, encoding="utf-8") as f:
        return obtener_usos_por_usuario_from_file(f)


def mostrar_usuario(usuario: UsuarioBizi) -> None:
    """Muestra en la pantalla una línea con la información de usuario.

    Escribe una línea en la pantalla que contiene la información de
    usuario (identificador, número de usos entre estaciones distintas, número
    de usos entre la misma estación y número de usos totales), escrita en ese
    orden y utilizando un mínimo de 10 caracteres en cada caso.
    """

    print(
        f"{usuario.id:>{ANCHO}}{usuario.num_usos_traslado:{ANCHO}}"
        + f"{usuario.num_usos_circular:{ANCHO}}{num_usos_totales(usuario):{ANCHO}}"
    )


def buscar_indice_del_mayor(usuarios: list[UsuarioBizi], indice_inicial: int) -> int:
    """Devuelve el índice de

    Args:
        usuarios: lista de usuarios
        indice_inicial: índice a partir del que buscar.
        0 <= indice_inicial < len(usuarios)

    Returns:
        el índice de la componente de la lista usuarios[indice_inicial:] que
        tiene un mayor número de usos de traslados.
    """
    # Esquema de búsqueda de máximo
    indice_del_mayor = indice_inicial
    usos_del_mayor = num_usos_totales(usuarios[indice_del_mayor])
    for i in range(indice_inicial + 1, len(usuarios)):
        if num_usos_totales(usuarios[i]) > usos_del_mayor:
            indice_del_mayor = i
            usos_del_mayor = num_usos_totales(usuarios[indice_del_mayor])
    return indice_del_mayor


def pedir_nombre_fichero() -> str:
    """Solicita un nombre de fichero y devuelve una ruta al mismo.

    Solicita al usuario el nombre de un fichero de usos del sistema Bizi
    escribiendo en la pantalla el mensaje
    "Escriba el nombre de un fichero de usos del sistema Bizi: ",
    lo lee de teclado y asigna a «nombreRelativo» una ruta de acceso relativa
    al mismo, consistente en la concatenación de la cadena «RUTA_DATOS» y el
    nombre de fichero leído de teclado.
    """
    nombre_fichero = input("Escriba el nombre de un fichero de usos del sistema Bizi: ")
    return RUTA_DATOS + nombre_fichero


def ordenar(usuarios: list[UsuarioBizi], num_ordenar: int) -> None:
    """Ordena los primeros num_ordenar datos de la lista usuarios

    Ordena parcialmente la lista de forma que los num_ordenar primeros son
    los usuarios de mayor número de usos y están ordenados por número de
    usos decreciente.

    Args:
        usuarios:
            la lista a ordenar parcialmente.
        num_ordenar:
            el número de elementos a ordenar.
    """
    for i in range(0, min(num_ordenar, len(usuarios))):
        indice_del_mayor = buscar_indice_del_mayor(usuarios, i)
        usuarios[i], usuarios[indice_del_mayor] = (
            usuarios[indice_del_mayor],
            usuarios[i],
        )


def mostrar(usuarios: list[UsuarioBizi], num_mostrar: int) -> None:
    """Escribe la lista de los num_mostrar usuarios que más han usado Bizi"""
    print()
    print("Número usuarios distintos:", len(usuarios))
    print()
    print("   Usuario Traslados  Circular     Total")
    print(" ========= ========= ========= =========")
    for i in range(0, min(num_mostrar, len(usuarios))):
        mostrar_usuario(usuarios[i])


def usos_por_usuario(nombre_fichero: str) -> None:
    """Lee de nombre_fichero la información relativa usuarios y escribe en la pantalla
    los usuarios que más la han usado
    """
    usuarios = obtener_usos_por_usuario(nombre_fichero)
    ordenar(usuarios, NUM_MOSTRAR)
    mostrar(usuarios, NUM_MOSTRAR)


def main() -> None:
    """Lee de un fichero cuyo nombre facilita el usuario la información relativa
    usuarios y escribe en la pantalla los usuarios que más la han usado.
    """

    usos_por_usuario(pedir_nombre_fichero())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
