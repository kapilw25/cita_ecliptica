"""Rename method labels in figure text at save time (CITA -> SwiPO); mapping lives in configs/pipeline.yaml. CPU-only.
    from src.utils.eval.display_names import apply_display_names; apply_display_names(fig)
"""

from __future__ import annotations

import re
from typing import Dict, Optional

import matplotlib.text

from src.utils.config import load_pipeline_config


def get_display_names() -> Dict[str, str]:
    """Return the {old_label: new_label} map from configs/pipeline.yaml (plots.display_names)."""
    return load_pipeline_config()["plots"]["display_names"]


def substitute(text: str, mapping: Dict[str, str]) -> str:
    """Replace whole-token occurrences of each old label (CITA_Instruct -> SwiPO_Instruct, not CITATION)."""
    for old, new in mapping.items():
        text = re.sub(rf"(?<![A-Za-z]){re.escape(old)}(?![A-Za-z])", new, text)
    return text


def apply_display_names(fig, mapping: Optional[Dict[str, str]] = None):
    """Rewrite every title, tick label, legend entry and annotation of `fig` in place; returns fig."""
    mapping = mapping if mapping is not None else get_display_names()
    # Tick labels come from the axis formatter at draw time (matplotlib >= 3.5 wraps
    # set_ticklabels() in a FuncFormatter, older versions in a FixedFormatter), so draw once to
    # realise them, then re-set only the axes whose realised labels actually change; numeric axes
    # (ScalarFormatter) never match a method name and are left untouched.
    fig.canvas.draw()
    for ax in fig.get_axes():
        for axis in (ax.xaxis, ax.yaxis):
            labels = [t.get_text() for t in axis.get_ticklabels()]
            renamed = [substitute(label, mapping) for label in labels]
            if renamed != labels:
                axis.set_ticklabels(renamed)
    for text_obj in fig.findobj(matplotlib.text.Text):
        current = text_obj.get_text()
        if current:
            text_obj.set_text(substitute(current, mapping))
    for ax in fig.get_axes():
        legend = ax.get_legend()
        if legend is not None:
            for text_obj in legend.get_texts():
                text_obj.set_text(substitute(text_obj.get_text(), mapping))
    for legend in fig.legends:
        for text_obj in legend.get_texts():
            text_obj.set_text(substitute(text_obj.get_text(), mapping))
    return fig
