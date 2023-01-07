import lib

# Letter sizes
let_h = 50
let_h_half = let_h / 2
let_h_quart = let_h / 4
let_h_fifth = let_h / 5
let_h_eight = let_h / 8
let_h_sixt = let_h / 16

line_height = let_h + let_h_quart + let_h_eight

def letter_cap_a(x, y):
  lib.path("M{} {}l{} {}l{} {}M{} {}h{}"
    .format(x, y, let_h_quart, -let_h, let_h_quart, let_h, x + let_h_eight, y-let_h_half, let_h_quart))

def letter_cap_b(x, y):
  lib.path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}m{} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, let_h_quart, 0,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))

def letter_cap_c(x, y):
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_half, y, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart))

def letter_cap_d(x, y):
  lib.path("M{} {}v{}h{}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))

def letter_cap_e(x, y):
  lib.path("M{} {}h{}v{}h{}m{} {}h{}"
    .format(x + let_h_half, y, -let_h_half, -let_h, let_h_half, -let_h_half, let_h_half, let_h_quart))

def letter_cap_f(x, y):
  lib.path("M{} {}v{}h{}m{} {}h{}"
    .format(x, y, -let_h, let_h_half, -let_h_half, let_h_half, let_h_quart))

def letter_cap_g(x, y):
  lib.path("M{} {}h{}v{} q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_quart, y - let_h_half, let_h_quart, let_h_quart,
            0, let_h_quart,  -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart))

def letter_cap_h(x, y):
  lib.path("M{} {}v{}m{} {}v{}m{} {}h{}"
    .format(x, y, -let_h, let_h_half, 0, let_h, 0, -let_h_half, -let_h_half))

def letter_cap_i(x, y):
  lib.path("M{} {}h{}m{} {}v{}m{} {}h{}"
    .format(x, y, let_h_half, -let_h_quart, 0, -let_h, -let_h_quart, 0, let_h_half))

def letter_cap_j(x, y):
  lib.path("M{} {}v{}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_half, y - let_h, let_h_half + let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart))

def letter_cap_k(x, y):
  lib.path("M{} {}v{}m{} {}l{} {}l{} {}"
    .format(x, y, -let_h, let_h_half, 0, -let_h_half, let_h_half, let_h_half, let_h_half))

def letter_cap_l(x, y):
  lib.path("M{} {}v{}h{}"
    .format(x, y - let_h, let_h, let_h_half))

def letter_cap_m(x, y):
  lib.path("M{} {}v{}l{} {}l{} {}v{}"
    .format(x, y, -let_h, let_h_quart, let_h, let_h_quart, -let_h, let_h))

def letter_cap_n(x, y):
  lib.path("M{} {}v{}l{} {}v{}"
    .format(x, y, -let_h, let_h_half, let_h, -let_h))

def letter_cap_o(x, y):
  lib.path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart))

def letter_cap_p(x, y):
  lib.path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))

def letter_cap_q(x, y):
  lib.path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}m{} {}l{} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            0, -let_h_quart, let_h_quart, let_h_quart))

def letter_cap_r(x, y):
  lib.path("M{} {}v{}h{}q{} {} {} {}q{} {} {} {}h{}l{} {}"
    .format(x, y, -let_h, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, let_h_half, let_h_half))

def letter_cap_s(x, y):
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart, let_h_quart))

def letter_cap_t(x, y):
  lib.path("M{} {}v{}m{} {}h{}"
    .format(x + let_h_quart, y, -let_h, -let_h_quart, 0, let_h_half))

def letter_cap_u(x, y):
  lib.path("M{} {}v{}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y - let_h, let_h_half + let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            -let_h_half - let_h_quart))

def letter_cap_v(x, y):
  lib.path("M{} {}l{} {}l{} {}"
    .format(x, y - let_h, let_h_quart, let_h, let_h_quart, -let_h))

def letter_cap_w(x, y):
  lib.path("M{} {}l{} {}l{} {}l{} {}l{} {}"
    .format(x, y - let_h,
            let_h_eight, let_h,
            let_h_eight, -let_h_half,
            let_h_eight, let_h_half,
            let_h_eight, -let_h))

def letter_cap_x(x, y):
  lib.path("M{} {}l{} {}m{} {}l{} {}"
    .format(x, y - let_h, let_h_half, let_h, 0, -let_h, -let_h_half, let_h))

def letter_cap_y(x, y):
  lib.path("M{} {}l{} {}l{} {}m{} {}v{}"
    .format(x, y - let_h, let_h_quart, let_h_half, let_h_quart, -let_h_half,
            -let_h_quart, let_h_half, let_h_half))

def letter_cap_z(x, y):
  lib.path("M{} {}h{}l{} {}h{}"
    .format(x + let_h_half, y, -let_h_half, let_h_half, -let_h, -let_h_half))

def letter_low_a(x, y):
  lib.path("M{} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_half, y, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart))

def letter_low_b(x, y):
  lib.path("M{} {}v{}M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x, y, -let_h, x, y - let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart))

def letter_low_c(x, y):
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + let_h_half, y, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart))

def letter_low_d(x, y):
  lib.path("M{} {}v{}M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_half, y, -let_h, x + let_h_half, y - let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart))

def letter_low_e(x, y):
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y - let_h_quart, let_h_half,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart))

def letter_low_f(x, y):
  lib.path("M{} {}v{}q{} {} {} {}m{} {}h{}"
    .format(x + let_h_quart, y, -let_h_half - let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            -let_h_half, let_h_half, let_h_half))

def letter_low_g(x, y):
  lib.path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}m{} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_half, y - let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))

def letter_low_h(x, y):
  lib.path("M{} {}v{}m{} {}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y - let_h, let_h, 0, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_quart))

def letter_low_i(x, y):
  lib.path("M{} {}v{}m{} {}v{}"
    .format(x + let_h_quart, y, -let_h_half, 0, -let_h_eight, -let_h_eight))

def letter_low_j(x, y):
  lib.path("M{} {}v{}m{} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_quart, y - let_h_half - let_h_quart, let_h_eight, 0, let_h_eight, let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_eight))

def letter_low_k(x, y):
  lib.path("M{} {}v{}m{} {}l{} {}l{} {}"
    .format(x, y - let_h, let_h, let_h_half, -let_h_half,
            -let_h_half, let_h_quart, let_h_half, let_h_quart))

def letter_low_l(x, y):
  lib.path("M{} {}v{}".format(x + let_h_quart, y, -let_h))

def letter_low_m(x, y):
  lib.path("M{} {}v{}m{} {}q{} {} {} {}q{} {} {} {}v{}m{} {}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y, -let_h_half, 0, let_h_eight,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            let_h_eight, 0, let_h_eight, let_h_eight,
            let_h_eight, 0, -let_h_eight,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            let_h_eight, 0, let_h_eight, let_h_eight,
            let_h_quart + let_h_eight))

def letter_low_n(x, y):
  lib.path("M{} {}v{}m{} {}q{} {} {} {}q{} {} {} {}v{}"
    .format(x, y, -let_h_half, 0, let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_quart))

def letter_low_o(x, y):
  lib.path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart))

def letter_low_p(x, y):
  lib.path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}m{} {}v{}"
    .format(x, y - let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_half + let_h_quart))

def letter_low_q(x, y):
  lib.path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}m{} {}v{}"
    .format(x + let_h_half, y - let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, let_h_half + let_h_quart))

def letter_low_r(x, y):
  lib.path("M{} {}v{}m{} {}q{} {} {} {}q{} {} {} {}"
    .format(x, y, -let_h_half, 0, let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart))

def letter_low_s(x, y):
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart + let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            -let_h_quart,
            -let_h_eight, 0, -let_h_eight, -let_h_eight,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            let_h_quart + let_h_eight))

def letter_low_t(x, y):
  lib.path("M{} {}v{}m{} {}h{}"
    .format(x + let_h_quart, y, -let_h_half - let_h_quart,
            -let_h_quart, let_h_quart, let_h_half))

def letter_low_u(x, y):
  lib.path("M{} {}v{}q{} {} {} {}q{} {} {} {}m{} {}v{}"
    .format(x, y - let_h_half, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, let_h_quart, -let_h_half))

def letter_low_v(x, y):
  lib.path("M{} {}l{} {}l{} {}"
    .format(x, y - let_h_half, let_h_quart, let_h_half, let_h_quart, -let_h_half))

def letter_low_w(x, y):
  lib.path("M{} {}v{}q{} {} {} {}q{} {} {} {}v{}m{} {}q{} {} {} {}q{} {} {} {}m{} {}v{}"
    .format(x, y - let_h_half, let_h_quart + let_h_eight,
            0, let_h_eight, let_h_eight, let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            -let_h_eight, 0, let_h_eight,
            0, let_h_eight, let_h_eight, let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            0, -let_h_quart - let_h_eight, let_h_half))

def letter_low_x(x, y):
  lib.path("M{} {}l{} {}m{} {}l{} {}"
    .format(x, y-let_h_half, let_h_half, let_h_half, 0, -let_h_half, -let_h_half, let_h_half))

def letter_low_y(x, y):
  lib.path("M{} {}l{} {}m{} {}l{} {}"
    .format(x, y - let_h_half, let_h_quart, let_h_half, let_h_quart, -let_h_half, -let_h_half + let_h_eight, let_h_half + let_h_quart))

def letter_low_z(x, y):
  lib.path("M{} {}h{}l{} {}h{}"
    .format(x + let_h_half, y, -let_h_half, let_h_half, -let_h_half, -let_h_half))

def number_0(x, y):
  lib.path("M{} {}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}m{} {}l{} {}"
    .format(x + let_h_quart, y,
            -let_h_quart, 0, -let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart, -let_h_quart, let_h_half, -let_h_half))

def number_1(x, y):
  lib.path("M{} {}h{}m{} {}v{}l{} {}"
    .format(x, y, let_h_half, -let_h_quart, 0, -let_h, -let_h_quart, let_h_quart))

def number_2(x, y):
  lib.path("M{} {}h{}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x + let_h_half, y, -let_h_half, -let_h_quart,
            0, -let_h_quart, let_h_quart, -let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart))

def number_3(x, y):
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}h{}m{} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_eight, let_h_eight, 0,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart))

def number_4(x, y):
  lib.path("M{} {}v{}h{}m{} {}v{}"
    .format(x, y - let_h, let_h_half, let_h_half, 0, let_h_half, -let_h))

def number_5(x, y):
  lib.path("M{} {}h{}v{}h{}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + let_h_half, y - let_h, -let_h_half, let_h_half, let_h_quart,
            let_h_quart, 0, let_h_quart, let_h_quart,
            0, let_h_quart, -let_h_quart, let_h_quart,
            -let_h_quart))

def number_6(x, y):
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x + let_h_half, y - let_h, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            let_h_half,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart))

def number_7(x, y):
  lib.path("M{} {}h{}l{} {}"
    .format(x, y - let_h, let_h_half, -let_h_half, let_h))

def number_8(x, y):
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

def number_9(x, y):
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}"
    .format(x, y, let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_quart,
            -let_h_half,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart))

def punc_exclamation(x, y):
  lib.path("M{} {}v{}m{} {}v{}"
    .format(x + let_h_quart, y - let_h, let_h_half + let_h_eight, 0, let_h_quart, let_h_eight))

def punc_at(x, y):
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

def punc_pound(x, y):
  lib.path("M{} {}v{}m{} {}v{}M{} {}h{}m{} {}h{}"
    .format(x + let_h_eight, y, -let_h, let_h_quart, 0, let_h,
            x, y - let_h_quart, let_h_half, 0, -let_h_half, -let_h_half))

def punc_dollar(x, y):
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}M{} {}v{}"
    .format(x, y - (let_h_fifth / 2), let_h_quart,
            let_h_quart, 0, let_h_quart, -let_h_fifth,
            0, -let_h_fifth, -let_h_quart, -let_h_fifth,
            -let_h_quart, 0, -let_h_quart, -let_h_fifth,
            0, -let_h_fifth, let_h_quart, -let_h_fifth,
            let_h_quart, x + let_h_quart, y, -let_h))

def punc_percent(x, y):
  lib.path("M{} {}l{} {}"
    .format(x, y, let_h_half, -let_h))
  lib.circ(x + let_h_eight, y - let_h + let_h_eight, let_h_eight)
  lib.circ(x + let_h_eight + let_h_quart, y - let_h_eight, let_h_eight)

def punc_carrot(x, y):
  lib.path("M{} {}l{} {}l{} {}"
    .format(x, y - let_h + let_h_quart, let_h_quart, -let_h_quart, let_h_quart, let_h_quart))

def punc_and(x, y):
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

def punc_star(x, y):
  lib.path("M{} {}v{}m{} {}l{} {}m{} {}l{} {}"
    .format(x + let_h_quart, y - let_h_quart + let_h_eight, -let_h_half -let_h_quart, -let_h_quart, let_h_eight, let_h_half, let_h_half, 0, -let_h_half, -let_h_half, let_h_half))

def punc_left_paren(x, y):
  lib.path("M{} {}q{} {} {} {}"
    .format(x + let_h_half - let_h_eight, y, -let_h_half, -let_h_half, 0, -let_h))

def punc_right_paren(x, y):
  lib.path("M{} {}q{} {} {} {}"
    .format(x + let_h_eight, y, let_h_half, -let_h_half, 0, -let_h))

def punc_dash(x, y):
  lib.path("M{} {}h{}".format(x, y - let_h_half, let_h_half))

def punc_underscore(x, y):
  lib.path("M{} {}h{}".format(x, y, let_h_half))

def punc_plus(x, y):
  lib.path("M{} {}h{}m{} {}v{}"
    .format(x, y - let_h_half, let_h_half, -let_h_quart, -let_h_quart, let_h_half))

def punc_equals(x, y):
  lib.path("M{} {}h{}m{} {}h{}"
    .format(x, y - let_h_half + let_h_eight, let_h_half, 0, -let_h_quart, -let_h_half))

def punc_left_brace(x, y):
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_quart + let_h_eight, y, -let_h_eight,
            -let_h_eight, 0, -let_h_eight, -let_h_eight,
            -let_h_quart,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            -let_h_quart,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            let_h_eight))

def punc_right_brace(x, y):
  lib.path("M{} {}h{}q{} {} {} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}"
    .format(x + let_h_quart - let_h_eight, y, let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            -let_h_quart,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            -let_h_eight, 0, -let_h_eight, -let_h_eight,
            -let_h_quart,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            -let_h_eight))

def punc_left_bracket(x, y):
  lib.path("M{} {}h{}v{}h{}"
    .format(x + let_h_quart + let_h_eight, y, -let_h_quart, -let_h, let_h_quart))

def punc_right_bracket(x, y):
  lib.path("M{} {}h{}v{}h{}"
    .format(x + let_h_quart - let_h_eight, y, +let_h_quart, -let_h, -let_h_quart))

def punc_backslash(x, y):
  lib.path("M{} {}l{} {}"
    .format(x, y - let_h, let_h_half, let_h))

def punc_line(x, y):
  lib.path("M{} {}v{}"
    .format(x + let_h_quart, y, -let_h))

def punc_comma(x, y):
  lib.path("M{} {}q{} {} {} {}v{}"
    .format(x + let_h_quart - let_h_eight, y,
            let_h_eight, 0, let_h_eight, -let_h_eight, -let_h_eight))

def punc_period(x, y):
  lib.path("M{} {}v{}".format(x + let_h_quart, y, -let_h_eight))

def punc_slash(x, y):
  lib.path("M{} {}l{} {}".format(x, y, let_h_half, -let_h))

def punc_left_arrow(x, y):
  lib.path("M{} {}l{} {}l{} {}"
    .format(x + let_h_quart + let_h_eight, y - let_h_half + let_h_quart,
            -let_h_quart, -let_h_quart, let_h_quart, -let_h_quart))

def punc_right_arrow(x, y):
  lib.path("M{} {}l{} {}l{} {}"
    .format(x + let_h_quart - let_h_eight, y - let_h_half + let_h_quart,
            let_h_quart, -let_h_quart, -let_h_quart, -let_h_quart))

def punc_question(x, y):
  lib.path("M{} {}v{}m{} {}v{}q{} {} {} {}q{} {} {} {}v{}q{} {} {} {}h{}q{} {} {} {}v{}"
    .format(x + let_h_quart, y, -let_h_eight, 0, -let_h_quart, -let_h_eight,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight,
            -let_h_eight,
            0, -let_h_eight, -let_h_eight, -let_h_eight,
            -let_h_quart,
            -let_h_eight, 0, -let_h_eight, let_h_eight,
            let_h_eight))

def punc_semicolon(x, y):
  lib.path("M{} {}q{} {} {} {}v{}m{} {}v{}"
    .format(x + let_h_quart - let_h_eight, y,
            let_h_eight, 0, let_h_eight, -let_h_eight, -let_h_eight,
            0, -let_h_eight, -let_h_eight))

def punc_colon(x, y):
  lib.path("M{} {}v{}m{} {}v{}"
    .format(x + let_h_quart, y - let_h_quart, -let_h_eight, 0, -let_h_quart, -let_h_eight))

def punc_single_quote(x, y):
  lib.path("M{} {}v{}".format(x + let_h_quart, y - let_h + let_h_eight, let_h_eight))

def punc_double_quote(x, y):
  lib.path("M{} {}v{}m{} {}v{}"
    .format(x + let_h_quart - let_h_sixt, y - let_h + let_h_eight, let_h_eight, let_h_eight, 0, -let_h_eight))

def punc_back_tick(x, y):
  lib.path("M{} {}l{} {}"
    .format(x + let_h_eight, y-let_h, let_h_quart, let_h_quart))

def punc_tilde(x, y):
  lib.path("M{} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}q{} {} {} {}"
    .format(x, y - let_h_half,
            0, -let_h_eight, let_h_eight, -let_h_eight,
            let_h_eight, 0, let_h_eight, let_h_eight,
            0, let_h_eight, let_h_eight, let_h_eight,
            let_h_eight, 0, let_h_eight, -let_h_eight))

def letter_low_e_accent(x, y):
  lib.path("M{} {}h{}q{} {} {} {}q{} {} {} {}q{} {} {} {}h{}M{} {}l{} {}"
    .format(x, y - let_h_quart, let_h_half,
            0, -let_h_quart, -let_h_quart, -let_h_quart,
            -let_h_quart, 0, -let_h_quart, let_h_quart,
            0, let_h_quart, let_h_quart, let_h_quart,
            let_h_quart - let_h_eight, x + let_h_eight, y - let_h_half - let_h_eight,
            let_h_quart, -let_h_quart))

def letter_cap_e_accent(x, y):
  lib.path("M{} {}h{}v{}h{}m{} {}h{}M{} {}l{} {}"
    .format(x + let_h_half, y, -let_h_half, -let_h,
            let_h_half, -let_h_half, let_h_half, let_h_quart,
            x + let_h_eight, y - let_h - let_h_eight,
            let_h_quart, -let_h_quart))

def draw_string(x, y, kern, value:str):
  for char in value:
    # lib.rect(x, y - let_h, let_h_half, let_h)
    # lib.path(f"M{x} {y - let_h_half}h{let_h_half}")
    # lib.path(f"M{x} {y + let_h_quart}h{let_h_half}")

    if char == " ":   pass
    elif char == "A": letter_cap_a(x, y)
    elif char == "B": letter_cap_b(x, y)
    elif char == "C": letter_cap_c(x, y)
    elif char == "D": letter_cap_d(x, y)
    elif char == "E": letter_cap_e(x, y)
    elif char == "F": letter_cap_f(x, y)
    elif char == "G": letter_cap_g(x, y)
    elif char == "H": letter_cap_h(x, y)
    elif char == "I": letter_cap_i(x, y)
    elif char == "J": letter_cap_j(x, y)
    elif char == "K": letter_cap_k(x, y)
    elif char == "L": letter_cap_l(x, y)
    elif char == "M": letter_cap_m(x, y)
    elif char == "N": letter_cap_n(x, y)
    elif char == "O": letter_cap_o(x, y)
    elif char == "P": letter_cap_p(x, y)
    elif char == "Q": letter_cap_q(x, y)
    elif char == "R": letter_cap_r(x, y)
    elif char == "S": letter_cap_s(x, y)
    elif char == "T": letter_cap_t(x, y)
    elif char == "U": letter_cap_u(x, y)
    elif char == "V": letter_cap_v(x, y)
    elif char == "W": letter_cap_w(x, y)
    elif char == "X": letter_cap_x(x, y)
    elif char == "Y": letter_cap_y(x, y)
    elif char == "Z": letter_cap_z(x, y)
    elif char == "a": letter_low_a(x, y)
    elif char == "b": letter_low_b(x, y)
    elif char == "c": letter_low_c(x, y)
    elif char == "d": letter_low_d(x, y)
    elif char == "e": letter_low_e(x, y)
    elif char == "f": letter_low_f(x, y)
    elif char == "g": letter_low_g(x, y)
    elif char == "h": letter_low_h(x, y)
    elif char == "i": letter_low_i(x, y)
    elif char == "j": letter_low_j(x, y)
    elif char == "k": letter_low_k(x, y)
    elif char == "l": letter_low_l(x, y)
    elif char == "m": letter_low_m(x, y)
    elif char == "n": letter_low_n(x, y)
    elif char == "o": letter_low_o(x, y)
    elif char == "p": letter_low_p(x, y)
    elif char == "q": letter_low_q(x, y)
    elif char == "r": letter_low_r(x, y)
    elif char == "s": letter_low_s(x, y)
    elif char == "t": letter_low_t(x, y)
    elif char == "u": letter_low_u(x, y)
    elif char == "v": letter_low_v(x, y)
    elif char == "w": letter_low_w(x, y)
    elif char == "x": letter_low_x(x, y)
    elif char == "y": letter_low_y(x, y)
    elif char == "z": letter_low_z(x, y)
    elif char == "0": number_0(x, y)
    elif char == "1": number_1(x, y)
    elif char == "2": number_2(x, y)
    elif char == "3": number_3(x, y)
    elif char == "4": number_4(x, y)
    elif char == "5": number_5(x, y)
    elif char == "6": number_6(x, y)
    elif char == "7": number_7(x, y)
    elif char == "8": number_8(x, y)
    elif char == "9": number_9(x, y)
    elif char == "!": punc_exclamation(x, y)
    elif char == "@": punc_at(x, y)
    elif char == "#": punc_pound(x, y)
    elif char == "$": punc_dollar(x, y)
    elif char == "%": punc_percent(x, y)
    elif char == "^": punc_carrot(x, y)
    elif char == "&": punc_and(x, y)
    elif char == "*": punc_star(x, y)
    elif char == "(": punc_left_paren(x, y)
    elif char == ")": punc_right_paren(x, y)
    elif char == "-" or char == "—": punc_dash(x, y)
    elif char == "_": punc_underscore(x, y)
    elif char == "+": punc_plus(x, y)
    elif char == "=": punc_equals(x, y)
    elif char == "{": punc_left_brace(x, y)
    elif char == "}": punc_right_brace(x, y)
    elif char == "[": punc_left_bracket(x, y)
    elif char == "]": punc_right_bracket(x, y)
    elif char == "\\": punc_backslash(x, y)
    elif char == "|": punc_line(x, y)
    elif char == ",": punc_comma(x, y)
    elif char == ".": punc_period(x, y)
    elif char == "/": punc_slash(x, y)
    elif char == "<": punc_left_arrow(x, y)
    elif char == ">": punc_right_arrow(x, y)
    elif char == "?": punc_question(x, y)
    elif char == ";": punc_semicolon(x, y)
    elif char == ":": punc_colon(x, y)
    elif char == "'" or char == "’" or char == "‘":
      punc_single_quote(x, y)
    elif char == "\"" or char == "“" or char == "”":
      punc_double_quote(x, y)
    elif char == "`": punc_back_tick(x, y)
    elif char == "~": punc_tilde(x, y)
    elif char == "é": letter_low_e_accent(x, y)
    elif char == "É": letter_cap_e_accent(x, y)
    else: print("Unhandled character: {}".format(char))
    x += let_h_half + kern