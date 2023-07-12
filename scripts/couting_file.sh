count_files_in_folder() {
    folder_path="$1"
    file_count=$(find "$folder_path" -type f | wc -l)
    echo "El número de archivos en la carpeta '$folder_path' es: $file_count"
}

# Llamada a la función con el argumento proporcionado al ejecutar el script
count_files_in_folder "$1"