"""
Custom internationalization module for Plotlyst.
This module provides a simple JSON-based translation mechanism
to bypass the issues with the standard Qt i18n toolchain.
"""
import json
from typing import Optional

import pkg_resources
from fbs_runtime.application_context import ApplicationContext

_translations = {}
_app_context: Optional[ApplicationContext] = None


def set_up_i18n(context: Optional[ApplicationContext]):
    """
    Sets up the i18n module by providing the application context.
    This must be called once at application startup.
    """
    global _app_context
    _app_context = context


def load_translation(lang: str):
    """
    Loads a translation file for the given language.
    """
    global _translations
    resource_path = ""
    try:
        if _app_context:
            resource_path = _app_context.get_resource(f"i18n/{lang}.json")
        else:
            resource_path = pkg_resources.resource_filename('plotlyst', f'resources/i18n/{lang}.json')

        with open(resource_path, "r", encoding="utf-8") as f:
            _translations = json.load(f)
    except FileNotFoundError:
        print(f"Warning: Translation file for language '{lang}' not found at {resource_path}.")
        _translations = {}


from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget


def t(key: str) -> str:
    """
    Translates a given key.
    If the key is not found in the current translation, it returns the key itself.
    """
    return _translations.get(key, key)


def translate_ui(widget: QWidget):
    """
    Recursively translates all child widgets of a given widget.
    """
    for child in widget.findChildren(QWidget):
        # Translate text property
        if hasattr(child, 'text') and callable(getattr(child, 'text')):
            original_text = child.text()
            if original_text:
                translated_text = t(original_text)
                if translated_text != original_text:
                    child.setText(translated_text)

        # Translate windowTitle property
        if hasattr(child, 'windowTitle') and callable(getattr(child, 'windowTitle')):
            original_title = child.windowTitle()
            if original_title:
                translated_title = t(original_title)
                if translated_title != original_title:
                    child.setWindowTitle(translated_title)

        # Translate title property (for QMenu, etc.)
        if hasattr(child, 'title') and callable(getattr(child, 'title')):
            original_title = child.title()
            if original_title:
                translated_title = t(original_title)
                if translated_title != original_title:
                    child.setTitle(translated_title)

        # Translate toolTip property
        if hasattr(child, 'toolTip') and callable(getattr(child, 'toolTip')):
            original_tooltip = child.toolTip()
            if original_tooltip:
                translated_tooltip = t(original_tooltip)
                if translated_tooltip != original_tooltip:
                    child.setToolTip(translated_tooltip)

        # Translate placeholderText property
        if hasattr(child, 'placeholderText') and callable(getattr(child, 'placeholderText')):
            original_placeholder = child.placeholderText()
            if original_placeholder:
                translated_placeholder = t(original_placeholder)
                if translated_placeholder != original_placeholder:
                    child.setPlaceholderText(translated_placeholder)

    # Special handling for QAction objects in menus
    for action in widget.findChildren(QAction):
        original_text = action.text()
        if original_text:
            translated_text = t(original_text)
            if translated_text != original_text:
                action.setText(translated_text)
