"""Ferramentas BR (4Devs offline) — 74 ferramentas: geradores e validadores de documentos,
funções de texto e calculadoras de matemática. Tudo offline, no seu PC.

A interface monta os formulários sozinha a partir do registro (registry.py).
Documentos são gerados por algoritmo (dígitos verificadores) pra TESTAR sistemas —
não são de pessoas reais.
"""
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QFormLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton,
                             QSpinBox, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import registry  # noqa: E402

ACCENT = "#7c5cff"
QSS = """
QWidget { background:#11131a; color:#e7e9f0; font:10pt 'Segoe UI'; }
#title { font:800 17pt 'Segoe UI'; }
#sub { color:#8a93a8; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { background:#1b202b; border:1px solid #2d3550;
    border-radius:8px; padding:6px; }
QLineEdit:focus, QPlainTextEdit:focus { border:1px solid #7c5cff; }
QPlainTextEdit { background:#161a23; border:1px solid #2d3550; border-radius:10px; padding:8px; }
#saida { background:#0c0e14; font:11pt 'Consolas','Segoe UI'; }
QTreeWidget { background:#161a23; border:1px solid #2d3550; border-radius:10px; outline:0; }
QTreeWidget::item { padding:4px 2px; }
QTreeWidget::item:selected { background:#2d3550; color:#fff; border-radius:5px; }
QCheckBox { spacing:7px; }
QPushButton { background:#222a38; border:0; border-radius:10px; padding:9px 14px; }
QPushButton:hover { background:#2d3550; }
#go { background:#7c5cff; color:#fff; font-weight:600; padding:10px 16px; }
#go:hover { background:#8f74ff; }
QLineEdit#busca { font:11pt 'Segoe UI'; padding:9px 12px; border-radius:10px; }
"""


def app_icon():
    pm = QPixmap(64, 64)
    pm.fill(QColor("transparent"))
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(ACCENT))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawRoundedRect(8, 8, 48, 48, 12, 12)
    p.setPen(QColor("white"))
    p.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, "BR")
    p.end()
    return QIcon(pm)


class Painel(QWidget):
    """Monta o formulário de UMA função e roda."""

    def __init__(self, func, parent=None):
        super().__init__(parent)
        self.func = func
        self.widgets = {}
        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 0, 4, 0)
        lay.setSpacing(10)
        lay.addWidget(QLabel(func.nome, objectName="title"))

        form = QFormLayout()
        form.setSpacing(8)
        for c in func.campos:
            w = self._make_widget(c)
            self.widgets[c.chave] = (c, w)
            if c.tipo == "bool":
                form.addRow("", w)
            else:
                form.addRow(c.rotulo + ":", w)
        lay.addLayout(form)

        br = QHBoxLayout()
        self.go = QPushButton(func.botao)
        self.go.setObjectName("go")
        self.go.clicked.connect(self.run)
        br.addWidget(self.go)
        self.copy = QPushButton("📋 Copiar")
        self.copy.clicked.connect(self._copy)
        br.addWidget(self.copy)
        br.addStretch(1)
        lay.addLayout(br)

        self.saida = QPlainTextEdit(objectName="saida")
        self.saida.setReadOnly(True)
        self.saida.setPlaceholderText("O resultado aparece aqui…")
        lay.addWidget(self.saida, 1)

    def _make_widget(self, c):
        if c.tipo == "multiline":
            w = QPlainTextEdit()
            if c.placeholder:
                w.setPlaceholderText(c.placeholder)
            if c.default:
                w.setPlainText(str(c.default))
            w.setMinimumHeight(90)
            return w
        if c.tipo == "bool":
            w = QCheckBox(c.rotulo)
            w.setChecked(bool(c.default))
            return w
        if c.tipo == "escolha":
            w = QComboBox()
            w.addItems([str(o) for o in (c.opcoes or [])])
            if c.default is not None:
                i = w.findText(str(c.default))
                if i >= 0:
                    w.setCurrentIndex(i)
            return w
        if c.tipo == "int":
            w = QSpinBox()
            w.setRange(-1_000_000_000, 1_000_000_000)
            w.setValue(int(c.default or 0))
            return w
        if c.tipo == "float":
            w = QDoubleSpinBox()
            w.setRange(-1e12, 1e12)
            w.setDecimals(4)
            w.setValue(float(c.default or 0))
            return w
        w = QLineEdit()
        if c.placeholder:
            w.setPlaceholderText(c.placeholder)
        if c.default:
            w.setText(str(c.default))
        return w

    def _values(self):
        vals = {}
        for chave, (c, w) in self.widgets.items():
            if c.tipo == "multiline":
                vals[chave] = w.toPlainText()
            elif c.tipo == "bool":
                vals[chave] = w.isChecked()
            elif c.tipo == "escolha":
                vals[chave] = w.currentText()
            elif c.tipo == "int":
                vals[chave] = int(w.value())
            elif c.tipo == "float":
                vals[chave] = float(w.value())
            else:
                vals[chave] = w.text()
        return vals

    def run(self):
        try:
            out = self.func.run(self._values())
        except Exception as e:  # noqa: BLE001
            out = f"Erro: {e}"
        self.saida.setPlainText(str(out))

    def _copy(self):
        t = self.saida.toPlainText()
        if t:
            QApplication.clipboard().setText(t)


class FerramentasBR(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ferramentas BR (4Devs offline)")
        self.setWindowIcon(app_icon())
        self.resize(900, 640)
        self.painel = None

        root = QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(12)

        # esquerda: busca + árvore
        left = QVBoxLayout()
        left.setSpacing(8)
        head = QVBoxLayout()
        head.setSpacing(1)
        head.addWidget(QLabel("Ferramentas BR", objectName="title"))
        head.addWidget(QLabel(f"{len(registry.FUNCS)} ferramentas offline", objectName="sub"))
        left.addLayout(head)
        self.busca = QLineEdit(objectName="busca")
        self.busca.setPlaceholderText("Buscar…")
        self.busca.textChanged.connect(self._filter)
        left.addWidget(self.busca)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setMinimumWidth(270)
        self.tree.itemClicked.connect(self._select)
        left.addWidget(self.tree, 1)
        lw = QWidget()
        lw.setLayout(left)
        lw.setMaximumWidth(300)
        root.addWidget(lw)

        # direita: painel da função
        self.right = QVBoxLayout()
        self.placeholder = QLabel("← Escolha uma ferramenta na lista.", objectName="sub")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right.addWidget(self.placeholder)
        rw = QWidget()
        rw.setLayout(self.right)
        root.addWidget(rw, 1)

        self._build_tree()

    def _build_tree(self):
        self.tree.clear()
        grupos = registry.por_categoria()
        for cat in registry.CATEGORIAS:
            funcs = grupos.get(cat, [])
            if not funcs:
                continue
            top = QTreeWidgetItem([f"{cat}  ({len(funcs)})"])
            top.setFlags(Qt.ItemFlag.ItemIsEnabled)
            f = top.font(0)
            f.setBold(True)
            top.setFont(0, f)
            self.tree.addTopLevelItem(top)
            for fn in funcs:
                it = QTreeWidgetItem([fn.nome])
                it.setData(0, Qt.ItemDataRole.UserRole, fn)
                top.addChild(it)
            top.setExpanded(True)

    def _filter(self, q):
        q = q.lower().strip()
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            shown = 0
            for j in range(top.childCount()):
                it = top.child(j)
                vis = q in it.text(0).lower()
                it.setHidden(not vis)
                shown += vis
            top.setHidden(shown == 0)

    def _select(self, item):
        fn = item.data(0, Qt.ItemDataRole.UserRole)
        if not fn:
            return
        if self.placeholder:
            self.placeholder.deleteLater()
            self.placeholder = None
        if self.painel:
            self.painel.deleteLater()
        self.painel = Painel(fn)
        self.right.addWidget(self.painel)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    w = FerramentasBR()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
