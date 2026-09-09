Add-Type -AssemblyName System.Drawing

$imgPath = "C:/Users/kprsn/.gemini/antigravity/brain/e20e1e7f-64ed-4e48-8665-23507a67e927/.user_uploaded/media_1787550557063.png"
$bmp = [System.Drawing.Bitmap]::FromFile($imgPath)

$width = 40
$ratio = ($bmp.Height / $bmp.Width) * 0.55
$height = [Math]::Floor($width * $ratio)

$resized = New-Object System.Drawing.Bitmap($bmp, $width, $height)

# Standard ASCII mapping (Dark areas = Dense, Light areas = Space/dots)
$chars = '@', '#', '%', 'S', '*', '+', '=', '-', ':', '.', ' ', ' '

$ascii = ""
for ($y = 0; $y -lt $resized.Height; $y++) {
    for ($x = 0; $x -lt $resized.Width; $x++) {
        $color = $resized.GetPixel($x, $y)
        $brightness = (0.299 * $color.R + 0.587 * $color.G + 0.114 * $color.B)
        
        # Increase contrast
        $b = ($brightness - 128) * 1.5 + 128
        if ($b -lt 0) { $b = 0 }
        if ($b -gt 255) { $b = 255 }
        
        $idx = [Math]::Floor(($b / 255) * ($chars.Length - 1))
        $ascii += $chars[$idx]
    }
    $ascii += "
"
}

$ascii | Out-File -FilePath "ascii_out_fixed.txt" -Encoding ascii
