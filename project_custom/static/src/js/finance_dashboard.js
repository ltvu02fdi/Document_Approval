/** @odoo-module **/

import * as Colors from "@web/core/colors/colors";

// 🎨 Bảng pastel mới
const PASTEL_COLORS = [
    "#FF1744", // soft peach
    "#FF9100", // soft orange
    "#FFD600", // pale yellow
    "#00E676", // blush pink
    "#00E5FF", // light coral
    "#2979FF", // rose pink
    "#D500F9", // warm sand
    "#76FF03", // pastel apricot
    "#F50057", // warm lavender pink
    "#FF4081", // golden pastel
];

// Ghi đè getColor
Colors.getColor = function (index, colorScheme, paletteSizeOrName) {
    return PASTEL_COLORS[index % PASTEL_COLORS.length];
};

// Nếu muốn patch getColors luôn
Colors.getColors = function () {
    return PASTEL_COLORS;
};

export default Colors;