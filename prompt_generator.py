import re
from typing import Dict, Any


class PromptGenerator:
    def __init__(self, template_text: str):
        """
        Initialize the PromptGenerator with a template containing placeholders.

        Args:
            template_text (str): A string containing placeholders in the format {{variable_name}}
                               These placeholders will be replaced with actual values during interpolation.

        Example template:
            "Here is a {{section_name}} that will be replaced with actual content"
        """
        self.template = template_text

    def extract_variables(self) -> list:
        """
        Extract all variable names from the template using regex pattern matching.

        The pattern r"\{\{(.*?)\}\}" matches any text between double curly braces.
        For example, from "Hello {{name}}, your score is {{score}}", it extracts:
        ["name", "score"]

        Returns:
            list: A list of variable names found in the template
        """
        pattern = r"\{\{(.*?)\}\}"
        return re.findall(pattern, self.template)

    def interpolate(self, variables: Dict[str, Any]) -> str:
        """
        Replace all placeholders in the template with their corresponding values.

        Args:
            variables (Dict[str, Any]): A dictionary mapping variable names to their values
                                      Keys should match the names in the placeholders

        Example:
            template: "Hello {{name}}, your score is {{score}}"
            variables: {"name": "John", "score": 95}
            result: "Hello John, your score is 95"

        Returns:
            str: The fully interpolated text with all placeholders replaced
        """
        result = self.template
        for var_name, value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            result = result.replace(placeholder, str(value))
        return result


def read_source_file(filepath: str) -> str:
    """
    Read and return the entire contents of a file.

    Args:
        filepath (str): Path to the file to be read

    Returns:
        str: The entire contents of the file as a string

    Note:
        - Uses UTF-8 encoding to properly handle special characters
        - File is automatically closed after reading due to context manager usage
        - If file doesn't exist or can't be read, will raise FileNotFoundError
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


# def extract_section(text: str, start_marker: str, end_marker: str) -> str:
#     """
#     Extract a section of text between two marker strings.

#     Args:
#         text (str): The source text to extract from
#         start_marker (str): The string that marks the beginning of the section
#         end_marker (str): The string that marks the end of the section

#     Example:
#         text: "// START_CODE\ndef hello():\n    print('Hello')\n// END_CODE"
#         start_marker: "// START_CODE"
#         end_marker: "// END_CODE"
#         result: "def hello():\n    print('Hello')"

#     Returns:
#         str: The extracted text between markers, with leading/trailing whitespace removed
#              Returns empty string if markers aren't found

#     Note:
#         - Case sensitive matching for markers
#         - Returns empty string if either marker is not found
#         - Removes the markers themselves from the returned text
#     """
#     try:
#         start_idx = text.index(start_marker) + len(start_marker)
#         end_idx = text.index(end_marker, start_idx)
#         return text[start_idx:end_idx].strip()
#     except ValueError:
#         return ""


def main():
    # Read the prompt template that contains placeholders
    # This template defines the structure of our final output
    presentation_template = read_source_file(
        "prompt_templates/presentation_template.txt"
    )
    accuracy_template = read_source_file("prompt_templates/accuracy_template.txt")
    optimality_template = read_source_file("prompt_templates/optimality_template.txt")

    # Create a generator instance with our template
    presentation_generator = PromptGenerator(presentation_template)
    accuracy_generator = PromptGenerator(accuracy_template)
    optimality_generator = PromptGenerator(optimality_template)

    # Read the source text file that contains the sections we want to extract
    # This file should have clearly marked sections using START/END markers
    source_prompt = read_source_file("source_data/user_prompt.txt")
    source_response = read_source_file("source_data/response.txt")

    # Create a dictionary mapping placeholder names to their content
    # Each key corresponds to a {{placeholder}} in the template
    # The values are extracted from the source text using markers
    variables = {
        "prompt": source_prompt,
        "response": source_response,
    }

    # Generate the final prompt by replacing all placeholders with their values
    # This combines our template structure with the extracted content
    compiled_presentation_prompt = presentation_generator.interpolate(variables)
    compiled_accuracy_prompt = accuracy_generator.interpolate(variables)
    compiled_optimality_prompt = optimality_generator.interpolate(variables)
    # Write the final prompt to a new text file called prompt.txt
    with open("compiled_prompts/presentation_prompt.txt", "w") as file:
        file.write(compiled_presentation_prompt)
    with open("compiled_prompts/accuracy_prompt.txt", "w") as file:
        file.write(compiled_accuracy_prompt)
    with open("compiled_prompts/optimality_prompt.txt", "w") as file:
        file.write(compiled_optimality_prompt)


if __name__ == "__main__":
    main()
