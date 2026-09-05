"""Interfaz grafica Tkinter para el clasificador."""

import tkinter as tk
from tkinter import ttk

from classifier import CloudServiceClassifier


class CloudClassifierApp(ttk.Frame):
    """Ventana de clasificacion que depende solo del servicio de dominio."""

    def __init__(
        self, master: tk.Misc, classifier: CloudServiceClassifier | None = None
    ) -> None:
        super().__init__(master, padding=20)
        self.classifier = classifier or CloudServiceClassifier()
        self.name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.status = tk.StringVar(value="Escribe una descripcion para comenzar")
        self._build()

    def _build(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        ttk.Label(
            self,
            text="Clasificador de servicios Cloud",
            font=("TkDefaultFont", 18, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 16))

        user_frame = ttk.LabelFrame(self, text="Datos del usuario", padding=12)
        user_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        user_frame.columnconfigure(1, weight=1)
        user_frame.columnconfigure(3, weight=1)
        ttk.Label(user_frame, text="Nombre").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        ttk.Entry(user_frame, textvariable=self.name).grid(
            row=0, column=1, sticky="ew", padx=(0, 16)
        )
        ttk.Label(user_frame, text="Apellido").grid(
            row=0, column=2, sticky="w", padx=(0, 8)
        )
        ttk.Entry(user_frame, textvariable=self.last_name).grid(
            row=0, column=3, sticky="ew"
        )

        ttk.Label(self, text="Descripcion del servicio").grid(
            row=2, column=0, sticky="w", pady=(0, 6)
        )
        self.description = tk.Text(self, height=8, wrap="word", undo=True)
        self.description.grid(row=3, column=0, sticky="nsew")
        self.description.focus_set()

        controls = ttk.Frame(self)
        controls.grid(row=4, column=0, sticky="ew", pady=(12, 0))
        ttk.Button(controls, text="Clasificar", command=self._classify).pack(
            side="right"
        )
        ttk.Label(controls, textvariable=self.status, wraplength=600).pack(
            side="left", fill="x", expand=True
        )

    def _classify(self) -> None:
        if not self.name.get().strip() or not self.last_name.get().strip():
            self.status.set("Escribe tu nombre y apellido antes de clasificar.")
            return

        result = self.classifier.classify(self.description.get("1.0", "end-1c"))
        if result.is_success:
            scores = " | ".join(
                f"{model.value}: {score}" for model, score in result.scores.items()
            )
            self.status.set(
                f"Usuario: {self.name.get().strip()} {self.last_name.get().strip()} | {result.message} | {scores}"
            )
        else:
            self.status.set(result.message)


def run() -> None:
    root = tk.Tk()
    root.title("Clasificador de Modelos Cloud")
    root.minsize(720, 460)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    CloudClassifierApp(root).grid(row=0, column=0, sticky="nsew")
    root.mainloop()
