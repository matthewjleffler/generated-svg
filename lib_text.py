from lib import draw_path, draw_circ, draw_rect, Group


###
### Text Drawing
###


# Letter sizes
_let_h = 50
_let_h_half = _let_h / 2
_let_h_quart = _let_h / 4
_let_h_fifth = _let_h / 5
_let_h_eight = _let_h / 8
_let_h_sixt = _let_h / 16

_line_height = _let_h + _let_h_quart + _let_h_eight


def text_letter_height() -> float:
  return _let_h

def text_letter_width() -> float:
  return _let_h_half

def text_line_height() -> float:
  return _line_height


def _letter_cap_a(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}l{} {}M{} {}h{}"
    .format(x, y, _let_h_quart, -_let_h, _let_h_quart, _let_h, x + _let_h_eight, y-_let_h_half, _let_h_quart), group)

def _letter_cap_b(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}m{} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, -_let_h, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, _let_h_quart, 0,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart), group)

def _letter_cap_c(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + _let_h_half, y, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            -_let_h_half,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart), group)

def _letter_cap_d(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}h{}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x, y, -_let_h, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            _let_h_half,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart), group)

def _letter_cap_e(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}v{}h{}m{} {}h{}"
    .format(x + _let_h_half, y, -_let_h_half, -_let_h, _let_h_half, -_let_h_half, _let_h_half, _let_h_quart), group)

def _letter_cap_f(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}h{}m{} {}h{}"
    .format(x, y, -_let_h, _let_h_half, -_let_h_half, _let_h_half, _let_h_quart), group)

def _letter_cap_g(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}v{} q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + _let_h_quart, y - _let_h_half, _let_h_quart, _let_h_quart,
            0, _let_h_quart,  -_let_h_quart, _let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            -_let_h_half,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart), group)

def _letter_cap_h(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}v{}m{} {}h{}"
    .format(x, y, -_let_h, _let_h_half, 0, _let_h, 0, -_let_h_half, -_let_h_half), group)

def _letter_cap_i(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}m{} {}v{}m{} {}h{}"
    .format(x, y, _let_h_half, -_let_h_quart, 0, -_let_h, -_let_h_quart, 0, _let_h_half), group)

def _letter_cap_j(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + _let_h_half, y - _let_h, _let_h_half + _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart), group)

def _letter_cap_k(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}l{} {}l{} {}"
    .format(x, y, -_let_h, _let_h_half, 0, -_let_h_half, _let_h_half, _let_h_half, _let_h_half), group)

def _letter_cap_l(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}h{}"
    .format(x, y - _let_h, _let_h, _let_h_half), group)

def _letter_cap_m(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}l{} {}l{} {}v{}"
    .format(x, y, -_let_h, _let_h_quart, _let_h, _let_h_quart, -_let_h, _let_h), group)

def _letter_cap_n(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}l{} {}v{}"
    .format(x, y, -_let_h, _let_h_half, _let_h, -_let_h), group)

def _letter_cap_o(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}"
    .format(x + _let_h_quart, y,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            -_let_h_half,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            _let_h_half,
            0, _let_h_quart, -_let_h_quart, _let_h_quart), group)

def _letter_cap_p(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, -_let_h, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart), group)

def _letter_cap_q(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}m{} {}l{} {}"
    .format(x + _let_h_quart, y,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            -_let_h_half,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            _let_h_half,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            0, -_let_h_quart, _let_h_quart, _let_h_quart), group)

def _letter_cap_r(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}l{} {}"
    .format(x, y, -_let_h, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, _let_h_half, _let_h_half), group)

def _letter_cap_s(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart, _let_h_quart), group)

def _letter_cap_t(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}h{}"
    .format(x + _let_h_quart, y, -_let_h, -_let_h_quart, 0, _let_h_half), group)

def _letter_cap_u(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y - _let_h, _let_h_half + _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            -_let_h_half - _let_h_quart), group)

def _letter_cap_v(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}l{} {}"
    .format(x, y - _let_h, _let_h_quart, _let_h, _let_h_quart, -_let_h), group)

def _letter_cap_w(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}l{} {}l{} {}l{} {}"
    .format(x, y - _let_h,
            _let_h_eight, _let_h,
            _let_h_eight, -_let_h_half,
            _let_h_eight, _let_h_half,
            _let_h_eight, -_let_h), group)

def _letter_cap_x(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}m{} {}l{} {}"
    .format(x, y - _let_h, _let_h_half, _let_h, 0, -_let_h, -_let_h_half, _let_h), group)

def _letter_cap_y(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}l{} {}m{} {}v{}"
    .format(x, y - _let_h, _let_h_quart, _let_h_half, _let_h_quart, -_let_h_half,
            -_let_h_quart, _let_h_half, _let_h_half), group)

def _letter_cap_z(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}l{} {}h{}"
    .format(x + _let_h_half, y, -_let_h_half, _let_h_half, -_let_h, -_let_h_half), group)

def _letter_low_a(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}m{} {}v{}q{} {} {} {}h{}"
    .format(x + _let_h_half, y - _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_half + _let_h_eight,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_eight), group)

def _letter_low_b(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x, y, -_let_h, x, y - _let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart), group)

def _letter_low_c(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + _let_h_half, y, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart), group)

def _letter_low_d(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + _let_h_half, y, -_let_h, x + _let_h_half, y - _let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart), group)

def _letter_low_e(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y - _let_h_quart, _let_h_half,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart), group)

def _letter_low_f(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}q{} {} {} {}m{} {}h{}"
    .format(x + _let_h_quart, y, -_let_h_half - _let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            -_let_h_half, _let_h_half, _let_h_half), group)

def _letter_low_g(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}m{} {}v{}q{} {} {} {}h{}"
    .format(x + _let_h_half, y - _let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, -_let_h_quart,
            _let_h_half,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart), group)

def _letter_low_h(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y - _let_h, _let_h, 0, -_let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            _let_h_quart), group)

def _letter_low_i(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}v{}"
    .format(x + _let_h_quart, y, -_let_h_half, 0, -_let_h_quart, -_let_h_eight), group)

def _letter_low_j(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}v{}q{} {} {} {}h{}"
    .format(x + _let_h_quart, y - _let_h_half - _let_h_quart - _let_h_eight, _let_h_eight, 0, _let_h_quart, _let_h_half,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_eight), group)

def _letter_low_k(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}l{} {}l{} {}"
    .format(x, y - _let_h, _let_h, _let_h_half, -_let_h_half,
            -_let_h_half, _let_h_quart, _let_h_half, _let_h_quart), group)

def _letter_low_l(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}".format(x + _let_h_quart, y, -_let_h), group)

def _letter_low_m(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}q{} {} {} {}q{} {} {} {}v{}m{} {}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y, -_let_h_half, 0, _let_h_eight,
            0, -_let_h_eight, _let_h_eight, -_let_h_eight,
            _let_h_eight, 0, _let_h_eight, _let_h_eight,
            _let_h_eight, 0, -_let_h_eight,
            0, -_let_h_eight, _let_h_eight, -_let_h_eight,
            _let_h_eight, 0, _let_h_eight, _let_h_eight,
            _let_h_quart + _let_h_eight), group)

def _letter_low_n(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y, -_let_h_half, 0, _let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            _let_h_quart), group)

def _letter_low_o(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + _let_h_quart, y,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart), group)

def _letter_low_p(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}m{} {}v{}"
    .format(x, y - _let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            0, -_let_h_quart, _let_h_half + _let_h_quart), group)

def _letter_low_q(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}m{} {}v{}"
    .format(x + _let_h_half, y - _let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, -_let_h_quart, _let_h_half + _let_h_quart), group)

def _letter_low_r(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}q{} {} {} {}q{} {} {} {}"
    .format(x, y, -_let_h_half, 0, _let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart), group)

def _letter_low_s(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}q{} {} {} {}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, _let_h_quart + _let_h_eight,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight,
            0, -_let_h_eight, -_let_h_eight, -_let_h_eight,
            -_let_h_quart,
            -_let_h_eight, 0, -_let_h_eight, -_let_h_eight,
            0, -_let_h_eight, _let_h_eight, -_let_h_eight,
            _let_h_quart + _let_h_eight), group)

def _letter_low_t(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}h{}"
    .format(x + _let_h_quart, y, -_let_h_half - _let_h_quart,
            -_let_h_quart, _let_h_quart, _let_h_half), group)

def _letter_low_u(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}q{} {} {} {}q{} {} {} {}m{} {}v{}"
    .format(x, y - _let_h_half, _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, _let_h_quart, -_let_h_half), group)

def _letter_low_v(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}l{} {}"
    .format(x, y - _let_h_half, _let_h_quart, _let_h_half, _let_h_quart, -_let_h_half), group)

def _letter_low_w(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}q{} {} {} {}q{} {} {} {}v{}m{} {}q{} {} {} {}q{} {} {} {}m{} {}v{}"
    .format(x, y - _let_h_half, _let_h_quart + _let_h_eight,
            0, _let_h_eight, _let_h_eight, _let_h_eight,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight,
            -_let_h_eight, 0, _let_h_eight,
            0, _let_h_eight, _let_h_eight, _let_h_eight,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight,
            0, -_let_h_quart - _let_h_eight, _let_h_half), group)

def _letter_low_x(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}m{} {}l{} {}"
    .format(x, y-_let_h_half, _let_h_half, _let_h_half, 0, -_let_h_half, -_let_h_half, _let_h_half), group)

def _letter_low_y(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}m{} {}l{} {}"
    .format(x, y - _let_h_half, _let_h_quart, _let_h_half, _let_h_quart, -_let_h_half, -_let_h_half + _let_h_eight, _let_h_half + _let_h_quart), group)

def _letter_low_z(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}l{} {}h{}"
    .format(x + _let_h_half, y, -_let_h_half, _let_h_half, -_let_h_half, -_let_h_half), group)

def _number_0(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}m{} {}l{} {}"
    .format(x + _let_h_quart, y,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            -_let_h_half,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            _let_h_half,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, -_let_h_quart, _let_h_half, -_let_h_half), group)

def _number_1(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}m{} {}v{}l{} {}"
    .format(x, y, _let_h_half, -_let_h_quart, 0, -_let_h, -_let_h_quart, _let_h_quart), group)

def _number_2(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + _let_h_half, y, -_let_h_half, -_let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart), group)

def _number_3(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}q{} {} {} {}h{}m{} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_eight, _let_h_eight, 0,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart), group)

def _number_4(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}h{}m{} {}v{}"
    .format(x, y - _let_h, _let_h_half, _let_h_half, 0, _let_h_half, -_let_h), group)

def _number_5(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}v{}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + _let_h_half, y - _let_h, -_let_h_half, _let_h_half, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart), group)

def _number_6(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + _let_h_half, y - _let_h, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart,
            _let_h_half,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart), group)

def _number_7(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}l{} {}"
    .format(x, y - _let_h, _let_h_half, -_let_h_half, _let_h), group)

def _number_8(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + _let_h_quart, y - _let_h,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart), group)

def _number_9(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_quart,
            -_let_h_half,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart), group)

def _punc_exclamation(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}v{}"
    .format(x + _let_h_quart, y - _let_h, _let_h_half + _let_h_eight, 0, _let_h_quart, _let_h_eight), group)

def _punc_at(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + _let_h_quart, y,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            -_let_h_half,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_quart, 0, _let_h_quart, _let_h_quart,
            _let_h_half,
            -_let_h_sixt, _let_h_eight, -_let_h_eight, 0,
            -_let_h_quart - _let_h_eight,
            0, -_let_h_eight, -_let_h_eight, -_let_h_eight,
            -_let_h_eight, 0, -_let_h_eight, _let_h_eight,
            _let_h_quart,
            0, _let_h_eight, _let_h_eight, _let_h_eight,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight), group)

def _punc_pound(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}v{}M{} {}h{}m{} {}h{}"
    .format(x + _let_h_eight, y, -_let_h, _let_h_quart, 0, _let_h,
            x, y - _let_h_quart, _let_h_half, 0, -_let_h_half, -_let_h_half), group)

def _punc_dollar(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}M{} {}v{}"
    .format(x, y - (_let_h_fifth / 2), _let_h_quart,
            _let_h_quart, 0, _let_h_quart, -_let_h_fifth,
            0, -_let_h_fifth, -_let_h_quart, -_let_h_fifth,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_fifth,
            0, -_let_h_fifth, _let_h_quart, -_let_h_fifth,
            _let_h_quart, x + _let_h_quart, y, -_let_h), group)

def _punc_percent(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}"
    .format(x, y, _let_h_half, -_let_h), group)
  draw_circ(x + _let_h_eight, y - _let_h + _let_h_eight, _let_h_eight, group)
  draw_circ(x + _let_h_eight + _let_h_quart, y - _let_h_eight, _let_h_eight, group)

def _punc_carrot(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}l{} {}"
    .format(x, y - _let_h + _let_h_quart, _let_h_quart, -_let_h_quart, _let_h_quart, _let_h_quart), group)

def _punc_and(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}L{} {}"
    .format(x + _let_h_half, y - _let_h_half, _let_h_quart,
            0, _let_h_quart, -_let_h_quart, _let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, -_let_h_quart,
            -_let_h_eight,
            0, -_let_h_quart, _let_h_quart, -_let_h_quart,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight,
            -_let_h_eight,
            0, -_let_h_eight, -_let_h_eight, -_let_h_eight,
            -_let_h_eight, 0, -_let_h_eight, _let_h_eight,
            _let_h_eight,
            x + _let_h_half, y), group)

def _punc_star(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}l{} {}m{} {}l{} {}"
    .format(x + _let_h_quart, y - _let_h_quart + _let_h_eight, -_let_h_half -_let_h_quart,
            -_let_h_quart, _let_h_eight, _let_h_half, _let_h_half, 0,
            -_let_h_half, -_let_h_half, _let_h_half), group)

def _punc_left_paren(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}"
    .format(x + _let_h_half - _let_h_eight, y, -_let_h_half, -_let_h_half, 0, -_let_h), group)

def _punc_right_paren(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}"
    .format(x + _let_h_eight, y, _let_h_half, -_let_h_half, 0, -_let_h), group)

def _punc_dash(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}".format(x, y - _let_h_half, _let_h_half), group)

def _punc_underscore(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}".format(x, y, _let_h_half), group)

def _punc_plus(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}m{} {}v{}"
    .format(x, y - _let_h_half, _let_h_half, -_let_h_quart, -_let_h_quart, _let_h_half), group)

def _punc_equals(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}m{} {}h{}"
    .format(x, y - _let_h_half + _let_h_eight, _let_h_half, 0, -_let_h_quart, -_let_h_half), group)

def _punc_left_brace(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + _let_h_quart + _let_h_eight, y, -_let_h_eight,
            -_let_h_eight, 0, -_let_h_eight, -_let_h_eight,
            -_let_h_quart,
            0, -_let_h_eight, -_let_h_eight, -_let_h_eight,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight,
            -_let_h_quart,
            0, -_let_h_eight, _let_h_eight, -_let_h_eight,
            _let_h_eight), group)

def _punc_right_brace(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + _let_h_quart - _let_h_eight, y, _let_h_eight,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight,
            -_let_h_quart,
            0, -_let_h_eight, _let_h_eight, -_let_h_eight,
            -_let_h_eight, 0, -_let_h_eight, -_let_h_eight,
            -_let_h_quart,
            0, -_let_h_eight, -_let_h_eight, -_let_h_eight,
            -_let_h_eight), group)

def _punc_left_bracket(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}v{}h{}"
    .format(x + _let_h_quart + _let_h_eight, y, -_let_h_quart, -_let_h, _let_h_quart), group)

def _punc_right_bracket(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}v{}h{}"
    .format(x + _let_h_quart - _let_h_eight, y, +_let_h_quart, -_let_h, -_let_h_quart), group)

def _punc_backslash(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}"
    .format(x, y - _let_h, _let_h_half, _let_h), group)

def _punc_line(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}"
    .format(x + _let_h_quart, y, -_let_h), group)

def _punc_comma(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}v{}"
    .format(x + _let_h_quart - _let_h_eight, y,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight, -_let_h_eight), group)

def _punc_period(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}".format(x + _let_h_quart, y, -_let_h_eight), group)

def _punc_slash(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}".format(x, y, _let_h_half, -_let_h), group)

def _punc_left_arrow(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}l{} {}"
    .format(x + _let_h_quart + _let_h_eight, y - _let_h_half + _let_h_quart,
            -_let_h_quart, -_let_h_quart, _let_h_quart, -_let_h_quart), group)

def _punc_right_arrow(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}l{} {}"
    .format(x + _let_h_quart - _let_h_eight, y - _let_h_half + _let_h_quart,
            _let_h_quart, -_let_h_quart, -_let_h_quart, -_let_h_quart), group)

def _punc_question(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}q{} {} {} {}v{}"
    .format(x + _let_h_quart, y, -_let_h_eight, 0, -_let_h_quart, -_let_h_eight,
            0, -_let_h_eight, _let_h_eight, -_let_h_eight,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight,
            -_let_h_eight,
            0, -_let_h_eight, -_let_h_eight, -_let_h_eight,
            -_let_h_quart,
            -_let_h_eight, 0, -_let_h_eight, _let_h_eight,
            _let_h_eight), group)

def _punc_semicolon(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}v{}m{} {}v{}"
    .format(x + _let_h_quart - _let_h_eight, y,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight, -_let_h_eight,
            0, -_let_h_quart, -_let_h_eight), group)

def _punc_colon(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}v{}"
    .format(x + _let_h_quart, y - _let_h_quart, -_let_h_eight, 0, -_let_h_quart, -_let_h_eight), group)

def _punc_single_quote(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}".format(x + _let_h_quart, y - _let_h + _let_h_eight, _let_h_eight), group)

def _punc_double_quote(x:float, y:float, group:Group = None):
  draw_path("M{} {}v{}m{} {}v{}"
    .format(x + _let_h_quart - _let_h_sixt, y - _let_h + _let_h_eight, _let_h_eight, _let_h_eight, 0, -_let_h_eight), group)

def _punc_back_tick(x:float, y:float, group:Group = None):
  draw_path("M{} {}l{} {}"
    .format(x + _let_h_eight, y-_let_h, _let_h_quart, _let_h_quart), group)

def _punc_tilde(x:float, y:float, group:Group = None):
  draw_path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x, y - _let_h_half,
            0, -_let_h_eight, _let_h_eight, -_let_h_eight,
            _let_h_eight, 0, _let_h_eight, _let_h_eight,
            0, _let_h_eight, _let_h_eight, _let_h_eight,
            _let_h_eight, 0, _let_h_eight, -_let_h_eight), group)

def _letter_low_e_accent(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}M{} {}l{} {}"
    .format(x, y - _let_h_quart, _let_h_half,
            0, -_let_h_quart, -_let_h_quart, -_let_h_quart,
            -_let_h_quart, 0, -_let_h_quart, _let_h_quart,
            0, _let_h_quart, _let_h_quart, _let_h_quart,
            _let_h_quart - _let_h_eight, x + _let_h_eight, y - _let_h_half - _let_h_eight,
            _let_h_quart, -_let_h_quart), group)

def _letter_cap_e_accent(x:float, y:float, group:Group = None):
  draw_path("M{} {}h{}v{}h{}m{} {}h{}M{} {}l{} {}"
    .format(x + _let_h_half, y, -_let_h_half, -_let_h,
            _let_h_half, -_let_h_half, _let_h_half, _let_h_quart,
            x + _let_h_eight, y - _let_h - _let_h_eight,
            _let_h_quart, -_let_h_quart), group)

def draw_text(x:float, y:float, kern:float, value:str, group:Group = None):
  for char in value:
    # draw_rect(x, y - _let_h, _let_h_half, _let_h, group)
    # draw_path(f"M{x} {y - _let_h_half}h{_let_h_half}", group)
    # draw_path(f"M{x} {y + _let_h_quart}h{_let_h_half}", group)

    if char == " ":   pass
    elif char == "A": _letter_cap_a(x, y, group)
    elif char == "B": _letter_cap_b(x, y, group)
    elif char == "C": _letter_cap_c(x, y, group)
    elif char == "D": _letter_cap_d(x, y, group)
    elif char == "E": _letter_cap_e(x, y, group)
    elif char == "F": _letter_cap_f(x, y, group)
    elif char == "G": _letter_cap_g(x, y, group)
    elif char == "H": _letter_cap_h(x, y, group)
    elif char == "I": _letter_cap_i(x, y, group)
    elif char == "J": _letter_cap_j(x, y, group)
    elif char == "K": _letter_cap_k(x, y, group)
    elif char == "L": _letter_cap_l(x, y, group)
    elif char == "M": _letter_cap_m(x, y, group)
    elif char == "N": _letter_cap_n(x, y, group)
    elif char == "O": _letter_cap_o(x, y, group)
    elif char == "P": _letter_cap_p(x, y, group)
    elif char == "Q": _letter_cap_q(x, y, group)
    elif char == "R": _letter_cap_r(x, y, group)
    elif char == "S": _letter_cap_s(x, y, group)
    elif char == "T": _letter_cap_t(x, y, group)
    elif char == "U": _letter_cap_u(x, y, group)
    elif char == "V": _letter_cap_v(x, y, group)
    elif char == "W": _letter_cap_w(x, y, group)
    elif char == "X": _letter_cap_x(x, y, group)
    elif char == "Y": _letter_cap_y(x, y, group)
    elif char == "Z": _letter_cap_z(x, y, group)
    elif char == "a": _letter_low_a(x, y, group)
    elif char == "b": _letter_low_b(x, y, group)
    elif char == "c": _letter_low_c(x, y, group)
    elif char == "d": _letter_low_d(x, y, group)
    elif char == "e": _letter_low_e(x, y, group)
    elif char == "f": _letter_low_f(x, y, group)
    elif char == "g": _letter_low_g(x, y, group)
    elif char == "h": _letter_low_h(x, y, group)
    elif char == "i": _letter_low_i(x, y, group)
    elif char == "j": _letter_low_j(x, y, group)
    elif char == "k": _letter_low_k(x, y, group)
    elif char == "l": _letter_low_l(x, y, group)
    elif char == "m": _letter_low_m(x, y, group)
    elif char == "n": _letter_low_n(x, y, group)
    elif char == "o": _letter_low_o(x, y, group)
    elif char == "p": _letter_low_p(x, y, group)
    elif char == "q": _letter_low_q(x, y, group)
    elif char == "r": _letter_low_r(x, y, group)
    elif char == "s": _letter_low_s(x, y, group)
    elif char == "t": _letter_low_t(x, y, group)
    elif char == "u": _letter_low_u(x, y, group)
    elif char == "v": _letter_low_v(x, y, group)
    elif char == "w": _letter_low_w(x, y, group)
    elif char == "x": _letter_low_x(x, y, group)
    elif char == "y": _letter_low_y(x, y, group)
    elif char == "z": _letter_low_z(x, y, group)
    elif char == "0": _number_0(x, y, group)
    elif char == "1": _number_1(x, y, group)
    elif char == "2": _number_2(x, y, group)
    elif char == "3": _number_3(x, y, group)
    elif char == "4": _number_4(x, y, group)
    elif char == "5": _number_5(x, y, group)
    elif char == "6": _number_6(x, y, group)
    elif char == "7": _number_7(x, y, group)
    elif char == "8": _number_8(x, y, group)
    elif char == "9": _number_9(x, y, group)
    elif char == "!": _punc_exclamation(x, y, group)
    elif char == "@": _punc_at(x, y, group)
    elif char == "#": _punc_pound(x, y, group)
    elif char == "$": _punc_dollar(x, y, group)
    elif char == "%": _punc_percent(x, y, group)
    elif char == "^": _punc_carrot(x, y, group)
    elif char == "&": _punc_and(x, y, group)
    elif char == "*": _punc_star(x, y, group)
    elif char == "(": _punc_left_paren(x, y, group)
    elif char == ")": _punc_right_paren(x, y, group)
    elif char == "-" or char == "—": _punc_dash(x, y, group)
    elif char == "_": _punc_underscore(x, y, group)
    elif char == "+": _punc_plus(x, y, group)
    elif char == "=": _punc_equals(x, y, group)
    elif char == "{": _punc_left_brace(x, y, group)
    elif char == "}": _punc_right_brace(x, y, group)
    elif char == "[": _punc_left_bracket(x, y, group)
    elif char == "]": _punc_right_bracket(x, y, group)
    elif char == "\\": _punc_backslash(x, y, group)
    elif char == "|": _punc_line(x, y, group)
    elif char == ",": _punc_comma(x, y, group)
    elif char == ".": _punc_period(x, y, group)
    elif char == "/": _punc_slash(x, y, group)
    elif char == "<": _punc_left_arrow(x, y, group)
    elif char == ">": _punc_right_arrow(x, y, group)
    elif char == "?": _punc_question(x, y, group)
    elif char == ";": _punc_semicolon(x, y, group)
    elif char == ":": _punc_colon(x, y, group)
    elif char == "'" or char == "’" or char == "‘":
      _punc_single_quote(x, y, group)
    elif char == "\"" or char == "“" or char == "”":
      _punc_double_quote(x, y, group)
    elif char == "`": _punc_back_tick(x, y, group)
    elif char == "~": _punc_tilde(x, y, group)
    elif char == "é": _letter_low_e_accent(x, y, group)
    elif char == "É": _letter_cap_e_accent(x, y, group)
    else: print("Unhandled character: {}".format(char))
    x += _let_h_half + kern

