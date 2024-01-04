variable "netbox_url" {
  type = string
  default = "https://netbox.openknowit.com"
  description = "netbox endpoint"
}


variable "color_map" {
  type = map(string)
  default = {
    "Black"         = "000000",
    "Blue"          = "0000ff",
    "BlueViolet"    = "8a2be2",
    "Brown"         = "a52a2a",
    "CadetBlue"     = "5f9ea0",
    "Chartreuse"    = "7fff00",
    "Chocolate"     = "d2691e",
    "Coral"         = "ff7f50",
    "Crimson"       = "dc143c",
    "Cyan"          = "00ffff",
    "DarkBlue"      = "00008b",
    "DarkCyan"      = "008b8b",
    "DarkGreen"     = "006400",
    "DarkKhaki"     = "bdb76b",
    "DarkMagenta"   = "8b008b",
    "DarkOliveGreen"= "556b2f",
    "DarkOrange"    = "ff8c00",
    "DarkOrchid"    = "9932cc",
    "DarkRed"       = "8b0000",
    "DarkSalmon"    = "e9967a",
    "DarkSeaGreen"  = "8fbc8f",
    "DarkSlateBlue" = "483d8b",
    "DarkSlateGray" = "2f4f4f",
    "DarkTurquoise" = "00ced1",
    "DarkViolet"    = "9400d3",
    "DeepPink"      = "ff1493",
    "DeepSkyBlue"   = "00bfff",
    "DimGrey"       = "696969",
    "FireBrick"     = "b22222",
    "ForestGreen"   = "228b22",
    "Goldenrod"     = "daa520",
    "Gold"          = "ffd700",
    "Gray"          = "808080",
    "Green"         = "008000",
    "Green"         = "00ff00",
    "GreenYellow"   = "adff2f",
    "HotPink"       = "ff69b4",
    "IndianRed"     = "cd5c5c",
    "Indigo"        = "4b0082",
    "Khaki"         = "f0e68c",
    "LavenderBlush" = "fff0f5",
    "Lavender"      = "e6e6fa",
    "LawnGreen"     = "7cfc00",
    "LemonChiffon"  = "fffacd",
    "LightBlue"     = "add8e6",
    "LightCoral"    = "f08080",
    "LightGreen"    = "90ee90",
    "LightGrey"     = "d3d3d3",
    "LightPink"     = "ffb6c1",
    "LightSalmon"   = "ffa07a",
    "LightSeaGreen" = "20b2aa",
    "LightSkyBlue"  = "87cefa",
    "LightSlateGrey"= "778899",
    "LightSteelBlue"= "b0c4de",
    "LightYellow"   = "ffffe0",
    "Lime"          = "008000",
    "LimeGreen"     = "32cd32",
    "Magenta"       = "ff00ff",
    "Maroon"        = "800000",
    "MediumAquamarine"= "66cdaa",
    "MediumBlue"    = "0000cd",
    "MediumOrchid"  = "9370db",
    "MediumOrchid"  = "ba55d3",
    "MediumPurple"  = "9370db",
    "MediumSeaGreen"= "3cb371",
    "MediumSlateBlue"= "7b68ee",
    "MediumSpringGreen" = "00fa9a",
    "MediumTurquoise"= "48d1cc",
    "MediumVioletRed"= "c71585",
    "MidnightBlue"  = "191970",
    "MintCream"     = "f5fffa",
    "Moccasin"      = "ffe4b5",
    "Navy"          = "000080",
    "Olive"         = "808000",
    "OliveDrab"     = "6b8e23",
    "Orange"        = "ffa500",
    "OrangeRed"     = "ff4500",
    "Orchid"        = "da70d6",
    "PaleGreen"     = "98fb98",
    "PaleTurquoise" = "afeeee",
    "PaleVioletRed" = "db7093",
    "Peru"          = "cd853f",
    "Pink"          = "ffc0cb",
    "Plum"          = "dda0dd",
    "PowderBlue"    = "b0e0e6",
    "Purple"        = "800080",
    "Red"           = "ff0000",
    "RosyBrown"     = "bc8f8f",
    "RoyalBlue"     = "4169e1",
    "SaddleBrown"   = "8b4513",
    "Salmon"        = "fa8072",
    "SandyBrown"    = "f4a460",
    "SeaGreen"      = "2e8b57",
    "Sienna"        = "a0522d",
    "Silver"        = "c0c0c0",
    "SkyBlue"       = "87ceeb",
    "SlateBlue"     = "6a5acd",
    "SlateGray"     = "708090",
    "Snow"          = "fffafa",
    "SpringGreen"   = "00ff7f",
    "SteelBlue"     = "4682b4",
    "Tan"           = "d2b48c",
    "Teal"          = "008080",
    "Thistle"       = "d8bfd8",
    "Tomato"        = "ff6347",
    "Turquoise"     = "40e0d0",
    "White"         = "ffffff",
    "Yellow"        = "ffff00"
  }
}