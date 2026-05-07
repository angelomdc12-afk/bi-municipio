$p = "PowerBI/bi_municipio_streamlit.py"
$lines = Get-Content -Encoding UTF8 $p
$start = 4428
$end = 4685
for ($i = $start; $i -le $end; $i++) {
  if ($i -le $lines.Length) {
    "{0,5}: {1}" -f $i, $lines[$i-1]
  }
}
