# HiDPI Display Issues and Solutions

This document records known HiDPI-related issues encountered during OpenPCB development and their solutions.

---

## Issue: Menu Dropdown Misalignment on GNOME with HiDPI

**Date Discovered**: 2026-02-03
**Status**: ✅ FIXED
**Affects**: GNOME desktop environments with HiDPI scaling (e.g., Ubuntu GNOME)
**Qt Version**: PySide6 6.10.2 / Qt 6.10
**Platform**: Linux (GNOME)

### Symptoms

When running OpenPCB on a HiDPI display with GNOME desktop environment and `QT_SCALE_FACTOR=2.0` set:
- Menu labels appear in correct order (File, Edit, View, Tools, Help)
- Text scaling is correct (2x)
- **BUG**: Clicking on a menu label causes the dropdown to appear at the wrong position
  - Example: Clicking "File" shows File menu content, but dropdown appears under "View" label
  - Dropdown is offset to the right by approximately 2-3 menu items

### Root Cause

**Double Scaling Conflict**: When `QT_SCALE_FACTOR` is set externally by the desktop environment, Qt 6's automatic HiDPI scaling can multiply this factor rather than using it directly. This causes two problems:

1. Geometry calculations become incorrect (scale is applied twice)
2. Menu dropdown positioning uses incorrectly scaled coordinates
3. Click targets and visual positions become misaligned

From Qt 6 documentation:
> In Qt 6, `QT_SCALE_FACTOR` doesn't set the factor to your value, it multiplies it.

When both manual scale factor AND automatic scaling are enabled, Qt applies both, resulting in incorrect geometry.

### Solution

Two-part fix implemented in `openpcb/ui/hidpi.py` and `openpcb/__main__.py`:

#### Part 1: Disable Automatic Scaling When External Scale Factor Detected

In `configure_hidpi()` function:

```python
external_scale = os.environ.get("QT_SCALE_FACTOR")

if external_scale and settings.scale_mode == "auto":
    # Prevent double scaling
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    logger.info(f"External QT_SCALE_FACTOR={external_scale} detected")
```

**Why this works**: By disabling automatic scaling when an external scale factor is present, we prevent Qt from multiplying the scale factor. The external scale factor (set by GNOME) is used directly, giving correct text size and geometry.

#### Part 2: Disable Native Menu Bar on GNOME

In `main_gui()` function, before creating QApplication:

```python
QApplication.setAttribute(Qt.AA_DontUseNativeMenuBar, True)
```

**Why this works**: GNOME's global menu system can interfere with Qt menu rendering. Disabling the native menu bar forces Qt to render menus in-window, giving Qt full control over positioning.

### Testing

To verify the fix works:

1. Ensure `QT_SCALE_FACTOR=2.0` is set in environment (check with `echo $QT_SCALE_FACTOR`)
2. Run OpenPCB: `./run.sh`
3. Verify text is properly scaled (readable, not tiny)
4. Click each menu label (File, Edit, View, Tools, Help)
5. **Expected**: Each dropdown appears directly under the clicked label
6. **Expected**: Menu content matches the clicked label

### Additional Notes

- This issue is specific to environments where scale factor is set externally
- The fix gracefully handles cases where no external scale factor is present
- Custom scale mode still works correctly with explicit factor setting
- System scale mode properly defers to desktop environment settings

### References

- **Qt 6 HiDPI Documentation**: https://doc.qt.io/qt-6/highdpi.html
- **Qt Bug QTBUG-52606**: Combo boxes appear on wrong screen with HiDPI scaling
- **ArchWiki HiDPI Guide**: https://wiki.archlinux.org/title/HiDPI
- **Related Issue**: https://github.com/qutebrowser/qutebrowser/issues/4786

### Files Modified

- `openpcb/ui/hidpi.py` - Added double scaling detection and prevention
- `openpcb/__main__.py` - Added `AA_DontUseNativeMenuBar` attribute
- `openpcb/ui/mainwindow.py` - Added placeholder items to empty menus (prevents rendering issues)

---

## Future Considerations

### Other Potential HiDPI Issues

Watch for these potential issues on HiDPI displays:

1. **Icon Scaling**: Toolbar and menu icons may appear blurry or incorrect size
   - Solution: Use SVG icons or provide @2x/@3x variants
   - Check: `toolbar_icon_size` and `menu_icon_size` in HiDPI settings

2. **Custom Widgets**: Custom-painted widgets may not scale correctly
   - Solution: Use `devicePixelRatio()` when computing sizes
   - Check: Any custom QWidget paint events

3. **OpenGL/Qt Quick**: OpenGL viewports may have incorrect coordinate systems
   - Solution: Use proper framebuffer scaling in Qt Quick
   - Important for Phase 2 viewer implementation

4. **Multi-Monitor**: Different DPI on multiple monitors
   - Qt 6 should handle this automatically
   - Test on mixed DPI setups when available

### Testing Checklist for HiDPI

When testing on HiDPI displays:

- [ ] Text is crisp and properly sized
- [ ] Menu dropdowns appear at correct positions
- [ ] Icons are sharp (not blurry)
- [ ] Dock widget sizing is appropriate
- [ ] Tooltips appear at cursor position
- [ ] Custom widgets scale correctly
- [ ] Performance is acceptable (scaling overhead)

---

**Last Updated**: 2026-02-03
**Tested On**: Ubuntu GNOME with 2x scaling, PySide6 6.10.2
