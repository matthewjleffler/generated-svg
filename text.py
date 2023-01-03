import lib

# Letter sizes
let_h = 50
let_h_half = let_h / 2
let_h_quart = let_h / 4
let_h_fifth = let_h / 5
let_h_eight = let_h / 8
let_h_sixt = let_h / 16

def letter_a(x, y) -> float:
  lib.path("M{} {}l{} {}l{} {}M{} {}h{}"
    .format(x, y, let_h_quart, -let_h, let_h_quart, let_h, x + let_h_eight, y-let_h_half, let_h_quart))
  return let_h_half

def letter_b(x, y) -> float:
  lib.path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}m{} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, let_h_quart, 0,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))
  return let_h_half

def letter_c(x, y) -> float:
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_half, y, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart))
  return let_h_half

def letter_d(x, y) -> float:
  lib.path("M{} {}v{}h{}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))
  return let_h_half

def letter_e(x, y) -> float:
  lib.path("M{} {}h{}v{}h{}m{} {}h{}"
    .format(x + let_h_half, y, -let_h_half, -let_h, let_h_half, -let_h_half, let_h_half, let_h_quart))
  return let_h_half

def letter_f(x, y) -> float:
  lib.path("M{} {}v{}h{}m{} {}h{}"
    .format(x, y, -let_h, let_h_half, -let_h_half, let_h_half, let_h_quart))
  return let_h_half

# TODO
def letter_g(x, y) -> float:
  lib.path("M{} {}h{}v{} q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_quart, y - let_h_half, let_h_quart, let_h_quart,
            0, let_h_quart,  -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart))
  return let_h_half

def letter_h(x, y) -> float:
  lib.path("M{} {}v{}m{} {}v{}m{} {}h{}"
    .format(x, y, -let_h, let_h_half, 0, let_h, 0, -let_h_half, -let_h_half))
  return let_h_half

def letter_i(x, y) -> float:
  lib.path("M{} {}h{}m{} {}v{}m{} {}h{}"
    .format(x, y, let_h_half, -let_h_quart, 0, -let_h, -let_h_quart, 0, let_h_half))
  return let_h_half

def letter_j(x, y) -> float:
  lib.path("M{} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_half, y - let_h, let_h_half + let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart))
  return let_h_half

def letter_k(x, y) -> float:
  lib.path("M{} {}v{}m{} {}l{} {}l{} {}"
    .format(x, y, -let_h, let_h_half, 0, -let_h_half, let_h_half, let_h_half, let_h_half))
  return let_h_half

def letter_l(x, y) -> float:
  lib.path("M{} {}v{}h{}"
    .format(x, y - let_h, let_h, let_h_half))
  return let_h_half

def letter_m(x, y) -> float:
  lib.path("M{} {}v{}l{} {}l{} {}v{}"
    .format(x, y, -let_h, let_h_quart, let_h, let_h_quart, -let_h, let_h))
  return let_h_half

def letter_n(x, y) -> float:
  lib.path("M{} {}v{}l{} {}v{}"
    .format(x, y, -let_h, let_h_half, let_h, -let_h))
  return let_h_half

def letter_o(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart))
  return let_h_half

def letter_p(x, y) -> float:
  lib.path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))
  return let_h_half

def letter_q(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}m{} {}l{} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            0, -let_h_quart, let_h_quart, let_h_quart))
  return let_h_half

def letter_r(x, y) -> float:
  lib.path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}l{} {}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, let_h_half, let_h_half))
  return let_h_half

def letter_s(x, y) -> float:
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart, let_h_quart))
  return let_h_half

def letter_t(x, y) -> float:
  lib.path("M{} {}v{}m{} {}h{}"
    .format(x + let_h_quart, y, -let_h, -let_h_quart, 0, let_h_half))
  return let_h_half

def letter_u(x, y) -> float:
  lib.path("M{} {}v{}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y - let_h, let_h_half + let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            -let_h_half - let_h_quart))
  return let_h_half

def letter_v(x, y) -> float:
  lib.path("M{} {}l{} {}l{} {}"
    .format(x, y - let_h, let_h_quart, let_h, let_h_quart, -let_h))
  return let_h_half

def letter_w(x, y) -> float:
  lib.path("M{} {}l{} {}l{} {}l{} {}l{} {}"
    .format(x, y - let_h,
            let_h_eight, let_h,
            let_h_eight, -let_h_half,
            let_h_eight, let_h_half,
            let_h_eight, -let_h))
  return let_h_half

def letter_x(x, y) -> float:
  lib.path("M{} {}l{} {}m{} {}l{} {}"
    .format(x, y - let_h, let_h_half, let_h, 0, -let_h, -let_h_half, let_h))
  return let_h_half

def letter_y(x, y) -> float:
  lib.path("M{} {}l{} {}l{} {}m{} {}v{}"
    .format(x, y - let_h, let_h_quart, let_h_half, let_h_quart, -let_h_half,
            -let_h_quart, let_h_half, let_h_half))
  return let_h_half

def letter_z(x, y) -> float:
  lib.path("M{} {}h{}l{} {}h{}"
    .format(x + let_h_half, y, -let_h_half, let_h_half, -let_h, -let_h_half))
  return let_h_half

def number_0(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}m{} {}l{} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, -let_h_quart, let_h_half, -let_h_half))
  return let_h_half

def number_1(x, y) -> float:
  lib.path("M{} {}h{}m{} {}v{}l{} {}"
    .format(x, y, let_h_half, -let_h_quart, 0, -let_h, -let_h_quart, let_h_quart))
  return let_h_half

def number_2(x, y) -> float:
  lib.path("M{} {}h{}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_half, y, -let_h_half, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart))
  return let_h_half

def number_3(x, y) -> float:
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}h{}m{} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_eight, let_h_eight, 0,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart))
  return let_h_half

def number_4(x, y) -> float:
  lib.path("M{} {}v{}h{}m{} {}v{}"
    .format(x, y - let_h, let_h_half, let_h_half, 0, let_h_half, -let_h))
  return let_h_half

def number_5(x, y) -> float:
  lib.path("M{} {}h{}v{}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + let_h_half, y - let_h, -let_h_half, let_h_half, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))
  return let_h_half

def number_6(x, y) -> float:
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + let_h_half, y - let_h, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart))
  return let_h_half

def number_7(x, y) -> float:
  lib.path("M{} {}h{}l{} {}"
    .format(x, y - let_h, let_h_half, -let_h_half, let_h))
  return let_h_half

def number_8(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_quart, y - let_h,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart))
  return let_h_half

def number_9(x, y) -> float:
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart))
  return let_h_half

def punc_exclamation(x, y) -> float:
  lib.path("M{} {}v{}m{} {}v{}"
    .format(x + let_h_quart, y - let_h, let_h_half + let_h_eight, 0, let_h_quart, let_h_eight))
  return let_h_half

def punc_at(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            -let_h_sixt, let_h_eight, -let_h_eight, 0,
            -let_h_quart - let_h_eight,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            -let_h_eight, 0, -let_h_eight, let_h_eight,
            let_h_quart,
            0, let_h_eight, let_h_eight, let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight))
  return let_h_half

def punc_pound(x, y) -> float:
  lib.path("M{} {}v{}m{} {}v{}M{} {}h{}m{} {}h{}"
    .format(x + let_h_eight, y, -let_h, let_h_quart, 0, let_h,
            x, y - let_h_quart, let_h_half, 0, -let_h_half, -let_h_half))
  return let_h_half

def punc_dollar(x, y) -> float:
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}M{} {}v{}"
    .format(x, y - (let_h_fifth / 2), let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_fifth,
            0, -let_h_fifth, -let_h_quart, -let_h_fifth,
            -let_h_quart, 0, -let_h_quart, -let_h_fifth,
            0, -let_h_fifth, let_h_quart, -let_h_fifth,
            let_h_quart, x + let_h_quart, y, -let_h))
  return let_h_half

def punc_percent(x, y) -> float:
  lib.path("M{} {}l{} {}"
    .format(x, y, let_h_half, -let_h))
  lib.circ(x + let_h_eight, y - let_h + let_h_eight, let_h_eight)
  lib.circ(x + let_h_eight + let_h_quart, y - let_h_eight, let_h_eight)
  return let_h_half

def punc_carrot(x, y) -> float:
  lib.path("M{} {}l{} {}l{} {}"
    .format(x, y - let_h + let_h_quart, let_h_quart, -let_h_quart, let_h_quart, let_h_quart))
  return let_h_half

def punc_and(x, y) -> float:
  lib.path("M{} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}L{} {}"
    .format(x + let_h_half, y - let_h_half, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_eight,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            -let_h_eight,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            -let_h_eight, 0, -let_h_eight, let_h_eight,
            let_h_eight,
            x + let_h_half, y))
  return let_h_half

def punc_star(x, y) -> float:
  lib.path("M{} {}v{}m{} {}l{} {}m{} {}l{} {}"
    .format(x + let_h_quart, y - let_h_quart + let_h_eight, -let_h_half -let_h_quart, -let_h_quart, let_h_eight, let_h_half, let_h_half, 0, -let_h_half, -let_h_half, let_h_half))
  return let_h_half

def punc_left_paren(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}"
    .format(x + let_h_half - let_h_eight, y, -let_h_half, -let_h_half, 0, -let_h))
  return let_h_half

def punc_right_paren(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}"
    .format(x + let_h_eight, y, let_h_half, -let_h_half, 0, -let_h))
  return let_h_half

def punc_dash(x, y) -> float:
  lib.path("M{} {}h{}".format(x, y - let_h_half, let_h_half))
  return let_h_half

def punc_underscore(x, y) -> float:
  lib.path("M{} {}h{}".format(x, y, let_h_half))
  return let_h_half

def punc_plus(x, y) -> float:
  lib.path("M{} {}h{}m{} {}v{}"
    .format(x, y - let_h_half, let_h_half, -let_h_quart, -let_h_quart, let_h_half))
  return let_h_half

def punc_equals(x, y) -> float:
  lib.path("M{} {}h{}m{} {}h{}"
    .format(x, y - let_h_half + let_h_eight, let_h_half, 0, -let_h_quart, -let_h_half))
  return let_h_half

def punc_left_brace(x, y) -> float:
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_quart + let_h_eight, y, -let_h_eight,
            -let_h_eight, 0, -let_h_eight, -let_h_eight,
            -let_h_quart,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            -let_h_quart,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            let_h_eight))
  return let_h_half

def punc_right_brace(x, y) -> float:
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_quart - let_h_eight, y, let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            -let_h_quart,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            -let_h_eight, 0, -let_h_eight, -let_h_eight,
            -let_h_quart,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            -let_h_eight))
  return let_h_half

def punc_left_bracket(x, y) -> float:
  lib.path("M{} {}h{}v{}h{}"
    .format(x + let_h_quart + let_h_eight, y, -let_h_quart, -let_h, let_h_quart))
  return let_h_half

def punc_right_bracket(x, y) -> float:
  lib.path("M{} {}h{}v{}h{}"
    .format(x + let_h_quart - let_h_eight, y, +let_h_quart, -let_h, -let_h_quart))
  return let_h_half

def punc_backslash(x, y) -> float:
  lib.path("M{} {}l{} {}"
    .format(x, y - let_h, let_h_half, let_h))
  return let_h_half

def punc_line(x, y) -> float:
  lib.path("M{} {}v{}"
    .format(x + let_h_quart, y, -let_h))
  return let_h_half

def punc_comma(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}v{}"
    .format(x + let_h_quart - let_h_eight, y,
            let_h_eight, 0, let_h_eight, -let_h_eight, -let_h_eight))
  return let_h_half

def punc_period(x, y) -> float:
  lib.path("M{} {}v{}".format(x + let_h_quart, y, -let_h_eight))
  return let_h_half

def punc_slash(x, y) -> float:
  lib.path("M{} {}l{} {}".format(x, y, let_h_half, -let_h))
  return let_h_half

def punc_left_arrow(x, y) -> float:
  lib.path("M{} {}l{} {}l{} {}"
    .format(x + let_h_quart + let_h_eight, y - let_h_half + let_h_quart,
            -let_h_quart, -let_h_quart, let_h_quart, -let_h_quart))
  return let_h_half

def punc_right_arrow(x, y) -> float:
  lib.path("M{} {}l{} {}l{} {}"
    .format(x + let_h_quart - let_h_eight, y - let_h_half + let_h_quart,
            let_h_quart, -let_h_quart, -let_h_quart, -let_h_quart))
  return let_h_half

def punc_question(x, y) -> float:
  lib.path("M{} {}v{}m{} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}q{} {} {} {}v{}"
    .format(x + let_h_quart, y, -let_h_eight, 0, -let_h_quart, -let_h_eight,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            -let_h_eight,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            -let_h_quart,
            -let_h_eight, 0, -let_h_eight, let_h_eight,
            let_h_eight))
  return let_h_half

def punc_semicolon(x, y) -> float:
  lib.path("M{} {}q{} {} {} {}v{}m{} {}v{}"
    .format(x + let_h_quart - let_h_eight, y,
            let_h_eight, 0, let_h_eight, -let_h_eight, -let_h_eight,
            0, -let_h_eight, -let_h_eight))
  return let_h_half

def punc_colon(x, y) -> float:
  lib.path("M{} {}v{}m{} {}v{}"
    .format(x + let_h_quart, y - let_h_quart, -let_h_eight, 0, -let_h_quart, -let_h_eight))
  return let_h_half

def punc_single_quote(x, y) -> float:
  lib.path("M{} {}v{}".format(x + let_h_quart, y - let_h + let_h_eight, let_h_eight))
  return let_h_half

def punc_double_quote(x, y) -> float:
  lib.path("M{} {}v{}m{} {}v{}"
    .format(x + let_h_quart - let_h_sixt, y - let_h + let_h_eight, let_h_eight, let_h_eight, 0, -let_h_eight))
  return let_h_half

def draw_char(x, y, kern, char:callable) -> float:
  # rect(x, y - let_h, let_h_half, let_h)
  return char(x, y) + kern

def draw_string(x, y, kern, value:str):
  value = value.upper()
  for char in value:
    if char == " ":
      x += let_h_half + kern
    elif char == "A":
      x += draw_char(x, y, kern, letter_a)
    elif char == "B":
      x += draw_char(x, y, kern, letter_b)
    elif char == "C":
      x += draw_char(x, y, kern, letter_c)
    elif char == "D":
      x += draw_char(x, y, kern, letter_d)
    elif char == "E":
      x += draw_char(x, y, kern, letter_e)
    elif char == "F":
      x += draw_char(x, y, kern, letter_f)
    elif char == "G":
      x += draw_char(x, y, kern, letter_g)
    elif char == "H":
      x += draw_char(x, y, kern, letter_h)
    elif char == "I":
      x += draw_char(x, y, kern, letter_i)
    elif char == "J":
      x += draw_char(x, y, kern, letter_j)
    elif char == "K":
      x += draw_char(x, y, kern, letter_k)
    elif char == "L":
      x += draw_char(x, y, kern, letter_l)
    elif char == "M":
      x += draw_char(x, y, kern, letter_m)
    elif char == "N":
      x += draw_char(x, y, kern, letter_n)
    elif char == "O":
      x += draw_char(x, y, kern, letter_o)
    elif char == "P":
      x += draw_char(x, y, kern, letter_p)
    elif char == "Q":
      x += draw_char(x, y, kern, letter_q)
    elif char == "R":
      x += draw_char(x, y, kern, letter_r)
    elif char == "S":
      x += draw_char(x, y, kern, letter_s)
    elif char == "T":
      x += draw_char(x, y, kern, letter_t)
    elif char == "U":
      x += draw_char(x, y, kern, letter_u)
    elif char == "V":
      x += draw_char(x, y, kern, letter_v)
    elif char == "W":
      x += draw_char(x, y, kern, letter_w)
    elif char == "X":
      x += draw_char(x, y, kern, letter_x)
    elif char == "Y":
      x += draw_char(x, y, kern, letter_y)
    elif char == "Z":
      x += draw_char(x, y, kern, letter_z)
    elif char == "0":
      x += draw_char(x, y, kern, number_0)
    elif char == "1":
      x += draw_char(x, y, kern, number_1)
    elif char == "2":
      x += draw_char(x, y, kern, number_2)
    elif char == "3":
      x += draw_char(x, y, kern, number_3)
    elif char == "4":
      x += draw_char(x, y, kern, number_4)
    elif char == "5":
      x += draw_char(x, y, kern, number_5)
    elif char == "6":
      x += draw_char(x, y, kern, number_6)
    elif char == "7":
      x += draw_char(x, y, kern, number_7)
    elif char == "8":
      x += draw_char(x, y, kern, number_8)
    elif char == "9":
      x += draw_char(x, y, kern, number_9)
    elif char == "!":
      x += draw_char(x, y, kern, punc_exclamation)
    elif char == "@":
      x += draw_char(x, y, kern, punc_at)
    elif char == "#":
      x += draw_char(x, y, kern, punc_pound)
    elif char == "$":
      x += draw_char(x, y, kern, punc_dollar)
    elif char == "%":
      x += draw_char(x, y, kern, punc_percent)
    elif char == "^":
      x += draw_char(x, y, kern, punc_carrot)
    elif char == "&":
      x += draw_char(x, y, kern, punc_and)
    elif char == "*":
      x += draw_char(x, y, kern, punc_star)
    elif char == "(":
      x += draw_char(x, y, kern, punc_left_paren)
    elif char == ")":
      x += draw_char(x, y, kern, punc_right_paren)
    elif char == "-":
      x += draw_char(x, y, kern, punc_dash)
    elif char == "_":
      x += draw_char(x, y, kern, punc_underscore)
    elif char == "+":
      x += draw_char(x, y, kern, punc_plus)
    elif char == "=":
      x += draw_char(x, y, kern, punc_equals)
    elif char == "{":
      x += draw_char(x, y, kern, punc_left_brace)
    elif char == "}":
      x += draw_char(x, y, kern, punc_right_brace)
    elif char == "[":
      x += draw_char(x, y, kern, punc_left_bracket)
    elif char == "]":
      x += draw_char(x, y, kern, punc_right_bracket)
    elif char == "\\":
      x += draw_char(x, y, kern, punc_backslash)
    elif char == "|":
      x += draw_char(x, y, kern, punc_line)
    elif char == ",":
      x += draw_char(x, y, kern, punc_comma)
    elif char == ".":
      x += draw_char(x, y, kern, punc_period)
    elif char == "/":
      x += draw_char(x, y, kern, punc_slash)
    elif char == "<":
      x += draw_char(x, y, kern, punc_left_arrow)
    elif char == ">":
      x += draw_char(x, y, kern, punc_right_arrow)
    elif char == "?":
      x += draw_char(x, y, kern, punc_question)
    elif char == ";":
      x += draw_char(x, y, kern, punc_semicolon)
    elif char == ":":
      x += draw_char(x, y, kern, punc_colon)
    elif char == "'":
      x += draw_char(x, y, kern, punc_single_quote)
    elif char == "\"":
      x += draw_char(x, y, kern, punc_double_quote)
    else:
      print("Unhandled character: {}".format(char))
      x += let_h_half + kern