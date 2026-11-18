// PBR Digital Biosphere — provisional flat-panel reactor
// Units: millimetres. Coordinate origin: centre of external envelope.
// Concept geometry only; not a fabrication or pressure-vessel design.

panel_length = 300;
panel_height = 200;
panel_depth = 40;
wall = 3;

port_bore_d = 8;
port_boss_od = 16;
boss_projection = 10;

sensor_x = [-75, 75];
sensor_y = [-50, 50];
gas_x = [-75, 75];

// Internal fluid-domain parameters. Port coordinates are measured from
// the left and front external edges; the front-edge datum maps to Z = 0.
sparger_diameter = 8;
sparger_x = 150;
sparger_y = 20;
drain_diameter = 10;
drain_x = 30;
drain_y = 20;
baffle_count = 2;
baffle_height = 25;
baffle_thickness = 2;

$fn = 96;

module sensor_boss(x, y) {
    translate([x, y, -panel_depth/2])
        rotate([180, 0, 0])
            cylinder(d=port_boss_od, h=boss_projection);
}

module gas_boss(x) {
    translate([x, panel_height/2, 0])
        rotate([-90, 0, 0])
            cylinder(d=port_boss_od, h=boss_projection);
}

module sensor_bore(x, y) {
    translate([x, y, -panel_depth/2-boss_projection-1])
        cylinder(d=port_bore_d, h=boss_projection+wall+2);
}

module gas_bore(x) {
    translate([x, panel_height/2-1, 0])
        rotate([-90, 0, 0])
            cylinder(d=port_bore_d, h=boss_projection+wall+2);
}

module bottom_port(diameter, x_from_left, z_from_front) {
    x = x_from_left - panel_length/2;
    z = z_from_front - panel_depth/2;
    // Cylinder's local Z axis is rotated to the reactor's +Y axis.
    translate([x, -panel_height/2-1, z])
        rotate([-90, 0, 0])
            cylinder(d=diameter, h=wall+2);
}

module internal_baffles() {
    usable_length = panel_length - 2*wall;
    floor_y = -panel_height/2 + wall;
    for (i = [0:baffle_count-1]) {
        x_from_left = wall + usable_length*(i+1)/(baffle_count+1);
        x = x_from_left - panel_length/2;
        translate([x, floor_y+baffle_height/2, 0])
            cube([baffle_thickness, baffle_height, panel_depth-2*wall], center=true);
    }
}

difference() {
    union() {
        // Closed six-wall shell.
        difference() {
            cube([panel_length, panel_height, panel_depth], center=true);
            cube([
                panel_length-2*wall,
                panel_height-2*wall,
                panel_depth-2*wall
            ], center=true);
        }

        for (x = sensor_x)
            for (y = sensor_y)
                sensor_boss(x, y);

        for (x = gas_x)
            gas_boss(x);

        // Positive internal geometry: baffles are fused to the floor.
        internal_baffles();
    }

    for (x = sensor_x)
        for (y = sensor_y)
            sensor_bore(x, y);

    for (x = gas_x)
        gas_bore(x);

    // Two bottom-wall ports, cut along +Y.
    bottom_port(sparger_diameter, sparger_x, sparger_y);
    bottom_port(drain_diameter, drain_x, drain_y);
}
