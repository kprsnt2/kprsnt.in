Add-Type -AssemblyName System.Drawing

$imgPath = "C:/Users/kprsn/.gemini/antigravity/brain/e20e1e7f-64ed-4e48-8665-23507a67e927/.user_uploaded/media_1787551259206.png"
# The user uploaded a new image, let's just use the previous source image: media_1787550557063.png
$imgPath = "C:/Users/kprsn/.gemini/antigravity/brain/e20e1e7f-64ed-4e48-8665-23507a67e927/.user_uploaded/media_1787550557063.png"

$bmp = [System.Drawing.Bitmap]::FromFile($imgPath)

$width = 45
$ratio = ($bmp.Height / $bmp.Width) * 0.55
$height = [Math]::Floor($width * $ratio)

$resized = New-Object System.Drawing.Bitmap($bmp, $width, $height)

# INVERTED CHARACTERS FOR DARK MODE! (Dark pixels -> less dense text, Light pixels -> more dense text)
$chars = ' ', '.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@'

$ascii = ""
for ($y = 0; $y -lt $resized.Height; $y++) {
    for ($x = 0; $x -lt $resized.Width; $x++) {
        $color = $resized.GetPixel($x, $y)
        $brightness = (0.299 * $color.R + 0.587 * $color.G + 0.114 * $color.B)
        $idx = [Math]::Floor(($brightness / 255) * ($chars.Length - 1))
        $ascii += $chars[$idx]
    }
    $ascii += "
"
}

$ascii | Out-File -FilePath "ascii_out_dark.txt" -Encoding ascii
Write-Host "Success"
