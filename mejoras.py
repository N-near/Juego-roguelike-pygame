"""Catálogo de mejoras que se pueden ofrecer entre oleadas."""

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Mejora:
    identificador: str
    nombre: str
    descripcion: str
    valor: float


CATALOGO_MEJORAS = (
    Mejora("curacion_1", "Curación pequeña", "Recupera 1 punto de vida.", 1),
    Mejora("curacion_2", "Curación grande", "Recupera 2 puntos de vida.", 2),
    Mejora("cadencia", "Disparo rápido", "Reduce 0.1 s entre disparos.", 0.1),
    Mejora("velocidad", "Pies ligeros", "Aumenta 10% tu velocidad.", 0.1),
    Mejora("danio", "Proyectiles fuertes", "Aumenta en 1 el daño.", 1),
    Mejora("vida_maxima", "Más resistencia", "Aumenta en 1 la vida máxima.", 1),
)


def elegir_opciones(
    vida_actual: int,
    vida_maxima: int,
    cantidad: int = 3,
) -> list[Mejora]:
    """Devuelve opciones distintas y omite curaciones si la vida está completa."""
    opciones_disponibles = [
        mejora
        for mejora in CATALOGO_MEJORAS
        if vida_actual < vida_maxima or not mejora.identificador.startswith("curacion_")
    ]
    return random.sample(opciones_disponibles, min(cantidad, len(opciones_disponibles)))
