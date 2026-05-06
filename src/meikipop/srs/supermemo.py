import html
import os
import re
from dataclasses import dataclass
from typing import Iterable

from meikipop.config.config import config
from meikipop.dictionary.lookup import DictionaryEntry, KanjiEntry
from meikipop.utils.paths import paths


class SuperMemoExportError(RuntimeError):
    """Raised when a lookup cannot be turned into a SuperMemo card."""


@dataclass
class SuperMemoCard:
    question: str
    answer: str
    text: str


class SuperMemoExporter:
    """Append popup lookups to SuperMemo's UTF-8 Q&A text import format."""

    def __init__(self, export_path: str | None = None):
        self.export_path = export_path or config.supermemo_export_path or paths.supermemo_qna_path

    def append_from_entries(self, entries: Iterable[DictionaryEntry | KanjiEntry] | None) -> SuperMemoCard:
        entry = self._select_entry(entries)
        if not entry:
            raise SuperMemoExportError("No lookup is available to export yet.")

        card = self._card_from_entry(entry)
        export_dir = os.path.dirname(self.export_path)
        if export_dir:
            os.makedirs(export_dir, exist_ok=True)

        needs_separator = os.path.exists(self.export_path) and os.path.getsize(self.export_path) > 0
        with open(self.export_path, "a", encoding="utf-8", newline="\n") as f:
            if needs_separator:
                f.write("\n")
            f.write(card.text)
            f.write("\n")
        return card

    def _select_entry(self, entries: Iterable[DictionaryEntry | KanjiEntry] | None):
        if not entries:
            return None

        materialized = list(entries)
        for entry in materialized:
            if isinstance(entry, DictionaryEntry):
                return entry
        for entry in materialized:
            if isinstance(entry, KanjiEntry):
                return entry
        return None

    def _card_from_entry(self, entry: DictionaryEntry | KanjiEntry) -> SuperMemoCard:
        if isinstance(entry, DictionaryEntry):
            question = self._question_for_dictionary_entry(entry)
            answer = self._answer_for_dictionary_entry(entry)
        elif isinstance(entry, KanjiEntry):
            question = self._inline(entry.character)
            answer = self._answer_for_kanji_entry(entry)
        else:
            raise SuperMemoExportError("Unsupported lookup entry type.")

        text = f"Q: {question}\nA: {answer}"
        return SuperMemoCard(question=question, answer=answer, text=text)

    def _question_for_dictionary_entry(self, entry: DictionaryEntry) -> str:
        question = self._inline(entry.written_form)
        if entry.reading and entry.reading != entry.written_form:
            question += f" [{self._inline(entry.reading)}]"
        return question

    def _answer_for_dictionary_entry(self, entry: DictionaryEntry) -> str:
        heading = f"<b>{self._inline(entry.written_form)}</b>"
        if entry.reading and entry.reading != entry.written_form:
            heading += f" [{self._inline(entry.reading)}]"

        sense_lines = []
        for idx, sense in enumerate(entry.senses, start=1):
            glosses = sense.get("glosses", [])
            if not glosses:
                continue
            gloss_text = "; ".join(self._inline(g) for g in glosses)
            pos = sense.get("pos", [])
            pos_text = f" <i>({self._inline(', '.join(pos))})</i>" if pos else ""
            sense_lines.append(f"{idx}. {gloss_text}{pos_text}")

        if not sense_lines:
            sense_lines.append("No glosses were available for this lookup.")

        footer = '<small>mined by superpop for SuperMemo Q&A import</small>'
        return "<br>".join([heading, *sense_lines, footer])

    def _answer_for_kanji_entry(self, entry: KanjiEntry) -> str:
        parts = [f"<b>{self._inline(entry.character)}</b>"]
        if entry.meanings:
            parts.append("Meanings: " + self._inline(", ".join(entry.meanings)))
        if entry.readings:
            parts.append("Readings: " + self._inline(", ".join(entry.readings)))
        if entry.components:
            component_text = ", ".join(
                self._inline(f"{c.get('c', '')} {c.get('m', '')}".strip())
                for c in entry.components
                if c.get("c") or c.get("m")
            )
            if component_text:
                parts.append("Components: " + component_text)
        parts.append('<small>mined by superpop for SuperMemo Q&A import</small>')
        return "<br>".join(parts)

    def _inline(self, value) -> str:
        compact = re.sub(r"\s+", " ", str(value)).strip()
        return html.escape(compact, quote=False)
