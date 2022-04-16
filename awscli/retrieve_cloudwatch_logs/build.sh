# Requires pytinstaller 'pip install pyinstaller'
temp_dir=$(mktemp -d)
python_file="retrieve_cloudwatch_logs.py"
unix_tool_name="cloudwatch_logs"

pyinstaller "$python_file" --onefile --workpath "$temp_dir/build" --distpath "$temp_dir/dist" --specpath "$temp_dir/spec" --name "$unix_tool_name"
mv "$temp_dir/dist/$unix_tool_name" "$HOME/.local/bin/"
rm -rf "$temp_dir"
