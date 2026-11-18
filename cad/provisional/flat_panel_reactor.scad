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
    // Through boss and rear wall, opening into the internal cavity.
    translate([x, y, -panel_depth/2-boss_projection-1])
        cylinder(d=port_bore_d, h=boss_projection+wall+2);
}

module gas_bore(x) {
    // Through boss and top wall, opening into the internal cavity.
    translate([x, panel_height/2-1, 0])
        rotate([-90, 0, 0])
            cylinder(d=port_bore_d, h=boss_projection+wall+2);
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

        // Four rear-face sensor access bosses.
        for (x = sensor_x)
            for (y = sensor_y)
                sensor_boss(x, y);

        // Two top-face gas connection bosses.
        for (x = gas_x)
            gas_boss(x);
    }

    // Six continuous bores.
    for (x = sensor_x)
        for (y = sensor_y)
            sensor_bore(x, y);

    for (x = gas_x)
        gas_bore(x);
}
