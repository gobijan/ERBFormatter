import sublime
import sublime_plugin
import subprocess
import os

class ErbFormatterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("ERBFormatter.sublime-settings")
        erb_format_path = settings.get("erb_format_path", "erb-format")

        # Expand the tilde to the user's home directory
        erb_format_path = os.path.expanduser(erb_format_path)

        if not os.path.exists(erb_format_path):
            sublime.error_message("ERB Formatter: erb-format not found at " + erb_format_path)
            return

        file_path = self.view.file_name()
        if not file_path:
            sublime.error_message("ERB Formatter: File must be saved before formatting.")
            return

        # Prepare the command to include the file path, ensuring it's properly formatted for shell execution
        cmd = [erb_format_path, file_path]

        try:
            # Execute the command, ensuring shell=True is used correctly with a string command
            output = subprocess.check_output(cmd, universal_newlines=True)
            print(output)
            if output:
                # Replace the entire content with the output
                self.view.replace(edit, sublime.Region(0, self.view.size()), output)
        except Exception as e:
            sublime.error_message("ERB Formatter Exception:" + e)
