"""Interfaz de linea de comandos para el clasificador cloud."""

import argparse

from classifier import CloudServiceClassifier


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser sin ejecutar la clasificacion."""
    parser = argparse.ArgumentParser(
        description="Clasifica una descripcion de servicio cloud."
    )
    parser.add_argument(
        "--text",
        required=True,
        help="Descripcion del servicio cloud que se desea clasificar.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Ejecuta la CLI y devuelve un codigo de salida de shell."""
    args = build_parser().parse_args(argv)
    result = CloudServiceClassifier().classify(args.text)

    if result.is_success:
        print(f"Modelo identificado: {result.model.value}")
        return 0

    print(result.message)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
