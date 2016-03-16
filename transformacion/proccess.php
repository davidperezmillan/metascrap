<?php 

$url = "http://elitetorrent.net/get-torrent/31103";
$save_to='fichero.txt';

file_put_contents($save_to, fopen("$url", 'r'));
?>