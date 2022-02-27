from solid import *
from solid.utils import *
import math

cm = 10
z = 0.01

arm_width = 2.05 * cm
arm_height = 4.45 * cm
arm_hook = 0.3 * cm
arm_hook_gap = 0.5 * cm
arm_depth = max(arm_hook + arm_hook_gap, 1.3 * cm)

skrew_placement_y = 0.8 * cm
skrew_placement_x = 1.5 * cm / 2
skrew_r = 0.4 * cm / 2

fasten_skrew_spacing = 0.5 * cm
fasten_skrew_r = 0.5 * cm / 2
fasten_skrew_head_r = 0.9 * cm / 2

base_grip_angle = atan2(0.41, 1)*180/pi
base_grip_width = 6 * cm
base_grip_height = 4 * cm
base_grip_depth = 3.5 * cm

dw = 0.5 * cm


def arm_attachment_base():
    attachment_base = cube(
        [arm_width + dw * 2, dw + arm_depth - z, arm_height + dw * 2])

    attachment_hole = cube([arm_width, arm_depth, arm_height])
    attachment_hole = translate([dw, dw, dw])(attachment_hole)

    attachment_skrew_hole = cylinder(skrew_r, arm_height + dw*2 + z*2)
    attachment_skrew_hole_top = translate(
        [dw + arm_width / 2, dw + skrew_r + skrew_placement_y, dw*2-z])(attachment_skrew_hole)
    attachment_skrew_hole_bottom_left = translate(
        [-skrew_placement_x, 0, -dw*4])(attachment_skrew_hole_top)
    attachment_skrew_hole_bottom_right = translate(
        [skrew_placement_x, 0, -dw*4])(attachment_skrew_hole_top)

    corner_cut = cube([dw*4, dw*4, arm_height + dw*2 + z*2])
    corner_cut_left = rotate([0, 0, atan2(2, 1)*180/pi])(corner_cut)
    corner_cut_left = translate([0, arm_depth - dw, -z])(corner_cut_left)
    corner_cut_right = rotate([0, 0, atan2(1, 2)*180/pi])(corner_cut)
    corner_cut_right = translate(
        [arm_width + dw*2, arm_depth - dw, -z])(corner_cut_right)

    return (
        attachment_base
        - attachment_hole
        - attachment_skrew_hole_top
        - attachment_skrew_hole_bottom_left
        - attachment_skrew_hole_bottom_right
        - corner_cut_left
        - corner_cut_right
    )


def table_attachment_base():

    attachment_base = cube(
        [base_grip_width, base_grip_depth, base_grip_height]
    )
    attachment_base = rotate([base_grip_angle, 0, 0])(attachment_base)
    attachment_base = translate([0, base_grip_depth, 0])(attachment_base)

    attachment_base_link = cube(
        [base_grip_width, base_grip_depth, base_grip_height]
    )

    assembled = (
        attachment_base
        + attachment_base_link
    )
    assembled = rotate([180, 0, 0])(assembled)
    assembled = translate([-dw-arm_width/2, 0, base_grip_height])(assembled)

    return assembled


def skrew_holes():
    skrew_hole = cylinder(fasten_skrew_r, dw + base_grip_depth * 2)
    skrew_hole = rotate([90, 0, 0])(skrew_hole)
    skrew_hole = translate(
        [dw + arm_width / 2, dw + z, dw + arm_height / 2])(skrew_hole)

    fss = fasten_skrew_spacing

    skrew_hole_top_left = translate([fss, 0, fss])(skrew_hole)
    skrew_hole_bottom_left = translate([fss, 0, -fss])(skrew_hole)
    skrew_hole_top_right = translate([-fss, 0, fss])(skrew_hole)
    skrew_hole_bottom_right = translate([-fss, 0, -fss])(skrew_hole)

    skrew_head_hole = cylinder(fasten_skrew_head_r, dw + base_grip_depth * 2)
    skrew_head_hole = rotate([90, 0, 0])(skrew_head_hole)
    skrew_head_hole = translate(
        [dw + arm_width / 2, dw - 1.5 * cm, dw + arm_height / 2])(skrew_head_hole)

    fss = fasten_skrew_spacing

    skrew_head_hole_top_left = translate([fss, 0, fss])(skrew_head_hole)
    skrew_head_hole_bottom_left = translate([fss, 0, -fss])(skrew_head_hole)
    skrew_head_hole_top_right = translate([-fss, 0, fss])(skrew_head_hole)
    skrew_head_hole_bottom_right = translate([-fss, 0, -fss])(skrew_head_hole)

    return (
        skrew_hole_top_left
        + skrew_hole_bottom_left
        + skrew_hole_top_right
        + skrew_hole_bottom_right
        + skrew_head_hole_top_left
        + skrew_head_hole_bottom_left
        + skrew_head_hole_top_right
        + skrew_head_hole_bottom_right
    )


def pen_holder():
    space_between_joints = 6.35 * cm
    pen_dist = space_between_joints - 2.7 * cm
    max_pen_r = 0.5 * cm

    pen_holder = cube([arm_width, pen_dist+max_pen_r, arm_width / 2])
    pen_holder = translate([dw, -pen_dist-max_pen_r, 0])(pen_holder)

    pen_hole = cylinder(max_pen_r, arm_width / 2 + z*2)
    pen_hole = translate([dw + arm_width / 2, -pen_dist, -z])(pen_hole)

    pen_thread_hole = cylinder(0.25 * cm, arm_width + z*2)
    pen_thread_hole = rotate([0, 90, 0])(pen_thread_hole)
    pen_thread_hole = translate(
        [dw - z, -pen_dist, arm_width / 4 - z])(pen_thread_hole)

    pen_thread_hook = cylinder(0.2 * cm, arm_width + dw*2)
    pen_thread_hook = rotate([0, 90, 0])(pen_thread_hook)
    pen_thread_hook = translate([0, -0.2 * cm, arm_width / 4])(pen_thread_hook)

    pen_holder_base = cube([arm_width, dw*1.5, arm_height])
    pen_holder_base = translate([dw, -dw*1.5, 0])(pen_holder_base)

    return translate([0, -dw, 0])(
        pen_holder_base
        + pen_holder
        - pen_hole
        - pen_thread_hole
        + pen_thread_hook
        + translate([0, 0, arm_height])(
            pen_holder
            - pen_hole
            - pen_thread_hole
            + pen_thread_hook
        )
    )


fn = 32
scad_render_to_file(
    arm_attachment_base() - skrew_holes(),
    __file__[:-3] + ".scad", file_header='$fn = %d;' % fn
)

scad_render_to_file(
    table_attachment_base() - skrew_holes(),
    __file__[:-3] + "_base.scad", file_header='$fn = %d;' % fn
)

scad_render_to_file(
    pen_holder() - skrew_holes(),
    __file__[:-3] + "_pen_holder.scad", file_header='$fn = %d;' % fn
)
