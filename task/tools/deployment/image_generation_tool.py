from typing import Any

from aidial_sdk.chat_completion import Message
from pydantic import StrictStr

from task.tools.deployment.base import DeploymentTool
from task.tools.models import ToolCallParams


class ImageGenerationTool(DeploymentTool):

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        message = await super()._execute(tool_call_params)

        if message.custom_content and message.custom_content.attachments:
            for attachment in message.custom_content.attachments:
                if attachment.type in ("image/png", "image/jpeg"):
                    tool_call_params.choice.append_content(f"\n\r![image]({attachment.url})\n\r")

            if not message.content:
                message.content = StrictStr('The image has been successfully generated')

        return message

    @property
    def deployment_name(self) -> str:
        return "dall-e-3"

    @property
    def name(self) -> str:
        return "generate_image"

    @property
    def description(self) -> str:
        return """
        Generate images from text descriptions using an AI image generation model.
        This tool converts detailed text prompts into visual images. It's most effective when:
        - The prompt is detailed and descriptive (e.g., "a serene mountain landscape at sunset with golden light reflecting on a lake" rather than just "mountain")
        - You need visual content creation, concept art, illustrations, or design mockups
        - The user explicitly asks to create, generate, visualize, or illustrate something
        Best practices:
        - Use specific details about style, composition, colors, and mood
        - Include artist references or art styles if relevant (e.g., "in the style of impressionism")
        - Mention lighting conditions and time of day for better results
        - Avoid ambiguous or vague descriptions
        - Note any constraints or specific elements that must be included
        Do NOT use this tool for:
        - Editing or modifying existing images
        - Text-to-speech or other non-visual tasks
        - Generating images of real people (privacy concerns)
        """

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Extensive description of the image that should be generated."
                },
                "size": {
                    "type": "string",
                    "description": "The size of the generated image.",
                    "enum": [
                        "1024x1024",
                        "1024x1792",
                        "1792x1024"
                    ],
                    "default": "1024x1024"
                },
                "style": {
                    "type": "string",
                    "description": "The style of the generated image. Must be one of `vivid` or `natural`. \n- `vivid` causes the model to lean towards generating hyper-realistic and dramatic images. \n- `natural` causes the model to produce more natural, less realistic looking images.",
                    "enum": [
                        "natural",
                        "vivid"
                    ],
                    "default": "natural"
                },
                "quality": {
                    "type": "string",
                    "description": "The quality of the image that will be generated. 'hd' creates images with finer details and greater consistency across the image.",
                    "enum": [
                        "standard",
                        "hd"
                    ],
                    "default": "standard"
                }
            },
            "required": [
                "prompt"
            ]
        }

