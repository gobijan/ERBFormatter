import sublime
import sublime_plugin
import subprocess

class ErbFormatterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("ERBFormatter.sublime-settings")
        htmlbeautifier_path = settings.get("htmlbeautifier_path", "htmlbeautifier")

        # Prepare the command
        if htmlbeautifier_path:
            cmd = [htmlbeautifier_path]
        else:
            cmd = ["htmlbeautifier"]

        region = sublime.Region(0, self.view.size())
        original_content = self.view.substr(region)

        # Execute the command
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        beautified_content, error = process.communicate(input=original_content.encode('utf-8'))

        if process.returncode == 0:
            self.view.replace(edit, region, beautified_content.decode('utf-8'))
        else:
            sublime.error_message("Error: " + error.decode('utf-8'))
