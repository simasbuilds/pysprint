"""PySprint icon set — hand-drawn SVG replacing every emoji in the UI.

All icons share one geometry: a 24x24 box, stroked in `currentColor` at
1.8 units, round caps and joins. They are emitted once per page as a
<symbol> sprite (see templates/_icons.html) and referenced with <use>, so
adding an icon costs one entry here and nothing per usage.

Names are semantic, not pictorial: data files store `"icon": "terminal"`,
never a glyph, so the visual can change without touching content.
"""

ICONS = {
    # ── course marks ──────────────────────────────────────────────────
    "terminal": '<rect x="2.5" y="4" width="19" height="16" rx="2.8"/>'
                '<path d="m7 10 2.6 2.5L7 15"/><path d="M13 15.2h4.2"/>',
    "layers": '<path d="m12 3 8.6 4.6L12 12.2 3.4 7.6z"/>'
              '<path d="m3.4 12.2 8.6 4.6 8.6-4.6"/>'
              '<path d="m3.4 16.6 8.6 4.6 8.6-4.6"/>',
    "nodes": '<circle cx="6" cy="5.8" r="2.4"/><circle cx="18" cy="5.8" r="2.4"/>'
             '<circle cx="12" cy="18.2" r="2.4"/>'
             '<path d="M6 8.2v2.4a2.2 2.2 0 0 0 2.2 2.2h7.6a2.2 2.2 0 0 0 2.2-2.2V8.2"/>'
             '<path d="M12 12.8v3"/>',
    "wrench": '<path d="M15.8 3.4a5.6 5.6 0 0 0-7.3 7L3.7 15.2a2.1 2.1 0 0 0 0 2.9l2.2 2.2a2.1 2.1 0 0 0 2.9 0l4.8-4.8a5.6 5.6 0 0 0 7-7.3l-3.2 3.2-2.9-.7-.7-2.9z"/>',
    "plug": '<path d="M9 2.8v6.4"/><path d="M15 2.8v6.4"/>'
            '<path d="M6.4 9.2h11.2v2.9a5.6 5.6 0 0 1-11.2 0z"/>'
            '<path d="M12 17.7v3.5"/>',
    "robot": '<rect x="4" y="8.2" width="16" height="11" rx="3.2"/>'
             '<path d="M12 4.9v3.3"/><circle cx="12" cy="3.6" r="1.3"/>'
             '<path d="M9.3 12.6v1.6"/><path d="M14.7 12.6v1.6"/>'
             '<path d="M2 13.2v2.8"/><path d="M22 13.2v2.8"/>',

    # ── project marks ─────────────────────────────────────────────────
    "wallet": '<path d="M3 8A2.6 2.6 0 0 1 5.6 5.4H18"/>'
              '<rect x="3" y="7.8" width="18" height="11.8" rx="2.6"/>'
              '<circle cx="16.6" cy="13.7" r="1.25"/>',
    "shield-key": '<path d="M12 3 5.2 6v5.4c0 4.2 2.8 7.6 6.8 9.4 4-1.8 6.8-5.2 6.8-9.4V6z"/>'
                  '<circle cx="12" cy="11" r="1.7"/><path d="M12 12.7v2.6"/>',
    "checklist": '<path d="M10 6.2h9.5"/><path d="M10 12h9.5"/><path d="M10 17.8h9.5"/>'
                 '<path d="m3.4 5.9 1.3 1.3 2.4-2.5"/>'
                 '<path d="m3.4 11.7 1.3 1.3 2.4-2.5"/>'
                 '<path d="m3.4 17.5 1.3 1.3 2.4-2.5"/>',
    "bar-chart": '<path d="M4.6 20.2v-5.4"/><path d="M9.5 20.2V8.6"/>'
                 '<path d="M14.5 20.2v-8.2"/><path d="M19.4 20.2V4.4"/>'
                 '<path d="M2.6 20.2h18.8"/>',
    "bolt": '<path d="M13.2 2.4 4.6 13.6h6.3l-1 8 8.5-11.2h-6.3z"/>',

    # ── achievements ──────────────────────────────────────────────────
    "flag": '<path d="M5.2 21V3.4"/>'
            '<path d="M5.2 4.6h11.4l-2.1 3.6 2.1 3.6H5.2z"/>',
    "flame": '<path d="M12.4 2.4c.7 3.2 2.5 4.5 4 6A7.6 7.6 0 0 1 18.7 14a6.7 6.7 0 0 1-13.4 0c0-2.1.9-3.7 2.2-5 .3 1.1 1 1.9 2 2.2-.1-3.1 1.2-6 2.9-8.8z"/>',
    "medal": '<circle cx="12" cy="15.4" r="5.6"/><circle cx="12" cy="15.4" r="1.9"/>'
             '<path d="m8.7 10.6-3.3-7.4h13.2l-3.3 7.4"/>',
    "trophy": '<path d="M7 3.8h10v5.1a5 5 0 0 1-10 0z"/>'
              '<path d="M7 5.4H4.4v1.4a3.1 3.1 0 0 0 3.1 3.1"/>'
              '<path d="M17 5.4h2.6v1.4a3.1 3.1 0 0 1-3.1 3.1"/>'
              '<path d="M12 13.9v3.6"/><path d="M8.4 20.4h7.2"/>',
    "swords": '<path d="M3.2 3.2h3.1l11.5 11.5v3.1h-3.1L3.2 6.3z"/>'
              '<path d="M20.8 3.2h-3.1L6.2 14.7v3.1h3.1L20.8 6.3z"/>',
    "shield": '<path d="M12 3 5.2 6v5.4c0 4.2 2.8 7.6 6.8 9.4 4-1.8 6.8-5.2 6.8-9.4V6z"/>'
              '<path d="m9.2 11.8 2 2 3.6-3.8"/>',
    "crown": '<path d="m2.8 7.6 3.6 3.2L12 4.6l5.6 6.2 3.6-3.2-1.6 11.4H4.4z"/>'
             '<path d="M4.4 19h15.2"/>',
    "star": '<path d="m12 3.4 2.7 5.5 6 .9-4.3 4.2 1 6-5.4-2.8-5.4 2.8 1-6L3.3 9.8l6-.9z"/>',
    "star-double": '<path d="m10 2.8 2.2 4.5 4.9.7-3.5 3.4.8 4.9-4.4-2.3-4.4 2.3.8-4.9-3.5-3.4 4.9-.7z"/>'
                   '<path d="m18.2 14.4 1 2.2 2.4.3-1.7 1.7.4 2.4-2.1-1.1-2.1 1.1.4-2.4-1.7-1.7 2.4-.3z"/>',
    "burst": '<path d="M12 1.8v3.6"/><path d="M12 18.6v3.6"/>'
             '<path d="M1.8 12h3.6"/><path d="M18.6 12h3.6"/>'
             '<path d="m4.8 4.8 2.6 2.6"/><path d="m16.6 16.6 2.6 2.6"/>'
             '<path d="m19.2 4.8-2.6 2.6"/><path d="m7.4 16.6-2.6 2.6"/>'
             '<circle cx="12" cy="12" r="3.4"/>',
    "hammer": '<rect x="3.2" y="4" width="14.4" height="6.6" rx="2.2"/>'
              '<path d="M17.6 5.8h1.6a1.6 1.6 0 0 1 1.6 1.6v0a1.6 1.6 0 0 1-1.6 1.6h-1.6"/>'
              '<path d="M10.4 10.6v9.8"/><path d="M7.6 20.4h5.6"/>',
    "rocket": '<path d="M12 2.4c3.1 2.6 4.7 6.2 4.7 9.8L12 16.4l-4.7-4.2c0-3.6 1.6-7.2 4.7-9.8z"/>'
              '<circle cx="12" cy="9.6" r="1.8"/>'
              '<path d="m9.2 15.6-2.6 5.8 4.2-1.6"/>'
              '<path d="m14.8 15.6 2.6 5.8-4.2-1.6"/>',
    "calendar": '<rect x="3.4" y="5" width="17.2" height="15.6" rx="2.6"/>'
                '<path d="M8 2.8v4.2"/><path d="M16 2.8v4.2"/>'
                '<path d="M3.4 10.2h17.2"/>',
    "calendar-check": '<rect x="3.4" y="5" width="17.2" height="15.6" rx="2.6"/>'
                      '<path d="M8 2.8v4.2"/><path d="M16 2.8v4.2"/>'
                      '<path d="M3.4 10.2h17.2"/><path d="m9.2 14.8 2 2 3.6-3.7"/>',

    # ── interface ─────────────────────────────────────────────────────
    "check": '<path d="m4.6 12.6 5 5 9.8-11"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8 12.2 2.8 2.8 5.2-5.5"/>',
    "x-circle": '<circle cx="12" cy="12" r="9"/><path d="m9.2 9.2 5.6 5.6"/><path d="m14.8 9.2-5.6 5.6"/>',
    "lightbulb": '<path d="M9.2 18.2h5.6"/><path d="M10.4 21h3.2"/>'
                 '<path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2v.3h5v-.3c0-.8.4-1.5 1-2A6 6 0 0 0 12 3z"/>',
    "eye": '<path d="M2.4 12S6 5.6 12 5.6 21.6 12 21.6 12 18 18.4 12 18.4 2.4 12 2.4 12z"/>'
           '<circle cx="12" cy="12" r="3"/>',
    "play": '<path d="M7.4 4.6v14.8L19.4 12z"/>',
    "book": '<path d="M12 7A4.6 4.6 0 0 0 7.4 4.4H2.8v13.4h4.6A4.6 4.6 0 0 1 12 20.4"/>'
            '<path d="M12 7a4.6 4.6 0 0 1 4.6-2.6h4.6v13.4h-4.6A4.6 4.6 0 0 0 12 20.4"/>'
            '<path d="M12 7v13.4"/>',
    "code": '<path d="m8 7.2-5 4.8 5 4.8"/><path d="m16 7.2 5 4.8-5 4.8"/>'
            '<path d="m13.6 3.8-3.2 16.4"/>',
    "brain": '<path d="M12 4.6a3.6 3.6 0 0 0-6.9 1.2A3.1 3.1 0 0 0 3.8 11a3.1 3.1 0 0 0 1.7 4.7A3.1 3.1 0 0 0 12 19.6z"/>'
             '<path d="M12 4.6a3.6 3.6 0 0 1 6.9 1.2A3.1 3.1 0 0 1 20.2 11a3.1 3.1 0 0 1-1.7 4.7A3.1 3.1 0 0 1 12 19.6z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 6.8v5.5l3.4 2"/>',
    "moon": '<path d="M20.2 14.6A8.6 8.6 0 0 1 9.4 3.8a8.6 8.6 0 1 0 10.8 10.8z"/>',
    "sun": '<circle cx="12" cy="12" r="4.2"/>'
           '<path d="M12 1.8v2.4"/><path d="M12 19.8v2.4"/>'
           '<path d="M1.8 12h2.4"/><path d="M19.8 12h2.4"/>'
           '<path d="m4.9 4.9 1.7 1.7"/><path d="m17.4 17.4 1.7 1.7"/>'
           '<path d="m19.1 4.9-1.7 1.7"/><path d="m6.6 17.4-1.7 1.7"/>',
    "target": '<circle cx="12" cy="12" r="8.6"/><circle cx="12" cy="12" r="4.8"/>'
              '<circle cx="12" cy="12" r="1.3"/>',
    "film": '<rect x="2.8" y="4.4" width="18.4" height="15.2" rx="2.6"/>'
            '<path d="M8 4.4v15.2"/><path d="M16 4.4v15.2"/><path d="M2.8 12h18.4"/>',
    "pencil": '<path d="M16.6 3.4 20.6 7.4 8.2 19.8H4.2v-4z"/><path d="m14.6 5.4 4 4"/>',
    "help": '<circle cx="12" cy="12" r="9"/>'
            '<path d="M9.5 9.4a2.6 2.6 0 0 1 5 .9c0 1.7-2.5 2.2-2.5 3.8"/>'
            '<path d="M12 17.6h.01"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3.3 9.4h17.4"/><path d="M3.3 14.6h17.4"/>'
             '<path d="M12 3a14.2 14.2 0 0 0 0 18 14.2 14.2 0 0 0 0-18z"/>',
    "alert": '<path d="M12 4.2 2.9 19.6h18.2z"/><path d="M12 10.2v4"/><path d="M12 17h.01"/>',
    "gem": '<path d="M6.2 3.6h11.6l3.4 5.4L12 20.4 2.8 9z"/><path d="M2.8 9h18.4"/>'
           '<path d="m9 3.6-1.4 5.4L12 20.4"/><path d="m15 3.6 1.4 5.4L12 20.4"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>',
    "lock": '<rect x="4.4" y="10.2" width="15.2" height="10.4" rx="2.6"/>'
            '<path d="M8 10.2V7a4 4 0 0 1 8 0v3.2"/>',
    "unlock": '<rect x="4.4" y="10.2" width="15.2" height="10.4" rx="2.6"/>'
              '<path d="M8 10.2V7a4 4 0 0 1 7.5-2"/>',
    "sparkles": '<path d="m10 2.6 1.8 4.6 4.6 1.8-4.6 1.8L10 15.4 8.2 10.8 3.6 9l4.6-1.8z"/>'
                '<path d="m18 14.2.9 2.3 2.3.9-2.3.9-.9 2.3-.9-2.3-2.3-.9 2.3-.9z"/>',
    "arrow-right": '<path d="M4.4 12h15.2"/><path d="m13 5.4 6.6 6.6L13 18.6"/>',
    "arrow-left": '<path d="M19.6 12H4.4"/><path d="m11 5.4-6.6 6.6L11 18.6"/>',
    "arrow-up": '<path d="M12 19.6V4.4"/><path d="m5.4 11 6.6-6.6L18.6 11"/>',
    "beaker": '<path d="M9 2.8v6.6L3.9 17.9A2.1 2.1 0 0 0 5.7 21h12.6a2.1 2.1 0 0 0 1.8-3.1L15 9.4V2.8"/>'
              '<path d="M7.4 2.8h9.2"/><path d="M6.6 14.6h10.8"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11.2v5.4"/><path d="M12 7.8h.01"/>',
    "users": '<circle cx="9.2" cy="8" r="3.6"/>'
             '<path d="M2.6 20a6.6 6.6 0 0 1 13.2 0"/>'
             '<path d="M16.6 5.2a3.6 3.6 0 0 1 0 5.6"/>'
             '<path d="M18.4 20a6.6 6.6 0 0 0-1.8-4.6"/>',
    "refresh": '<path d="M20.6 12a8.6 8.6 0 1 1-2.6-6.1"/><path d="M19.4 2.8v3.8h-3.8"/>',
    "folder": '<path d="M3 6.6A2.2 2.2 0 0 1 5.2 4.4h3.6l2.2 2.6h7.8A2.2 2.2 0 0 1 21 9.2v8.2a2.2 2.2 0 0 1-2.2 2.2H5.2A2.2 2.2 0 0 1 3 17.4z"/>',
    "blocks": '<rect x="3.2" y="3.2" width="7.8" height="7.8" rx="1.9"/>'
              '<rect x="13" y="3.2" width="7.8" height="7.8" rx="1.9"/>'
              '<rect x="3.2" y="13" width="7.8" height="7.8" rx="1.9"/>'
              '<path d="M16.9 13v7.8"/><path d="M13 16.9h7.8"/>',
    "dot": '<circle cx="12" cy="12" r="3.4"/>',
}


def icon_names():
    """Sorted icon names — used by the sprite template."""
    return sorted(ICONS)
