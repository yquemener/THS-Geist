def RenderText(screen, text, xy=[0,0], style={}):
    _xy=xy
    if "font" in style.keys():
        _font = style["font"]
    else:
        _font = pygame.font.Font(None, 36)
    if "bold" in style.keys():
        _font.set_bold(True)
    else:
        _font.set_bold(False)

    for l in text.split("\n"):
        ts = _font.render(l, 1, (255,255,255))
        if 'align-center' in style.keys():
            _xy[0]=ts.get_rect(centerx=screen.get_width()/2)[0]
        else:
            _xy[0] = xy[0]
        screen.blit(ts, xy)
        _xy[1] += ts.get_height()
    return _xy
