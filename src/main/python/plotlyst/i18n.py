import json
from logging import getLogger
from typing import Dict

from PyQt6.QtCore import QObject, pyqtSignal

from plotlyst.env import app_env

log = getLogger(__name__)

_TRANSLATIONS: Dict[str, str] = {}


class I18N(QObject):
    language_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._language = None

    def set_language(self, language: str):
        self._language = language
        self.language_changed.emit()

    def language(self) -> str:
        return self._language


i18n = I18N()


def t(text: str, *args) -> str:
    if not _TRANSLATIONS:
        load_translations()

    return _TRANSLATIONS.get(text, text).format(*args)


from plotlyst.settings import settings


def load_translations():
    lang = settings.language()
    if not lang:
        return

    try:
        from importlib.resources import files
        resource = files('plotlyst.resources.i18n').joinpath(f'{lang}.json')
        with resource.open('r', encoding='utf-8') as f:
            global _TRANSLATIONS
            _TRANSLATIONS = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log.warning(f'Could not load translation file for language "{lang}": {e}')


i18n.language_changed.connect(load_translations)
