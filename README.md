# Darcula

[![Version](https://img.shields.io/visual-studio-marketplace/v/rokoroku.vscode-theme-darcula)](https://marketplace.visualstudio.com/items?itemName=rokoroku.vscode-theme-darcula)
[![Installs](https://img.shields.io/visual-studio-marketplace/i/rokoroku.vscode-theme-darcula)](https://marketplace.visualstudio.com/items?itemName=rokoroku.vscode-theme-darcula)

A theme extension for [Visual Studio Code](https://code.visualstudio.com) based on **Darcula** theme from [Jetbrains](https://www.jetbrains.com) IDEs.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md)

## Description

- Mainly focused on HTML5 / CSS / JS (TS) development.  
- **Not exactly same with the theme from Jetbrains IDE**. There are few modifications to match look and feel with VS Code IDE.
- Follows common textmate tokens (such as `entity.name.type`, `entity.name.function`, `variable.property`...) so try it on any languages and report issues on the GitHub repo.
- Any suggestions/contributions are welcomed!
 

## Setting

- When installation completes, select **Darcula** as your color theme (Preferences → Workbench: Color Theme → **Darcula**)
- Select **Darcula GoLand Icons** under **Preferences: Product Icon Theme** to enable the bundled symbol icons, including Go structs, interfaces, functions, fields, constants, and packages.
- The completion popup uses 13px text and 20px rows by default. User and workspace settings take precedence. Remove older `editorSuggestWidget.*` color overrides to use the bundled palette. The bundled font uses fixed COLR/CPAL colors, so selecting a suggestion changes the row background and text while preserving its icon color. Rebuild the font after changing the symbol palette in `themes/darcula.json`.

The original icon outlines live in `scripts/build-icons.py`. To rebuild the bundled WOFF and icon mappings, use Python with the build-only dependency `fonttools==4.65.0` and run `npm run build:icons`. No Python or FontTools installation is needed to use the extension.

## Customizing

- If you want to customize on top of this theme, use vscode's [color customization](https://code.visualstudio.com/docs/getstarted/themes#_customizing-a-color-theme) feature.  
  (Related Issue: [#9](https://github.com/rokoroku/vscode-theme-darcula/issues/9), [#15](https://github.com/rokoroku/vscode-theme-darcula/issues/15))
 
## Screenshot

![Screenshot](https://github.com/rokoroku/vscode-theme-darcula/raw/master/screenshot.png)

**Enjoy!**
